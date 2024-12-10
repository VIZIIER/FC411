import pandas as pd
import os
import sys
import argparse
from pathlib import Path


def print_banner():
    banner = """
________ ________          ___   ___    _____    _____     
|\  _____\\   ____\        |\  \ |\  \  / __  \  / __  \    
\ \  \__/\ \  \___|        \ \  \\_\  \|\/_|\  \|\/_|\  \   
 \ \   __\\ \  \            \ \______  \|/ \ \  \|/ \ \  \  
  \ \  \_| \ \  \____        \|_____|\  \   \ \  \   \ \  \ 
   \ \__\   \ \_______\             \ \__\   \ \__\   \ \__\

    \|__|    \|_______|              \|__|    \|__|    \|__|
   [Wardriving Attack Project By: Bader, Adel, Abdulkarim, Muhannad, Sultan ]                                              
                                                             """
    print("\033[94m" + banner + "\033[0m")  # Print in blue color
    print("-" * 50)


def get_file_gui():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(
            title="Select the input CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
    except:
        return None


def get_file_cli():
    """Get file path from command line input"""
    while True:
        file_path = input("Enter the path to your CSV file (or 'q' to quit): ")
        if file_path.lower() == 'q':
            sys.exit(0)
        if os.path.exists(file_path) and file_path.endswith('.csv'):
            return file_path
        print("Invalid file path.  Enter a valid path to a CSV file.")


def clean_and_save_data(input_file, output_file):
    try:
        # Load the data
        print(f"\nReading file: {input_file}")
        df = pd.read_csv(input_file)

        df.columns = df.columns.str.strip()

        required_columns = ['Latitude', 'Longitude', 'BSSID', 'ESSID', 'Power', 'Security', 'Type']
        for column in required_columns:
            if column not in df.columns:
                raise KeyError(f"Missing required column: {column}")

        #Drop rows with empty or zero values in any column
        df = df.dropna()  # Drop rows with NaN
        df = df[~(df.isin([0, '0'])).any(axis=1)]

        #Remove duplicates based on BSSID
        df = df.drop_duplicates(subset=['BSSID'])

        #Save the cleaned data to a new CSV file
        df.to_csv(output_file, index=False)

        print(f"\n✓ Cleaned data saved to: {output_file}")
        print(f"✓ Total unique devices processed: {len(df)}")
        print(f"✓ Access Points found: {len(df[df['Type'] == 'AP'])}")
        print(f"✓ Clients found: {len(df[df['Type'] == 'Client'])}")

    except Exception as e:
        print(f"\n❌ Error occurred during data cleaning: {str(e)}")
        raise


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process wireless capture data.')
    parser.add_argument('--input', '-i', help='Input CSV file path')
    parser.add_argument('--output', '-o', help='Output CSV file path')
    parser.add_argument('--cli', action='store_true', help='Force CLI mode')
    return parser.parse_args()


def main():
    print_banner()

    args = parse_arguments()
    input_file = args.input
    output_file = args.output

    if not input_file:
        if not args.cli:
            input_file = get_file_gui()
        if not input_file:
            input_file = get_file_cli()

    # Verify input file exists
    if not os.path.exists(input_file):
        print(f"\n❌ Error: Input file '{input_file}' not found!")
        return

    # If no output file specified, use default name in same directory as input
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / 'Done.csv')

    try:
        clean_and_save_data(input_file, output_file)
    except Exception as e:
        print(f"\n❌ Failed to process file: {str(e)}")


if __name__ == "__main__":
    main()