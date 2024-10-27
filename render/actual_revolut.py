import csv
import sys
from datetime import datetime
import os

def process_files(input_file):
    # Generate output file name by appending '_processed' to the input file name
    output_file = os.path.splitext(input_file)[0] + "_processed.csv"

    with open(input_file, mode='r') as infile:
        reader = csv.reader(infile)
        # Skip the header
        next(reader)

        # Prepare a list to store processed rows
        processed_rows = []
        
        for row in reader:
            # Extract the third field (date and time)
            datetime_str = row[2]  # e.g. '2024-10-07 19:33:24'
            # Convert the string to a datetime object
            dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            # Format the date to DD/MM/YYYY
            formatted_date = dt.strftime('%d/%m/%Y')
            # Extract the fifth and sixth fields
            description = row[4]  # Description (used as Payee)
            amount = row[5]       # Amount
            
            # Ensure the amount uses a point as the decimal separator
            amount_formatted = amount.replace('.', '.')  # Point as decimal separator
            # Remove decimal part if it's '.00'
            if amount_formatted.endswith('.00'):
                amount_formatted = amount_formatted[:-3]  # Remove '.00'
            
            # Add the new row to the list with empty Notes field
            processed_rows.append([formatted_date, description, '', amount_formatted])

    # Write the processed data to a new file without quotes
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)  # Use QUOTE_MINIMAL to avoid issues
        # Write the header
        writer.writerow(['Date', 'Payee', 'Notes', 'Amount'])
        # Write the processed rows
        writer.writerows(processed_rows)

    print(f"Processed data saved in '{output_file}'.")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_files(input_file)
