import pandas as pd
import os
from datetime import datetime


def print_banner():
    banner = """
________ ________          ___   ___    _____    _____     
|\  _____\\   ____\        |\  \ |\  \  / __  \  / __  \    
\ \  \__/\ \  \___|        \ \  \\_\  \|\/_|\  \|\/_|\  \   
 \ \   __\\ \  \            \ \______  \|/ \ \  \|/ \ \  \  
  \ \  \_| \ \  \____        \|_____|\  \   \ \  \   \ \  \ 
   \ \__\   \ \_______\             \ \__\   \ \__\   \ \__\
   
    \|__|    \|_______|              \|__|    \|__|    \|__|
              [Wardriving Attack Project By Group]                                              
                                                            
                                                            """
    print("\033[94m" + banner + "\033[0m")  # Print in blue color
    print("-" * 50)


def clean_string(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def process_wifi_log(file_path):
    try:
        df = pd.read_csv(file_path)

        df.columns = df.columns.str.strip()

        df['LocalTime'] = pd.to_datetime(df['LocalTime'])

        latest_entries = df.sort_values('LocalTime').groupby('BSSID').last().reset_index()

        latest_entries = latest_entries.sort_values(['Type', 'Power'], ascending=[True, False])

        latest_entries.to_csv('Done.csv', index=False)

        #summary
        ap_count = len(latest_entries[latest_entries['Type'] == 'AP'])
        client_count = len(latest_entries[latest_entries['Type'] == 'Client'])

        print("\nSummary:")
        print(f"✓ Found {ap_count} unique access points")
        print(f"✓ Found {client_count} unique client devices")
        print(f"✓ Total entries processed: {len(df)}")
        print(f"✓ Unique devices after processing: {len(latest_entries)}")
        print(f"\nOutput saved to: Done.csv")

        print("\nSample of processed data:")
        print("-" * 50)
        print(latest_entries[['LocalTime', 'ESSID', 'BSSID', 'Type', 'Power']].head().to_string())
        print("-" * 50)

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\nCheck if the CSV file format is correct.")


def main():
    print_banner()
    input_file = 'war-01.log.csv'

    if not os.path.exists(input_file):
        print(f"\n❌ Error: Input file '{input_file}' not found!")
        return

    process_wifi_log(input_file)


if __name__ == "__main__":
    main()