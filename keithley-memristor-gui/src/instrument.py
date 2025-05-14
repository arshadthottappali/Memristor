import pyvisa
import numpy as np
import time
import random

class Instrument:
    def __init__(self, simulation_mode=False):
        self.simulation_mode = simulation_mode
        if not simulation_mode:
            try:
                self.rm = pyvisa.ResourceManager('@py')
            except Exception:
                self.rm = pyvisa.ResourceManager()
        self.instrument = None
        self.current_voltage = 0

    def connect(self, resource_name):
        if self.simulation_mode:
            return "KEITHLEY INSTRUMENTS INC.,MODEL 2602,1398687,3.0.0"
        try:
            self.instrument = self.rm.open_resource(resource_name)
            # Set appropriate timeout and termination characters
            self.instrument.timeout = 10000  # 10 seconds
            self.instrument.write_termination = '\n'
            self.instrument.read_termination = '\n'
            
            # Reset the instrument and clear buffers
            self.instrument.write("reset()")
            time.sleep(0.5)  # Give it time to reset
            
            # Verify connection with simple command
            idn = self.instrument.query("print(_VERSION)")
            return f"KEITHLEY 2602 TSP Version: {idn}"
        except Exception as e:
            raise ConnectionError(f"Failed to connect to instrument: {e}")

    def disconnect(self):
        if self.simulation_mode:
            return
            
        if self.instrument:
            # Turn off output before disconnecting
            self.instrument.write("smua.source.output = smua.OUTPUT_OFF")
            self.instrument.close()
            self.instrument = None

    def set_voltage(self, voltage):
        if self.simulation_mode:
            self.current_voltage = voltage
            return
            
        if self.instrument:
            # Set voltage level
            self.instrument.write(f"smua.source.levelv = {voltage}")

    def measure_current(self):
        if self.simulation_mode:
            # Simulate memristor behavior with hysteresis
            time.sleep(0.01)  # Simulate measurement delay
            return float(self.current_voltage) * (0.001 + random.random() * 0.0002)
            
        if self.instrument:
            # Measure and return current
            return float(self.instrument.query("print(smua.measure.i())"))

    def set_voltage_source_mode(self):
        if self.simulation_mode:
            return
            
        if self.instrument:
            # Configure for voltage source mode and current measurement
            self.instrument.write("smua.source.func = smua.OUTPUT_DCVOLTS")
            self.instrument.write("smua.source.autorangev = smua.AUTORANGE_ON")
            self.instrument.write("smua.source.levelv = 0")  # Start at 0V
            self.instrument.write("smua.measure.autorangei = smua.AUTORANGE_ON")
            self.instrument.write("smua.measure.nplc = 1")  # Integration time (adjust as needed)
            self.instrument.write("smua.source.output = smua.OUTPUT_ON")

    def set_current_measurement_mode(self):
        if self.simulation_mode:
            return
            
        if self.instrument:
            # Configure current measurement settings
            self.instrument.write("smua.measure.autozero = smua.AUTOZERO_ONCE")
            # Set current compliance (protection)
            self.instrument.write("smua.source.limiti = 0.1")  # 100mA limit

    def set_current_compliance(self, limit_amps):
        """
        Set current compliance limit to protect the device
        
        Args:
            limit_amps (float): Maximum allowed current in amperes
        """
        if self.simulation_mode:
            return
            
        if self.instrument:
            try:
                # Convert to scientific notation for better precision
                self.instrument.write(f"smua.source.limiti = {limit_amps}")
                print(f"Current compliance set to {limit_amps} A")
            except Exception as e:
                raise RuntimeError(f"Failed to set current compliance: {e}")

    def ramp_voltage(self, target_voltage, step_size=0.1, delay=0.02):
        """
        Gradually ramp voltage to target value for device safety
        
        Args:
            target_voltage (float): Target voltage in volts
            step_size (float): Voltage step size for ramping
            delay (float): Delay between steps in seconds
        """
        if self.simulation_mode:
            self.current_voltage = target_voltage
            return
            
        if not self.instrument:
            raise RuntimeError("Instrument not connected")
            
        try:
            # Get current voltage
            current_voltage = 0
            try:
                current_voltage = float(self.instrument.query("print(smua.source.levelv)"))
            except:
                # If query fails, assume starting from 0
                pass
            
            # Calculate steps
            if abs(target_voltage - current_voltage) <= step_size:
                # If the difference is smaller than step_size, just set the voltage directly
                self.set_voltage(target_voltage)
                return
                
            # Determine step direction
            if target_voltage > current_voltage:
                steps = np.arange(current_voltage, target_voltage, step_size)
            else:
                steps = np.arange(current_voltage, target_voltage, -step_size)
                
            # Apply voltage gradually
            for voltage in steps:
                self.set_voltage(voltage)
                time.sleep(delay)
            
            # Final set to ensure we reach exact target
            self.set_voltage(target_voltage)
            
        except Exception as e:
            raise RuntimeError(f"Error during voltage ramp: {e}")

    def safe_shutdown(self):
        """Safely shutdown the instrument"""
        if self.simulation_mode:
            return
            
        if self.instrument:
            try:
                # Ramp voltage to 0V
                self.ramp_voltage(0)
                # Turn off output
                self.instrument.write("smua.source.output = smua.OUTPUT_OFF")
                print("Instrument safely shut down")
            except Exception as e:
                print(f"Warning: Error during safe shutdown: {e}")

    def self_test(self):
        """Perform instrument self-test and verify basic functionality"""
        if self.simulation_mode:
            time.sleep(1)  # Simulate test delay
            return "Self-test passed (Simulation Mode)"
            
        if not self.instrument:
            raise RuntimeError("Instrument not connected")
            
        try:
            # First ensure output is off
            self.instrument.write("smua.source.output = smua.OUTPUT_OFF")
            
            # Run TSP built-in self-test
            result = self.instrument.query("print(smua.selftest.run())")
            
            # 0 means success
            if result.strip() == "0":
                # Now test communication by setting/reading a parameter
                self.instrument.write("smua.measure.nplc = 1.0")
                nplc = self.instrument.query("print(smua.measure.nplc)").strip()
                
                if abs(float(nplc) - 1.0) < 0.01:
                    return "Self-test passed. Communication verified."
                else:
                    return f"Self-test passed but parameter readback failed: NPLC={nplc}"
            else:
                return f"Self-test failed with code: {result}"
        except Exception as e:
            return f"Self-test failed: {str(e)}"