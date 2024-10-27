import pandas as pd
import sys
import os
import csv

def convert_xls_to_csv(input_file):
    # Generate output file name by appending '_processed' to the input file name
    output_file = os.path.splitext(input_file)[0] + "_processed.csv"

    # Read the Excel file, starting from the 4th row (index 3)
    df = pd.read_excel(input_file, skiprows=3)  # Start processing from row 4

    # Prepare a list to store processed rows
    processed_rows = []

    for index, row in df.iterrows():
        try:
            # Debug print to check the content of the current row
            print(f"Processing row {index + 4}: {row.values}")  # Display the contents of the row
            
            # Access values based on the new column mapping
            date_str = row.iloc[0]  # Column 1 (Date)
            payee = row.iloc[2]      # Column 3 (Payee)
            amount = row.iloc[3]     # Column 4 (Amount)

            # Strip any whitespace from the date string
            date_str = str(date_str).strip()

            # Convert date to datetime and format it to DD/MM/YYYY
            if date_str:
                # Attempt to parse the date with dayfirst=True
                dt = pd.to_datetime(date_str, dayfirst=True, errors='raise')
                formatted_date = dt.strftime('%d/%m/%Y')
            else:
                print(f"Skipping row {index + 4} due to invalid date format: '{date_str}'")
                continue
            
            # Ensure the amount uses a point as the decimal separator
            amount_formatted = str(amount).replace(',', '.')
            # Remove decimal part if it's '.00'
            if amount_formatted.endswith('.00'):
                amount_formatted = amount_formatted[:-3]  # Remove '.00'

            # Remove slashes, backslashes, and commas from the payee string
            payee = str(payee).replace('/', '').replace('\\', '').replace(',', '').strip()

            # Add the new row to the list with empty Notes field
            processed_rows.append([formatted_date, payee, '', amount_formatted])
        
        except ValueError as ve:
            print(f"Skipping row {index + 4} due to parsing error: {ve}")  # Adjusting for the skipped rows
            continue  # Skip this row if there's an error

        except Exception as e:
            print(f"An unexpected error occurred while processing row {index + 4}: {e}")

    # Create a DataFrame from the processed rows
    processed_df = pd.DataFrame(processed_rows, columns=['Date', 'Payee', 'Notes', 'Amount'])

    # Write the processed data to a new CSV file without quotes
    processed_df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')  # Use csv.QUOTE_NONE

    print(f"Processed data saved in '{output_file}'.")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.xls>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_xls_to_csv(input_file)
