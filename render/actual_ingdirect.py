import pandas as pd
import sys
import os
import csv
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

def convert_xls_to_csv(input_file):
    output_file = os.path.splitext(input_file)[0] + "_processed.csv"

    try:
        df = pd.read_excel(input_file, header=None, dtype=str)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        sys.exit(1)

    print("First 10 rows before processing:")
    print(df.head(10))

    # Buscar la fila que contiene "F. VALOR"
    header_row_idx = df[df.apply(lambda row: row.astype(str).str.contains('F. VALOR', case=False, na=False).any(), axis=1)].index.min()

    if header_row_idx is None:
        print("Error: No se encontró la fila de encabezado con 'F. VALOR'.")
        sys.exit(1)

    print(f"Detected header at row index: {header_row_idx}")

    # Extraer nombres de las columnas
    column_names = df.iloc[header_row_idx].str.strip().str.lower().tolist()

    # Volver a leer el archivo saltando filas anteriores y usando los nombres correctos
    df = pd.read_excel(input_file, skiprows=header_row_idx + 1, names=column_names, dtype=str)

    # Mapeo de nombres esperados
    column_mapping = {
        'f. valor': 'Date',
        'descripción': 'Description',
        'importe (€)': 'Amount'
    }

    # Verificar si las columnas esperadas están presentes
    missing_cols = [col for col in column_mapping if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing expected columns: {missing_cols}")
        print(f"Detected columns: {list(df.columns)}")
        sys.exit(1)

    # Renombrar columnas y seleccionar solo las necesarias
    df = df.rename(columns=column_mapping)[['Date', 'Description', 'Amount']]

    processed_rows = []

    for index, row in df.iterrows():
        try:
            date_str = row['Date']
            payee = row['Description']
            amount = row['Amount']

            if pd.isnull(date_str) or (isinstance(date_str, str) and date_str.strip() == ""):
                print(f"Skipping row {index + header_row_idx + 1} due to missing or invalid date")
                continue

            print(f"Raw date at row {index + header_row_idx + 1}: '{date_str}'")
            
            # Intentar convertir la fecha directamente si ya está en formato YYYY-MM-DD
            dt = pd.to_datetime(date_str, format='%Y-%m-%d %H:%M:%S', errors='coerce')
            
            if pd.isnull(dt):
                dt = pd.to_datetime(date_str, dayfirst=True, errors='coerce')
            
            if pd.isnull(dt):
                print(f"Skipping row {index + header_row_idx + 1} due to invalid date format: '{date_str}'")
                continue

            formatted_date = dt.strftime('%d/%m/%Y')

            if pd.isnull(amount) or isinstance(amount, str) and amount.strip() == "":
                print(f"Skipping row {index + header_row_idx + 1} due to missing amount")
                continue

            amount_str = str(amount).replace(',', '.').strip()
            amount_float = float(amount_str)

            amount_formatted = f"{amount_float:.2f}".rstrip('0').rstrip('.')

            payee = str(payee).replace('/', '').replace('\\', '').replace(',', '').strip()

            processed_rows.append([formatted_date, payee, '', amount_formatted])
        
        except Exception as e:
            print(f"Error processing row {index + header_row_idx + 1}: {e}")

    processed_df = pd.DataFrame(processed_rows, columns=['Date', 'Payee', 'Notes', 'Amount'])
    processed_df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    print(f"Processed data saved to '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.xls>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_xls_to_csv(input_file)
