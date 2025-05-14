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
            return self.instrument.query("*IDN?")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to instrument: {e}")

    def disconnect(self):
        if self.instrument:
            self.instrument.close()
            self.instrument = None

    def set_voltage(self, voltage):
        if self.simulation_mode:
            self.current_voltage = voltage
            return
        if self.instrument:
            self.instrument.write(f"VOLT {voltage}")

    def measure_current(self):
        if self.simulation_mode:
            # Simulate memristor behavior with hysteresis
            time.sleep(0.01)  # Simulate measurement delay
            return float(self.current_voltage) * (0.001 + random.random() * 0.0002)
        if self.instrument:
            return float(self.instrument.query("MEAS:CURR?"))

    def set_voltage_source_mode(self):
        if self.simulation_mode:
            return
        if self.instrument:
            self.instrument.write("FUNC 'VOLT'")

    def set_current_measurement_mode(self):
        if self.simulation_mode:
            return
        if self.instrument:
            self.instrument.write("FUNC 'CURR'")