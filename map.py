import pandas as pd
import os
import folium
from folium.plugins import MarkerCluster
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
    print("\033[94m" + banner + "\033[0m")
    print("-" * 50)


def get_file_gui():
    """Try to use GUI file dialog, fall back to CLI if not available"""
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
        print("Invalid file path. Please enter a valid path to a CSV file.")


def get_marker_color(security_type):
    security_colors = {
        'WPA': 'red',
        'WPA2': 'blue',
        'WPA3': 'green',
    }
    normalized_security_type = str(security_type).strip().upper()
    return security_colors.get(normalized_security_type, 'gray')


def map_networks(input_file, output_file=None):
    try:
        print(f"\nReading file: {input_file}")
        df = pd.read_csv(input_file)

        #Clean data
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=['Latitude', 'Longitude', 'Security'])

        map_center = [df['Latitude'].iloc[0], df['Longitude'].iloc[0]]
        network_map = folium.Map(location=map_center, zoom_start=15)

        marker_cluster = MarkerCluster().add_to(network_map)

        for _, row in df.iterrows():
            popup_text = f"""
            <b>BSSID:</b> {row['BSSID']}<br>
            <b>ESSID:</b> {row['ESSID']}<br>
            <b>Power:</b> {row['Power']}<br>
            <b>Security:</b> {row['Security']}<br>
            <b>Type:</b> {row['Type']}
            """
            marker_color = get_marker_color(row['Security'])
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=popup_text,
                tooltip=row['ESSID'] if pd.notna(row['ESSID']) else 'Unknown Network',
                icon=folium.Icon(color=marker_color, icon="wifi")
            ).add_to(marker_cluster)

        if output_file is None:
            output_file = os.path.join(os.path.dirname(input_file), "network_map.html")

        network_map.save(output_file)

        print(f"\n✓ The network map has been saved to: {os.path.abspath(output_file)}")
        print(f"✓ Total networks mapped: {len(df)}")
        print(f"✓ Access Points mapped: {len(df[df['Type'] == 'AP'])}")
        print(f"✓ Clients mapped: {len(df[df['Type'] == 'Client'])}")

        import webbrowser
        webbrowser.open(output_file)

    except Exception as e:
        print("\n❌ Error occurred while generating the map.")
        import traceback
        traceback.print_exc()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate wireless network map from CSV data.')
    parser.add_argument('--input', '-i', help='Input CSV file path')
    parser.add_argument('--output', '-o', help='Output HTML file path')
    parser.add_argument('--cli', action='store_true', help='Force CLI mode')
    return parser.parse_args()


def main():
    print_banner()

    args = parse_arguments()
    input_file = args.input
    output_file = args.output

    # If no input file specified, try GUI then fall back to CLI
    if not input_file:
        if not args.cli:
            input_file = get_file_gui()
        if not input_file:
            input_file = get_file_cli()

    # Verify input file exists
    if not os.path.exists(input_file):
        print(f"\n❌ Error: Input file '{input_file}' not found!")
        return

    try:
        map_networks(input_file, output_file)
    except Exception as e:
        print(f"\n❌ Failed to generate map: {str(e)}")


if __name__ == "__main__":
    main()