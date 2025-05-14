from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from tkinter.filedialog import asksaveasfilename
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import numpy as np
from instrument import Instrument
from measurement import Measurement
from utils import validate_numerical_input, save_data_to_csv, show_error_message

class KeithleyMemristorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Keithley Memristor Measurement GUI")

        self.instrument = None
        self.voltage_sweep = None
        self.measurement = None  # Add this line

        self.gpib_address = StringVar()
        self.start_voltage = StringVar()
        self.stop_voltage = StringVar()
        self.step_voltage = StringVar()
        self.delay_time = StringVar()

        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        Label(self.master, text="GPIB Address:").grid(row=0, column=0)
        Entry(self.master, textvariable=self.gpib_address).grid(row=0, column=1)

        Button(self.master, text="Connect", command=self.connect_instrument).grid(row=0, column=2)
        Button(self.master, text="List Resources", command=self.list_resources).grid(row=0, column=3)

        Label(self.master, text="Start Voltage (V):").grid(row=1, column=0)
        Entry(self.master, textvariable=self.start_voltage).grid(row=1, column=1)

        Label(self.master, text="Stop Voltage (V):").grid(row=2, column=0)
        Entry(self.master, textvariable=self.stop_voltage).grid(row=2, column=1)

        Label(self.master, text="Step Voltage (V):").grid(row=3, column=0)
        Entry(self.master, textvariable=self.step_voltage).grid(row=3, column=1)

        Label(self.master, text="Delay Time (s):").grid(row=4, column=0)
        Entry(self.master, textvariable=self.delay_time).grid(row=4, column=1)

        Button(self.master, text="Start Measurement", command=self.start_measurement).grid(row=5, column=0, columnspan=3)

        Button(self.master, text="Save Data", command=self.save_data).grid(row=6, column=0, columnspan=3)

    def create_plot(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("I-V Characteristics")
        self.ax.set_xlabel("Voltage (V)")
        self.ax.set_ylabel("Current (A)")
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=3)

    def connect_instrument(self):
        try:
            self.instrument = Instrument(simulation_mode=True)  # Use simulation mode for testing
            idn = self.instrument.connect(self.gpib_address.get() or "GPIB::24::INSTR")
            messagebox.showinfo("Connection Status", f"Connected to instrument: {idn}")
        except Exception as e:
            if "VI_ERROR_INV_RSRC_NAME" in str(e):
                messagebox.showerror(
                    "Connection Error",
                    "Invalid GPIB resource name specified.\n"
                    "Ensure the GPIB address is in the correct format (e.g., GPIB::24::INSTR).\n"
                    "You can also use the 'List Resources' feature to find available instruments."
                )
            else:
                messagebox.showerror("Connection Error", f"Failed to connect to instrument: {str(e)}")

    def start_measurement(self):
        try:
            start_v = float(self.start_voltage.get()) if validate_numerical_input(self.start_voltage.get()) else 0
            stop_v = float(self.stop_voltage.get()) if validate_numerical_input(self.stop_voltage.get()) else 1
            step_v = float(self.step_voltage.get()) if validate_numerical_input(self.step_voltage.get()) else 0.1
            delay = float(self.delay_time.get()) if validate_numerical_input(self.delay_time.get()) else 0.1

            self.measurement = Measurement(self.instrument)
            self.instrument.set_voltage_source_mode()
            self.instrument.set_current_measurement_mode()

            threading.Thread(target=self.execute_measurement, args=(start_v, stop_v, step_v, delay), daemon=True).start()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")

    def execute_measurement(self, start_v, stop_v, step_v, delay):
        try:
            voltages, currents = self.measurement.execute_measurement(start_v, stop_v, step_v, delay)
            # Store the voltage and current values for later use
            self.measurement.voltages = voltages  # This could cause issues
            self.measurement.currents = currents  # This could cause issues
            for v, c in zip(voltages, currents):
                self.ax.plot(v, c, 'bo')
                self.canvas.draw()
        except Exception as e:
            show_error_message(f"Measurement Error: {str(e)}")

    def save_data(self):
        if self.measurement:
            filename = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                save_data_to_csv(filename, self.measurement.voltages, self.measurement.currents)
                messagebox.showinfo("Data Saving", "Data saved successfully.")
        else:
            show_error_message("No data to save.")

    def list_resources(self):
        try:
            import pyvisa
            # Explicitly use pyvisa-py backend
            rm = pyvisa.ResourceManager('@py')
            resources = rm.list_resources()
            if resources:
                messagebox.showinfo("Available Resources", f"Connected instruments:\n{', '.join(resources)}")
            else:
                messagebox.showinfo("Available Resources", "No instruments found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list resources: {str(e)}\nMake sure pyvisa-py is installed.")

if __name__ == "__main__":
    root = Tk()
    app = KeithleyMemristorGUI(root)
    root.mainloop()