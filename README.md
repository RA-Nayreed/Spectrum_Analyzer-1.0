# Spectrum Analyzer 1.0

**Spectrum Analyzer 1.0** is a Python-based GUI tool that allows users to analyze and visualize spectral data using various techniques, including background subtraction and intensity calculations. It uses `Tkinter` for the GUI and `Matplotlib` for plotting the spectral data.

## Features
- **Load Data**: Load your spectral data from text files.
- **Plot Spectral Data**: View the frequency spectrum visually.
- **Background Removal**: Select two points on the plot to remove a linear background.
- **Intensity Calculation**: Calculate the area under the spectral curve using the trapezoidal rule.
- **Save Plot**: Save the generated plot as a PNG image.
- **User-Friendly GUI**: Built with `Tkinter` for a smooth user experience.

## Installation

### Requirements:
- Python 3.13.2 (or later)
- Tkinter (usually included with Python)
- Numpy
- Matplotlib

### Steps to Install:
1. Clone or download the project to your local machine.
2. Install the necessary dependencies:
   ```bash
   pip install numpy matplotlib
