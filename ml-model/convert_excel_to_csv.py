import pandas as pd
import os

# Input Excel file path
input_file = "ml-model/data/Online Retail.xlsx"

# Output CSV file path
output_file = "ml-model/data/online_retail.csv"

def convert_excel_to_csv():
    try:
        print("Reading Excel file...")
        df = pd.read_excel(input_file)

        print(f"Converting to CSV and saving to: {output_file}")
        df.to_csv(output_file, index=False)
        print("Conversion successful ✅")

    except Exception as e:
        print("❌ Error during conversion:", e)

if __name__ == "__main__":
    convert_excel_to_csv()
