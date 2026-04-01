# 1D Materials Analysis Tool

A comprehensive desktop application for analyzing 1D material spectroscopic data, with a focus on Raman spectroscopy and UV-Vis absorption spectroscopy.

## Features

### 1. Raman Spectroscopy Analysis
- **Multi-file Import**: Import multiple Raman data files simultaneously
- **Peak Detection**: Automatic peak detection with customizable parameters
- **Baseline Correction**: Built-in baseline correction for cleaner spectra
- **Multi-plot Display**: Overlay multiple spectra for comparison
- **Customizable Plotting**:
  - Adjustable axis labels and font sizes
  - Customizable line styles and colors
  - Grid and legend options
- **Data Export**: Export processed data and plots in various formats

### 2. UV-Vis Absorption Spectroscopy Analysis
- **Absorption Curve Plotting**: Visualize absorption spectra
- **Band Gap Calculation**: Estimate optical band gap from absorption data
- **Multi-sample Comparison**: Compare absorption spectra from different samples
- **Customizable Visualization**: Adjust plot parameters for publication-quality figures

### 3. User Interface
- **Modern Qt-based Interface**: Built with PyQt5 and QFluentWidgets
- **Dark/Light Theme**: Support for both dark and light themes
- **Intuitive Navigation**: Tab-based interface for easy switching between analysis modes
- **Real-time Preview**: Instant visualization of data processing results

## Installation

### Option 1: Download Executable (Windows)
1. Download `1D_Materials_Analysis_Tool.exe` from the `dist` folder
2. Run the executable directly (no installation required)

### Option 2: Run from Source
1. Clone this repository:
   ```bash
   git clone https://github.com/dachuanx/cnt_raman_tool.git
   cd cnt_raman_tool
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python 1Dtool.py
   ```

## Requirements

If running from source, install the following packages:

```bash
pip install PyQt5
pip install qfluentwidgets
pip install matplotlib
pip install numpy
pip install pandas
pip install scipy
```

## Usage

### Raman Analysis
1. Launch the application
2. Navigate to the "Raman Analysis" tab
3. Click "Import Data" to load Raman spectra files
4. Use the controls to:
   - Adjust peak detection sensitivity
   - Apply baseline correction
   - Customize plot appearance
   - Export results

### Absorption Analysis
1. Navigate to the "Absorption Analysis" tab
2. Import absorption data files
3. Visualize absorption curves
4. Calculate and analyze band gap information

## File Structure

```
1DMaterialsAnalysisTool/
├── 1Dtool.py              # Main application entry point
├── pages/
│   ├── page_raman.py      # Raman spectroscopy interface
│   ├── page_absorption.py # Absorption spectroscopy interface
│   └── page_transmittance.py # Transmittance analysis interface
├── dist/
│   └── 1D_Materials_Analysis_Tool.exe # Windows executable
└── README.md              # This file
```

## Data Format

The application supports common data formats for spectroscopic data:

### Raman Data Format
- CSV files with two columns: Wavenumber (cm⁻¹) and Intensity
- TXT files with tab-separated values
- Excel files with appropriate column headers

### Absorption Data Format
- CSV/TXT files with Wavelength (nm) and Absorbance columns
- Support for multiple concentration samples

## Development

### Building from Source
To build the executable yourself:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="1D_Materials_Analysis_Tool" 1Dtool.py
```

### Adding New Features
The modular design makes it easy to add new analysis modules:
1. Create a new Python file in the `pages` directory
2. Implement the analysis interface following the existing patterns
3. Import and integrate it into the main application

## License

This project is available for academic and research use. Please contact the author for commercial licensing.

## Contact

For questions, bug reports, or feature requests, please open an issue on GitHub or contact the maintainer.

## Acknowledgments

- Built with PyQt5 and QFluentWidgets for the modern UI
- Uses Matplotlib for scientific visualization
- Inspired by the need for user-friendly materials characterization tools