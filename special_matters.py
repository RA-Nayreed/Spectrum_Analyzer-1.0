"""
Spectrum Analyzer 1.0
=====================

This module implements a GUI for analyzing spectral data using Tkinter and
Matplotlib. The application provides functionalities to load measurement data,
plot spectral data, remove a linear background by selecting two points on the
plot, calculate intensities using the trapezoidal rule, save the plotted figure
as a PNG image, and quit via a dedicated "Quit" button.

Usage:
------
1. Ensure the following dependencies are installed:
   - Python 3.13.2
   - tkinter
   - numpy
   - matplotlib
2. Custom font file "Helvetica.ttf" in the "fonts" folder (optional).
3. Run the script:
       python spectrum_analyzer.py

Classes:
--------
SpectrumAnalyzerApp:
    Sets up the GUI, processes data, handles plotting, background removal,
    intensity calculation, and saving the figure.

Methods:
--------
__init__(self, root):
    Initializes the main window, data variables, and creates GUI widgets.
create_widgets(self):
    Sets up the button panel with custom fonts and the plotting canvas.
load_data(self):
    Opens a folder dialog, loads text files using numpy, and processes the data.
plot_data(self):
    Clears previous plots and draws the current spectral data on the canvas.
remove_background(self):
    Lets the user select two points to define a linear background and removes it.
calculate_intensities(self):
    Lets the user select two points to compute the area under the curve.
save_figure(self):
    Opens a file dialog to save the current figure as a PNG image.
get_user_points(self, num_points):
    Collects a specified number of points from user clicks on the plot.

Dependencies:
-------------
- tkinter: For creating the GUI.
- numpy: For numerical operations and data processing.
- matplotlib: For plotting the spectral data.
- os: For operating system interactions.

Author:
-------

REZWAN AHMAD NAYREED :)

"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk, scrolledtext
import numpy as np
import matplotlib.figure as mplfig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SpectrumAnalyzerApp:
    """Sets up the GUI, processes data, handles plotting, background removal,
    intensity calculation, and saving the figure."""
    def __init__(self, master):
        self.root = master
        self.root.title("Spectrum Analyzer 1.0")

        self.data = None  # Holds processed data
        self.binding_energies = None  # x-axis values
        self.sum_intensities = None  # y-axis values
        self.points_collected = None  # Variable for waiting for user points
        self.file_names = []  # List to hold the loaded file names
        self.selected_file = tk.StringVar()
        self.file_paths = []

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        """Initialize and arrange GUI widgets in the main application window.

        Creates a left-aligned control panel containing:
        - Data loading controls
        - Data visualization buttons
        - Analysis tools
        - A styled exit button
        """
        # Create a frame for the buttons on the left
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        custom_font = font.Font(family="fonts/Helvetica", size=8)

        # Put all buttons inside the button_frame

        tk.Button(
            button_frame, text="Load Data", command=self.load_data, font=custom_font
            ).pack(pady=5)

        self.file_selector = ttk.Combobox(
            button_frame, textvariable=self.selected_file, state="readonly"
        )
        self.file_selector.pack(pady=5)
        self.file_selector.bind("<<ComboboxSelected>>", self.load_selected_file)

        tk.Button(
            button_frame, text="Plot Data", command=self.plot_data, font=custom_font
        ).pack(pady=5)

        tk.Button(
            button_frame, text="Remove Background", command=self.remove_background,
            font=custom_font
        ).pack(pady=5)

        tk.Button(
            button_frame, text="Calculate Intensities", command=self.calculate_intensities,
            font=custom_font
        ).pack(pady=5)

        tk.Button(
            button_frame, text="Save Figure", command=self.save_figure, font=custom_font
        ).pack(pady=5)

        tk.Button(
            button_frame, text="Quit", command=self.root.quit, bg="red", fg="white",
            font=("Helvetica", 14, "bold")
        ).pack(side=tk.BOTTOM, pady=10)

        # Canvas for the plot (packs to the right)
        self.figure = mplfig.Figure(figsize=(8, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.results_text = scrolledtext.ScrolledText(button_frame,
                                                        font=custom_font,
                                                        height=10,
                                                        width=30,
                                                        wrap=tk.WORD)
        self.results_text.pack(pady=10, fill=tk.BOTH, expand=True)
        self.results_text.configure(state='disabled')

    def load_data(self):
        """Loads data from selected folder and populates the file selector with available files."""

        folder = filedialog.askdirectory(title="Select Folder Containing Measurement Files")
        if not folder:
            return

        # Get all .txt files in the selected folder
        self.file_paths =[os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.txt')]
        if not self.file_paths:
            messagebox.showerror("Error", "No text files found in the selected folder.")
            return

        self.file_selector['values'] = [os.path.basename(f) for f in self.file_paths]
        self.file_selector.set("Select a file")
        messagebox.showinfo("Success", "Files loaded successfully!")

    def load_selected_file(self, event=None):
        """Handles file selection and loads the selected data file."""
        selected_file = self.selected_file.get()
        if not selected_file or selected_file == "Select a file":
            return

        file_path = next(f for f in self.file_paths if os.path.basename(f) == selected_file)
        try:
            data = np.loadtxt(file_path)
            self.binding_energies = data[:, 0]
            self.sum_intensities = data[:, 1]
            self.data = (self.binding_energies, self.sum_intensities)
            messagebox.showinfo("Success", f"Loaded {selected_file} successfully!")
        except IOError:
            messagebox.showerror("Error", f"Failed to load {selected_file}: File not found.")
        except ValueError:
            messagebox.showerror("Error", f"Failed to load {selected_file}: Invalid data format.")

    def plot_data(self):
        """Plots the spectral data on the canvas."""
        if self.data is None:
            messagebox.showerror("Error", "No data loaded. Please load data first.")
            return

        self.ax.clear()
        self.ax.plot(self.binding_energies, self.sum_intensities, label="Spectrum")
        self.ax.set_xlabel("Binding Energy (eV)")
        self.ax.set_ylabel("Intensity")
        self.ax.set_title("Photoionization Spectrum")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def remove_background(self):
        """Removes the linear background from the spectral data."""
        if self.data is None:
            messagebox.showerror("Error", "No data loaded. Please load data first.")
            return

        # User selects two points on the graph
        points = self.get_user_points(2)
        if len(points) != 2:
            return

        # Order points by x-value
        x1, y1 = points[0]
        x2, y2 = points[1]
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        # Remove linear background
        linear_fit = slope * self.binding_energies + intercept
        self.sum_intensities -= linear_fit
        self.plot_data()

    def calculate_intensities(self):
        """Calculates the intensities (area under the curve) using the trapezoidal rule."""
        if self.data is None:
            messagebox.showerror("Error", "No data loaded. Please load data first.")
            return

        # User selects two intervals on the graph
        points = self.get_user_points(2)
        if len(points) < 2:
            return

        # Sort the x-values to ensure proper integration range
        x_values = sorted([pt[0] for pt in points])
        x_lower, x_upper = x_values[0], x_values[1]

        start_idx = np.argmin(np.abs(self.binding_energies - x_lower))
        end_idx = np.argmin(np.abs(self.binding_energies - x_upper))
        if start_idx >= end_idx:
            messagebox.showerror("Error", "Invalid range selected.")
            return

        # Calculate area using trapezoidal rule
        area = np.trapz(self.sum_intensities[start_idx:end_idx],
                        self.binding_energies[start_idx:end_idx])
        messagebox.showinfo("Intensity", f"Calculated Intensity: {area}")

        # Update text widget instead of showing messagebox
        self.results_text.configure(state='normal')
        self.results_text.insert(tk.END, f"Intensity({x_lower:.2f}-{x_upper:.2f} eV): {area:.4f}\n")
        self.results_text.see(tk.END)  # Auto-scroll to bottom
        self.results_text.configure(state='disabled')

    def save_figure(self):
        """Saves the current plot as a PNG image."""
        file_path = filedialog.asksaveasfilename(title="Save Figure",
                                                 filetypes=[("PNG files", "*.png")],
                                                 defaultextension=".png")
        if not file_path:
            return

        try:
            self.figure.savefig(file_path)
            messagebox.showinfo("Success", "Figure saved successfully!")
        except IOError:
            messagebox.showerror("Error", "Failed to save figure: IOError.")

    def get_user_points(self, num_points):
        """
        Helper function to let the user click on the plot to select points.
        Waits until 'num_points' are collected.
        """
        points = []
        self.points_collected = tk.BooleanVar(value=False)

        def onclick(event):
            if event.xdata is not None and event.ydata is not None:
                points.append((event.xdata, event.ydata))
                if len(points) == num_points:
                    self.canvas.mpl_disconnect(cid)
                    self.points_collected.set(True)

        cid = self.canvas.mpl_connect('button_press_event', onclick)
        messagebox.showinfo("Instructions", f"Click {num_points} points on the graph.")
        self.root.wait_variable(self.points_collected)
        return points


if __name__ == "__main__":
    root = tk.Tk()
    app = SpectrumAnalyzerApp(root)
    root.mainloop()
