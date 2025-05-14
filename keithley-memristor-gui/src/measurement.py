import time
import numpy as np
import pyvisa

class Measurement:
    def __init__(self, instrument):
        self.instrument = instrument
        self.voltages = []
        self.currents = []

    def voltage_sweep(self, start_voltage, stop_voltage, step_voltage, delay):
        """
        Execute a voltage sweep and measure current at each step
        
        Args:
            start_voltage (float): Starting voltage
            stop_voltage (float): Ending voltage
            step_voltage (float): Step size
            delay (float): Delay between measurements
            
        Returns:
            tuple: Lists of voltages and corresponding currents
        """
        # Initialize data lists
        self.voltages = []
        self.currents = []
        
        try:
            # First ramp safely to start voltage
            self.instrument.ramp_voltage(start_voltage)
            
            # Calculate step count for proper np.linspace
            if step_voltage == 0:
                # Just a single point measurement if step is 0
                step_count = 1
            else:
                step_count = abs(int((stop_voltage - start_voltage) / step_voltage)) + 1
                
            # Generate evenly spaced voltage points
            voltage_points = np.linspace(start_voltage, stop_voltage, step_count)
            
            # Perform the sweep
            for voltage in voltage_points:
                # Set voltage (without ramping within the sweep)
                self.instrument.set_voltage(voltage)
                
                # Wait for device settling
                time.sleep(delay)
                
                # Measure current
                current = self.instrument.measure_current()
                
                # Store results
                self.voltages.append(voltage)
                self.currents.append(current)
                
                # Print feedback
                print(f"V = {voltage:.6f} V, I = {current:.6e} A")
            
            # Safety: ramp back to 0V after measurement
            self.instrument.ramp_voltage(0)
                
            return self.voltages, self.currents
            
        except Exception as e:
            # Ensure safe state on error
            print("Error during sweep, shutting down safely")
            self.instrument.safe_shutdown()
            raise e

    def validate_parameters(self, start_voltage, stop_voltage, step_voltage, delay):
        if not all(isinstance(param, (int, float)) for param in [start_voltage, stop_voltage, step_voltage, delay]):
            raise ValueError("All parameters must be numeric values.")
            
        if step_voltage == 0:
            raise ValueError("Step voltage cannot be zero.")
            
        if delay < 0:
            raise ValueError("Delay time cannot be negative.")
            
        # Validate step direction matches voltage sweep direction
        if start_voltage < stop_voltage and step_voltage < 0:
            raise ValueError("Step voltage must be positive when start voltage < stop voltage.")
            
        if start_voltage > stop_voltage and step_voltage > 0:
            raise ValueError("Step voltage must be negative when start voltage > stop voltage.")

    def execute_measurement(self, start_voltage, stop_voltage, step_voltage, delay):
        self.validate_parameters(start_voltage, stop_voltage, step_voltage, delay)
        return self.voltage_sweep(start_voltage, stop_voltage, step_voltage, delay)