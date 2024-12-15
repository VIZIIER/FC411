# FC411 Wireless Network Analyzer for Wardriving Attack Project

A Python-based wireless network analysis tool that processes wireless capture data and generates an interactive map visualization of discovered networks. This tool is part of the Wardriving Attack Project.

## Features

### Data Cleaning (`clean.py`)
- Removes duplicate network entries
- Filters out invalid or incomplete data
- Removes entries with zero values or empty fields
- Multiple interface options for file selection (GUI/CLI)
- Cross-platform compatibility (Windows/Linux)

### Network Mapping (`map.py`)
- Creates interactive HTML maps of discovered networks
- Interactive interface for file selection (GUI/CLI)
- Clustered markers for better visualization
- Color-coded markers based on security type:
  - WPA: Red
  - WPA2: Blue
  - WPA3: Green
  - Others: Gray
- Detailed network information in popups including:
  - BSSID (MAC Address)
  - ESSID (Network Name)
  - Power (Signal Strength)
  - Security Type
  - Device Type
- Automatic map opening in default browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VIZIIER/FC411.git
cd FC411
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Data Cleaning (Step 1)

Run the cleaning script using any of these methods:

1. GUI Mode (Default):
```bash
python clean.py
```

2. CLI Mode:
```bash
python clean.py --cli
```

3. Direct file paths:
```bash
python clean.py -i input.csv -o output.csv
```

### Map Generation (Step 2)

Generate the map using any of these methods:

1. GUI Mode (Default):
```bash
python map.py
```

2. CLI Mode:
```bash
python map.py --cli
```

3. Direct file paths:
```bash
python map.py -i input.csv -o network_map.html
```

## Input File Format

The input CSV file should contain the following columns:
- LocalTime: Timestamp of the capture
- GPSTime: GPS timestamp
- ESSID: Network name
- BSSID: MAC address
- Power: Signal strength
- Security: Network security type (WPA/WPA2/WPA3)
- Latitude: GPS latitude
- Longitude: GPS longitude
- Type: Device type (AP/Client)

## Output Files

### From clean.py:
- Cleaned CSV file (default: `Done.csv`)
- Removes duplicates and invalid entries
- Preserves original column structure with clean data

### From map.py:
- Interactive HTML map (default: `network_map.html`)
- Opens automatically in default web browser
- Shows all networks with their locations and details

## System Requirements

### Software Requirements:
- Python 3.x
- Modern web browser for map viewing

### Python Dependencies:
- pandas: Data processing
- folium: Map generation
- branca: Map styling
- tkinter: GUI support (usually included with Python)

## Command Line Arguments

### clean.py:
- `-i` or `--input`: Input CSV file path
- `-o` or `--output`: Output CSV file path
- `--cli`: Force CLI mode

### map.py:
- `-i` or `--input`: Input CSV file path
- `-o` or `--output`: Output HTML file path
- `--cli`: Force CLI mode

## Project Team

- Bader
- Adel
- Sultan
- Abdulkarim
- Muhannad


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Troubleshooting

### Common Issues:
1. **File Not Found**: Ensure the input file path is correct
2. **Missing Columns**: Verify CSV file format matches requirements
3. **Invalid Coordinates**: Check GPS data in input file
4. **GUI Not Working**: Use CLI mode with --cli flag

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Important Note

This tool is for educational and research purposes only. Always ensure you have proper authorization before conducting wireless network analysis in any area.

## Note

This tool is for educational purposes only. Ensure you have permission to analyze wireless networks in your area.
