import pandas as pd
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Input Excel file path relative to the script's directory
input_file_name = "Online Retail.xlsx"
input_file = os.path.join(script_dir, "data", input_file_name) # ml-model/data/Online Retail.xlsx

# Output CSV file path relative to the script's directory
output_file_name = "online_retail.csv"
output_file = os.path.join(script_dir, "data", output_file_name) # ml-model/data/online_retail.csv

def convert_excel_to_csv():
    try:
        print(f"Reading Excel file from: {input_file}") # اضافه شده برای وضوح
        # بررسی وجود فایل ورودی قبل از خواندن (اختیاری اما خوب است)
        if not os.path.exists(input_file):
            print(f"❌ Error: Input file not found at {input_file}")
            return

        df = pd.read_excel(input_file)

        print(f"Converting to CSV and saving to: {output_file}")
        # اطمینان از وجود دایرکتوری خروجی (اختیاری اما خوب است)
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        df.to_csv(output_file, index=False)
        print("Conversion successful ✅")

    except Exception as e:
        print("❌ Error during conversion:", e)

if __name__ == "__main__":
    convert_excel_to_csv()