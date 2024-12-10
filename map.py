import pandas as pd
import os
import folium
from folium.plugins import MarkerCluster

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

def get_marker_color(security_type):

    security_colors = {
        'WPA': 'red',
        'WPA2': 'blue',
        'WPA3': 'green',
    }
    normalized_security_type = str(security_type).strip().upper()
    return security_colors.get(normalized_security_type, 'gray')

def map_networks(file_path):
    try:
        df = pd.read_csv(file_path)

        # Clean data
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

        map_file = "network_map.html"
        network_map.save(map_file)

        print(f"\n✓ The network map has been saved to: {os.path.abspath(map_file)}")

        import webbrowser
        webbrowser.open(map_file)

    except Exception as e:
        print("\n❌ Error occurred while generating the map.")
        import traceback
        traceback.print_exc()

def main():
    print_banner()
    input_file = 'Done.csv'

    if not os.path.exists(input_file):
        print(f"\n❌ Error: Input file '{input_file}' not found!")
        return

    map_networks(input_file)

if __name__ == "__main__":
    main()
