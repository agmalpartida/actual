import pandas as pd
import sys
import os
import csv
import warnings

# Silenciar advertencias sobre conversiones de fechas
warnings.simplefilter(action='ignore', category=UserWarning)

def convert_xls_to_csv(input_file):
    # Generar el nombre del archivo de salida
    output_file = os.path.splitext(input_file)[0] + "_processed.csv"

    # Leer el archivo de Excel, comenzando desde la fila 4
    try:
        df = pd.read_excel(input_file, skiprows=3)
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        sys.exit(1)

    # Mostrar las columnas detectadas para depuración
    print("Columnas detectadas en el archivo:", df.columns)

    # Renombrar columnas relevantes
    expected_columns = ['Fecha', 'Categoría', 'Subcategoría', 'Descripción', 'Comentario', 'Imagen', 'Importe', 'Saldo']
    df.columns = expected_columns

    # Filtrar solo las columnas necesarias
    df = df[['Fecha', 'Descripción', 'Importe']]

    # Lista para almacenar las filas procesadas
    processed_rows = []

    for index, row in df.iterrows():
        try:
            # Acceso a los valores por nombre de columna
            date_str = row['Fecha']       # Columna Fecha
            payee = row['Descripción']    # Columna Descripción
            amount = row['Importe']       # Columna Importe

            # Validar fecha
            if pd.isnull(date_str) or (isinstance(date_str, str) and date_str.strip() == ""):
                print(f"Saltando fila {index + 4} debido a la falta de fecha o valor inválido")
                continue

            # Intentar convertir la fecha
            try:
                dt = pd.to_datetime(date_str, format='%d/%m/%Y', errors='raise')
                formatted_date = dt.strftime('%d/%m/%Y')
            except ValueError:
                print(f"Saltando fila {index + 4} debido a formato de fecha inválido: '{date_str}'")
                continue

            # Validar monto
            if pd.isnull(amount) or isinstance(amount, str) and amount.strip() == "":
                print(f"Saltando fila {index + 4} debido a la falta de monto")
                continue
            
            # Limpieza del monto
            amount_str = str(amount).replace(',', '.').strip()  # Reemplazar comas por puntos y quitar espacios
            
            # Validar si el monto es convertible a float
            try:
                amount_float = float(amount_str)
            except ValueError:
                print(f"Saltando fila {index + 4} debido a un valor de monto no procesable: '{amount_str}'")
                continue
            
            # Formatear el monto a string y eliminar '.00' si es necesario
            amount_formatted = f"{amount_float:.2f}"  # Asegurar 2 decimales
            if amount_formatted.endswith('.00'):
                amount_formatted = amount_formatted[:-3]  # Eliminar '.00'

            # Formatear el beneficiario eliminando caracteres no deseados
            payee = str(payee).replace('/', '').replace('\\', '').replace(',', '').strip()

            # Agregar la fila procesada a la lista
            processed_rows.append([formatted_date, payee, '', amount_formatted])
        
        except ValueError as ve:
            print(f"Saltando fila {index + 4} debido a un error de análisis: {ve}")
            continue

        except Exception as e:
            print(f"Ocurrió un error inesperado al procesar la fila {index + 4}: {e}")

    # Crear DataFrame de las filas procesadas
    processed_df = pd.DataFrame(processed_rows, columns=['Date', 'Payee', 'Notes', 'Amount'])

    # Escribir los datos procesados en un archivo CSV sin comillas
    processed_df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    print(f"Datos procesados guardados en '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <input_file.xls>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_xls_to_csv(input_file)
