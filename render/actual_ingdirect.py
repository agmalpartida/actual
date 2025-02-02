import pandas as pd
import sys
import os
import csv
import warnings

# Suppress warnings about date parsing
warnings.simplefilter(action='ignore', category=UserWarning)

def convert_xls_to_csv(input_file):
    # Generate the output file name
    output_file = os.path.splitext(input_file)[0] + "_processed.csv"

    # Read the Excel file skipping the first 5 rows
    try:
        df = pd.read_excel(input_file, skiprows=5, header=None, dtype=str)  # Leer todo como string para evitar problemas de tipos
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        sys.exit(1)

    # Mostrar las primeras filas para depuración
    print("First 5 rows after skipping:")
    print(df.head())

    # Buscar la primera fila que tenga encabezados válidos
    for i in range(len(df)):
        if df.iloc[i].notna().sum() >= 3:  # Si la fila tiene al menos 3 valores no vacíos
            df.columns = df.iloc[i]  # Asigna esta fila como encabezado
            df = df[i+1:]  # Elimina las filas anteriores
            break

    # Resetear el índice después de eliminar filas
    df = df.reset_index(drop=True)

    # Expected columns to extract
    expected_columns = ['Date', 'Description', 'Amount']

    # Normalizar los nombres de las columnas (remover espacios extra, convertir a minúsculas)
    df.columns = df.columns.str.strip().str.lower()

    # Crear un mapeo de nombres esperados a los nombres detectados más cercanos
    column_mapping = {
        'date': 'date',
        'description': 'description',
        'amount': 'amount',
    }

    # Encontrar las columnas correctas
    detected_columns = {col: col for col in df.columns}  # Si los nombres coinciden exactamente
    for expected, real in column_mapping.items():
        for col in df.columns:
            if expected in col.lower():
                detected_columns[expected] = col

    # Verificar que las columnas requeridas existen
    missing_cols = [col for col in column_mapping if col not in detected_columns]
    if missing_cols:
        print(f"Error: Missing expected columns: {missing_cols}")
        sys.exit(1)

    # Seleccionar solo las columnas necesarias
    df = df[[detected_columns[col] for col in expected_columns]]

    # Renombrar columnas con nombres estándar
    df.columns = expected_columns

    # List to store processed rows
    processed_rows = []

    for index, row in df.iterrows():
        try:
            date_str = row['Date']
            payee = row['Description']
            amount = row['Amount']

            # Validate the date
            if pd.isnull(date_str) or (isinstance(date_str, str) and date_str.strip() == ""):
                print(f"Skipping row {index + 6} due to missing or invalid date")
                continue

            # Attempt to parse the date
            try:
                dt = pd.to_datetime(date_str, dayfirst=True, errors='coerce')
                if pd.isnull(dt):
                    print(f"Skipping row {index + 6} due to invalid date format: '{date_str}'")
                    continue
                formatted_date = dt.strftime('%d/%m/%Y')
            except ValueError:
                print(f"Skipping row {index + 6} due to invalid date format: '{date_str}'")
                continue

            # Validate the amount
            if pd.isnull(amount) or isinstance(amount, str) and amount.strip() == "":
                print(f"Skipping row {index + 6} due to missing amount")
                continue

            # Clean and validate the amount
            amount_str = str(amount).replace(',', '.').strip()

            try:
                amount_float = float(amount_str)
            except ValueError:
                print(f"Skipping row {index + 6} due to unprocessable amount: '{amount_str}'")
                continue

            # Format the amount
            amount_formatted = f"{amount_float:.2f}".rstrip('0').rstrip('.')  # Remove unnecessary decimals

            # Clean the payee string
            payee = str(payee).replace('/', '').replace('\\', '').replace(',', '').strip()

            # Add processed row
            processed_rows.append([formatted_date, payee, '', amount_formatted])
        
        except Exception as e:
            print(f"Error processing row {index + 6}: {e}")

    # Create DataFrame for processed rows
    processed_df = pd.DataFrame(processed_rows, columns=['Date', 'Payee', 'Notes', 'Amount'])

    # Write to CSV without quotes
    processed_df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    print(f"Processed data saved to '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.xls>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_xls_to_csv(input_file)
