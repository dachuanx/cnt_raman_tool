# CNT Analysis Tool

A desktop application for carbon nanotube (CNT) analysis, specifically designed for comparing and visualizing Raman and absorption spectra.

## Overview

This tool is built for researchers working with carbon nanotubes (CNTs) to analyze and compare spectroscopic data. It provides a user-friendly interface for loading experimental data, visualizing spectra, and performing comparative analysis.

## Features

### Core Functionality
- **Raman Spectroscopy Analysis** - Import and analyze Raman spectra from TXT files
- **Absorption Spectroscopy** - Import and analyze absorption data from Excel files
- **Comparative Curve Plotting** - Overlay multiple spectra for comparison
- **Peak Detection** - Automatic peak identification in Raman spectra
- **Data Normalization** - Normalize spectra for better comparison

### File Format Support
- **Raman Data**: TXT files (two-column format: wavenumber vs intensity)
- **Absorption Data**: Excel files (wavelength vs absorbance)

### Visualization
- Interactive matplotlib plots
- Multiple curve overlay
- Customizable axis labels and titles
- Export plots as images

## Installation

### Prerequisites
- Python 3.8+
- PyQt5
- pandas, numpy, matplotlib, scipy
- qfluentwidgets

### Quick Start
```bash
# Clone the repository
git clone https://github.com/dachuanx/cnt_raman_tool.git
cd cnt_raman_tool

# Run the application
python 1Dtool.py
```

### Windows Users
A pre-built executable is available in the `dist/` folder:
- Download `1D_Materials_Analysis_Tool.exe`
- Double-click to run (no Python installation required)

## Usage

### 1. Launch the Application
Run `1Dtool.py` or the executable file.

### 2. Raman Analysis
- Navigate to the "Raman" tab
- Click "Import Raman Data" to load TXT files
- Multiple files can be loaded for comparison
- Use peak detection to identify characteristic peaks (D-band, G-band, etc.)
- Adjust visualization settings as needed

### 3. Absorption Analysis
- Navigate to the "Absorption" tab
- Click "Import Absorption Data" to load Excel files
- Compare absorption spectra from different samples
- Analyze optical properties of CNTs

### 4. Data Comparison
- Overlay multiple spectra in the same plot
- Use normalization for fair comparison
- Export comparison plots for reports

## Project Structure

```
cnt_raman_tool/
├── 1Dtool.py              # Main application
├── pages/                 # Analysis modules
│   ├── page_raman.py     # Raman spectroscopy interface
│   ├── page_absorption.py # Absorption spectroscopy interface
│   └── page_transmittance.py # Placeholder for future features
├── dist/                  # Distribution files
│   └── 1D_Materials_Analysis_Tool.exe
└── .gitignore            # Git ignore rules
```

## Technical Details

### Raman Analysis Module
- **File Format**: TXT files with two columns (wavenumber, intensity)
- **Features**:
  - Multiple file loading and comparison
  - Automatic peak detection using scipy.signal.find_peaks
  - Baseline correction
  - Peak labeling and annotation
- **Output**: Comparative plots showing multiple Raman spectra

### Absorption Analysis Module
- **File Format**: Excel files (.xlsx, .xls)
- **Features**:
  - Excel file parsing using pandas
  - Wavelength vs absorbance plotting
  - Multiple sample comparison
  - Optical property analysis
- **Output**: Absorption spectra comparison plots

## Development

### Building the Executable
To create a standalone executable:
```bash
python build_exe.py
```

### Dependencies
- PyQt5 >= 5.15.0
- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- scipy >= 1.7.0
- qfluentwidgets >= 0.1.0

## Future Development

This tool is under active development. Planned features include:
- Enhanced data processing algorithms
- Additional spectroscopy techniques
- Improved data export options
- More customization features

## License

This project is available for academic and research use.

---

*Last Updated: April 2024*