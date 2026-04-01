# 1D Materials Analysis Tool

A comprehensive desktop application for analyzing one-dimensional materials, built with PyQt5 and Python.

## 📋 Overview

The 1D Materials Analysis Tool is a user-friendly desktop application designed for researchers and scientists working with one-dimensional materials such as carbon nanotubes (CNTs), nanowires, and other nanostructures. The tool provides multiple analysis modules for different material characterization techniques.

## ✨ Features

### Core Analysis Modules
- **Raman Spectroscopy Analysis** - Process and analyze Raman spectra of 1D materials
- **Absorption Spectroscopy** - Analyze optical absorption properties
- **Transmittance Analysis** - Calculate and visualize transmittance spectra

### Key Features
- **Modern GUI** - Built with PyQt5 and QFluentWidgets for a professional interface
- **Multi-page Design** - Organized workflow with dedicated pages for each analysis type
- **Data Visualization** - Interactive plots and charts for result presentation
- **Batch Processing** - Support for analyzing multiple samples efficiently
- **Export Capabilities** - Save results in various formats (CSV, PNG, PDF)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- PyQt5
- NumPy, SciPy, Matplotlib
- QFluentWidgets

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dachuanx/cnt_raman_tool.git
   cd cnt_raman_tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python 1Dtool.py
   ```

### For Windows Users
A pre-built executable is available in the `dist/` directory:
- Download `1D_Materials_Analysis_Tool.exe`
- Double-click to run (no Python installation required)

## 📁 Project Structure

```
1DMaterialsAnalysisTool/
├── 1Dtool.py              # Main application entry point
├── README.md              # This documentation
├── .gitignore            # Git ignore rules
├── dist/                 # Distribution directory
│   └── 1D_Materials_Analysis_Tool.exe  # Windows executable
└── pages/                # Analysis modules
    ├── __init__.py       # Package initialization
    ├── page_raman.py     # Raman spectroscopy analysis
    ├── page_absorption.py # Absorption spectroscopy analysis
    └── page_transmittance.py # Transmittance analysis
```

## 🔧 Usage

1. **Launch the application** by running `1Dtool.py` or the executable
2. **Select analysis type** from the navigation sidebar
3. **Load your data** (supports common spectroscopy file formats)
4. **Configure analysis parameters** specific to your material
5. **Run analysis** and visualize results
6. **Export results** for further processing or reporting

### Supported Data Formats
- CSV files (.csv)
- Text files (.txt, .dat)
- Excel files (.xlsx, .xls)
- Common spectroscopy instrument formats

## 📊 Analysis Capabilities

### Raman Spectroscopy Module
- Peak identification and fitting
- Background subtraction
- Intensity normalization
- D-band and G-band analysis for carbon materials
- Defect characterization

### Optical Properties Modules
- Absorption coefficient calculation
- Band gap estimation
- Transmittance/reflectance analysis
- Optical conductivity calculations

## 🛠️ Development

### Building from Source
To build the executable yourself:

```bash
python build_exe.py
```

The build script uses PyInstaller to create a standalone executable.

### Adding New Features
1. Create new analysis modules in the `pages/` directory
2. Follow the existing pattern for page structure
3. Register new pages in `1Dtool.py`
4. Test thoroughly before committing

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** - Open an issue with detailed information
2. **Suggest features** - Share your ideas for improvement
3. **Submit pull requests** - Contribute code improvements
4. **Improve documentation** - Help make the tool more accessible

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include tests for new functionality
- Update documentation when adding features

## 📝 Citation

If you use this tool in your research, please consider citing:

```
[Citation information will be added]
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For questions, suggestions, or collaboration opportunities:
- **GitHub Issues**: [https://github.com/dachuanx/cnt_raman_tool/issues](https://github.com/dachuanx/cnt_raman_tool/issues)
- **Email**: shidachuanx@126.com

## 🔄 Status

**🚧 Active Development** - This project is under continuous development with regular updates and improvements planned.

### Recent Updates
- Initial release with core analysis modules
- Windows executable available
- Multi-page interface implementation

### Planned Features
- [ ] Additional spectroscopy techniques
- [ ] Machine learning integration for pattern recognition
- [ ] Cloud data storage and sharing
- [ ] Plugin system for extensibility
- [ ] More export formats and reporting tools

---

*Last Updated: April 2024*  
*Version: 1.0.0*