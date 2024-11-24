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

    # Read the Excel file starting from row 6
    try:
        df = pd.read_excel(input_file, skiprows=5)  # Skip the first 5 rows
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        sys.exit(1)

    # Display detected columns for debugging
    print("Detected columns in the file:", df.columns)

    # Rename columns to match the expected structure
    expected_columns = ['Date', 'Category', 'Subcategory', 'Description', 'Comment', 'Image', 'Amount', 'Balance']
    df.columns = expected_columns

    # Select only the necessary columns for processing
    df = df[['Date', 'Description', 'Amount']]

    # List to store processed rows
    processed_rows = []

    for index, row in df.iterrows():
        try:
            # Access values by column name
            date_str = row['Date']        # Column 'Date'
            payee = row['Description']    # Column 'Description'
            amount = row['Amount']        # Column 'Amount'

            # Validate the date
            if pd.isnull(date_str) or (isinstance(date_str, str) and date_str.strip() == ""):
                print(f"Skipping row {index + 6} due to missing or invalid date")
                continue

            # Attempt to parse the date
            try:
                dt = pd.to_datetime(date_str, format='%d/%m/%Y', errors='raise')
                formatted_date = dt.strftime('%d/%m/%Y')
            except ValueError:
                print(f"Skipping row {index + 6} due to invalid date format: '{date_str}'")
                continue

            # Validate the amount
            if pd.isnull(amount) or isinstance(amount, str) and amount.strip() == "":
                print(f"Skipping row {index + 6} due to missing amount")
                continue

            # Clean and validate the amount
            amount_str = str(amount).replace(',', '.').strip()  # Replace commas with dots and remove spaces

            # Check if the amount is convertible to float
            try:
                amount_float = float(amount_str)
            except ValueError:
                print(f"Skipping row {index + 6} due to unprocessable amount: '{amount_str}'")
                continue

            # Format the amount to string and remove '.00' if unnecessary
            amount_formatted = f"{amount_float:.2f}"  # Ensure 2 decimals
            if amount_formatted.endswith('.00'):
                amount_formatted = amount_formatted[:-3]  # Remove '.00'

            # Clean the payee string
            payee = str(payee).replace('/', '').replace('\\', '').replace(',', '').strip()

            # Add the processed row to the list
            processed_rows.append([formatted_date, payee, '', amount_formatted])
        
        except ValueError as ve:
            print(f"Skipping row {index + 6} due to a parsing error: {ve}")
            continue

        except Exception as e:
            print(f"An unexpected error occurred while processing row {index + 6}: {e}")

    # Create DataFrame for processed rows
    processed_df = pd.DataFrame(processed_rows, columns=['Date', 'Payee', 'Notes', 'Amount'])

    # Write the processed data to a CSV file without quotes
    processed_df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    print(f"Processed data saved to '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.xls>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_xls_to_csv(input_file)
