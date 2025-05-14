from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Frame
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
        self.measurement = None

        self.gpib_address = StringVar()
        self.start_voltage = StringVar()
        self.stop_voltage = StringVar()
        self.step_voltage = StringVar()
        self.delay_time = StringVar()
        self.current_compliance = StringVar(value="0.01")  # Default 10mA
        
        # Add status indicator variable
        self.connection_status = StringVar()
        self.connection_status.set("Not Connected")

        # Add measurement control flag
        self.measurement_running = False

        self.create_widgets()
        self.create_plot()

        # Add this line to register a close event handler
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        Label(self.master, text="GPIB Address:").grid(row=0, column=0)
        Entry(self.master, textvariable=self.gpib_address).grid(row=0, column=1)

        Button(self.master, text="Connect", command=self.connect_instrument).grid(row=0, column=2)
        Button(self.master, text="List Resources", command=self.list_resources).grid(row=0, column=3)
        Button(self.master, text="Self-Test", command=self.run_self_test).grid(row=0, column=4)
        
        # Add status indicator with colored background
        self.status_label = Label(self.master, textvariable=self.connection_status, 
                            bg="red", fg="white", width=15)
        self.status_label.grid(row=0, column=5, padx=10)

        Label(self.master, text="Start Voltage (V):").grid(row=1, column=0)
        Entry(self.master, textvariable=self.start_voltage).grid(row=1, column=1)

        Label(self.master, text="Stop Voltage (V):").grid(row=2, column=0)
        Entry(self.master, textvariable=self.stop_voltage).grid(row=2, column=1)

        Label(self.master, text="Step Voltage (V):").grid(row=3, column=0)
        Entry(self.master, textvariable=self.step_voltage).grid(row=3, column=1)

        Label(self.master, text="Delay Time (s):").grid(row=4, column=0)
        Entry(self.master, textvariable=self.delay_time).grid(row=4, column=1)

        Label(self.master, text="Current Compliance (A):").grid(row=4, column=0)
        Entry(self.master, textvariable=self.current_compliance).grid(row=4, column=1)

        # Replace the existing Start Measurement button with these two buttons in a frame:
        measurement_frame = Frame(self.master)
        measurement_frame.grid(row=5, column=0, columnspan=2)
        
        Button(measurement_frame, text="Start Measurement", command=self.start_measurement).grid(row=0, column=0, padx=5)
        self.abort_button = Button(measurement_frame, text="Abort", command=self.abort_measurement, state="disabled")
        self.abort_button.grid(row=0, column=1, padx=5)

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
            # Ask if user wants simulation mode
            use_simulation = messagebox.askyesno("Connection Mode", 
                                           "Do you want to use simulation mode?\n\n"
                                           "Select 'Yes' for simulation without hardware.\n"
                                           "Select 'No' to connect to actual hardware.")
        
            self.instrument = Instrument(simulation_mode=use_simulation)
            idn = self.instrument.connect(self.gpib_address.get() or "GPIB::24::INSTR")
            
            # Update status indicator
            if use_simulation:
                self.connection_status.set("SIMULATION MODE")
                self.status_label.config(bg="blue")
            else:
                self.connection_status.set("CONNECTED")
                self.status_label.config(bg="green")
                
            messagebox.showinfo("Connection Status", f"Connected to instrument: {idn}")
        except Exception as e:
            # Update status indicator to show error
            self.connection_status.set("CONNECTION ERROR")
            self.status_label.config(bg="red")
            
            if "VI_ERROR_INV_RSRC_NAME" in str(e):
                messagebox.showerror(
                    "Connection Error",
                    "Invalid GPIB resource name specified.\n"
                    "Ensure the GPIB address is in the correct format (e.g., GPIB::24::INSTR).\n"
                    "You can also use the 'List Resources' feature to find available instruments."
                )
            else:
                messagebox.showerror("Connection Error", f"Failed to connect to instrument: {str(e)}")

    def list_resources(self):
        try:
            import pyvisa
            try:
                # Try pure Python backend first
                rm = pyvisa.ResourceManager('@py')
            except Exception:
                # Fall back to system VISA
                rm = pyvisa.ResourceManager()
                
            resources = rm.list_resources()
            if resources:
                messagebox.showinfo("Available Resources", 
                                    f"Connected instruments:\n{', '.join(resources)}")
            else:
                messagebox.showinfo("Available Resources", "No instruments found.")
        except Exception as e:
            messagebox.showerror("Error", 
                                f"Failed to list resources: {str(e)}\n"
                                "Make sure pyvisa-py is installed.")

    def start_measurement(self):
        if not self.instrument:
            messagebox.showerror("Connection Error", "Please connect to an instrument first.")
            return
            
        try:
            # Handle negative values properly with validation
            if not validate_numerical_input(self.start_voltage.get()):
                messagebox.showerror("Input Error", "Start voltage must be a valid number.")
                return
            
            if not validate_numerical_input(self.stop_voltage.get()):
                messagebox.showerror("Input Error", "Stop voltage must be a valid number.")
                return
                
            if not validate_numerical_input(self.step_voltage.get()):
                messagebox.showerror("Input Error", "Step voltage must be a valid number.")
                return
                
            if not validate_numerical_input(self.delay_time.get()):
                messagebox.showerror("Input Error", "Delay time must be a valid number.")
                return
            
            # Validate current compliance
            if not validate_numerical_input(self.current_compliance.get()):
                messagebox.showerror("Input Error", "Current compliance must be a valid number.")
                return
            
            compliance = float(self.current_compliance.get())
            if compliance <= 0:
                messagebox.showerror("Input Error", "Current compliance must be positive.")
                return
            
            start_v = float(self.start_voltage.get())
            stop_v = float(self.stop_voltage.get())
            step_v = float(self.step_voltage.get())
            delay = float(self.delay_time.get())

            # Step size validation
            if start_v < stop_v and step_v <= 0:
                messagebox.showerror("Input Error", "Step voltage must be positive when start voltage < stop voltage.")
                return
            
            if start_v > stop_v and step_v >= 0:
                messagebox.showerror("Input Error", "Step voltage must be negative when start voltage > stop voltage.")
                return

            self.measurement = Measurement(self.instrument)
            self.instrument.set_voltage_source_mode()
            self.instrument.set_current_measurement_mode()
            self.instrument.set_current_compliance(compliance)  # Set current compliance

            # Clear previous plot data before starting new measurement
            self.ax.clear()
            self.ax.set_title("I-V Characteristics")
            self.ax.set_xlabel("Voltage (V)")
            self.ax.set_ylabel("Current (A)")
            self.ax.grid(True)
            self.canvas.draw()

            # Set flag to indicate measurement is running and enable abort button
            self.measurement_running = True
            self.abort_button.config(state="normal")

            # Use threading to prevent GUI freezing
            threading.Thread(target=self.execute_measurement, 
                            args=(start_v, stop_v, step_v, delay), 
                            daemon=True).start()
        except Exception as e:
            show_error_message(f"Error starting measurement: {str(e)}")

    def save_data(self):
        if not hasattr(self, 'measurement') or not hasattr(self.measurement, 'voltages') or not self.measurement.voltages:
            messagebox.showerror("Error", "No measurement data available to save.")
            return
            
        try:
            filename = asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Measurement Data"
            )
            
            if filename:
                # Create metadata dictionary with measurement parameters
                metadata = {
                    "Start Voltage (V)": self.start_voltage.get(),
                    "Stop Voltage (V)": self.stop_voltage.get(),
                    "Step Voltage (V)": self.step_voltage.get(),
                    "Delay Time (s)": self.delay_time.get(),
                    "Current Compliance (A)": self.current_compliance.get(),
                    "Instrument": self.connection_status.get()
                }
                
                save_data_to_csv(filename, self.measurement.voltages, self.measurement.currents, metadata)
                messagebox.showinfo("Success", f"Data saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def execute_measurement(self, start_v, stop_v, step_v, delay):
        """Modified to update plot in real-time"""
        try:
            # Clear previous plot data
            self.ax.clear()
            self.ax.set_title("I-V Characteristics")
            self.ax.set_xlabel("Voltage (V)")
            self.ax.set_ylabel("Current (A)")
            self.ax.grid(True)
            line, = self.ax.plot([], [], 'bo-')
            self.canvas.draw()
            
            # Create local lists for data
            voltages = []
            currents = []
            
            # Create a measurement object
            self.measurement = Measurement(self.instrument)
            
            # Calculate step count
            if step_v == 0:
                step_count = 1
            else:
                step_count = abs(int((stop_v - start_v) / step_v)) + 1
                
            # Generate voltage points
            voltage_points = np.linspace(start_v, stop_v, step_count)
            
            # Perform the sweep with abort checking
            for i, voltage in enumerate(voltage_points):
                # Check if abort was requested
                if not self.measurement_running:
                    print("Measurement aborted by user")
                    break
                    
                # Set voltage and measure current
                self.instrument.set_voltage(voltage)
                time.sleep(delay)
                current = self.instrument.measure_current()
                
                # Store values
                voltages.append(voltage)
                currents.append(current)
                
                # Update plot in real-time
                line.set_data(voltages, currents)
                self.ax.relim()
                self.ax.autoscale_view()
                self.canvas.draw_idle()
                self.master.update()
                
                # Update progress in the window title
                progress_percent = int((i + 1) / step_count * 100)
                self.master.title(f"Keithley Memristor Measurement - {progress_percent}%")
            
            # Store data in measurement object for later saving
            self.measurement.voltages = voltages
            self.measurement.currents = currents
            
            # Reset title after completion
            self.master.title("Keithley Memristor Measurement GUI")
            
            # Final plot update
            self.ax.set_title("I-V Characteristics - Completed")
            self.canvas.draw()
            
            # Disable abort button after measurement completes
            self.abort_button.config(state="disabled")
            self.measurement_running = False
            
            # Safety: ramp back to 0V
            self.instrument.ramp_voltage(0)
            
        except Exception as e:
            self.measurement_running = False
            self.abort_button.config(state="disabled")
            messagebox.showerror("Measurement Error", str(e))
            
            # Safety in case of error
            try:
                self.instrument.ramp_voltage(0)
            except:
                pass

    def abort_measurement(self):
        """Safely abort the measurement process"""
        try:
            # Set flag to stop the measurement thread
            self.measurement_running = False
            
            # Reset instrument to safe state
            if self.instrument:
                self.instrument.ramp_voltage(0)  # Set voltage to 0V
            
            messagebox.showinfo("Measurement Aborted", 
                           "Measurement has been aborted.\nVoltage has been set to 0V for safety.")
                           
            # Update GUI elements
            self.abort_button.config(state="disabled")
            self.master.title("Keithley Memristor Measurement GUI")
        except Exception as e:
            messagebox.showerror("Error", f"Error during abort: {str(e)}")

    def run_self_test(self):
        """Run instrument self-test"""
        if not self.instrument:
            messagebox.showerror("Self-Test Error", "Instrument not connected")
            return
            
        # Show wait message
        self.master.config(cursor="wait")
        self.master.update()
        
        try:
            result = self.instrument.self_test()
            messagebox.showinfo("Self-Test Result", result)
        except Exception as e:
            messagebox.showerror("Self-Test Error", f"Failed to run self-test: {str(e)}")
        finally:
            self.master.config(cursor="")

    def on_closing(self):
        """Handle application closing"""
        try:
            if self.instrument:
                print("Shutting down instrument safely...")
                self.instrument.safe_shutdown()
        except Exception as e:
            print(f"Error during shutdown: {e}")
        
        print("Application closing...")
        self.master.destroy()