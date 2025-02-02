import pandas as pd
import sys
import os
import csv
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

def convert_xls_to_csv(input_file):
    output_file = os.path.splitext(input_file)[0] + "_processed.csv"

    try:
        df = pd.read_excel(input_file, skiprows=4, header=0, dtype=str)  # Saltar filas y forzar encabezado
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        sys.exit(1)

    print("First 5 rows after skipping:")
    print(df.head())

    # Convertir nombres de columna a string en minúsculas
    df.columns = df.columns.map(lambda x: str(x).strip().lower())

    # Forzar renombrado explícito
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
                print(f"Skipping row {index + 5} due to missing or invalid date")
                continue

            try:
                dt = pd.to_datetime(date_str, dayfirst=True, errors='coerce')
                if pd.isnull(dt):
                    print(f"Skipping row {index + 5} due to invalid date format: '{date_str}'")
                    continue
                formatted_date = dt.strftime('%d/%m/%Y')
            except ValueError:
                print(f"Skipping row {index + 5} due to invalid date format: '{date_str}'")
                continue

            if pd.isnull(amount) or isinstance(amount, str) and amount.strip() == "":
                print(f"Skipping row {index + 5} due to missing amount")
                continue

            amount_str = str(amount).replace(',', '.').strip()

            try:
                amount_float = float(amount_str)
            except ValueError:
                print(f"Skipping row {index + 5} due to unprocessable amount: '{amount_str}'")
                continue

            amount_formatted = f"{amount_float:.2f}".rstrip('0').rstrip('.')

            payee = str(payee).replace('/', '').replace('\\', '').replace(',', '').strip()

            processed_rows.append([formatted_date, payee, '', amount_formatted])
        
        except Exception as e:
            print(f"Error processing row {index + 5}: {e}")

    processed_df = pd.DataFrame(processed_rows, columns=['Date', 'Payee', 'Notes', 'Amount'])
    processed_df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    print(f"Processed data saved to '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.xls>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_xls_to_csv(input_file)
