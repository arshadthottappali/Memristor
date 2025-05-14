import time
import numpy as np
import pyvisa

class Measurement:
    def __init__(self, instrument):
        self.instrument = instrument

    def voltage_sweep(self, start_voltage, stop_voltage, step_voltage, delay):
        voltages = np.arange(start_voltage, stop_voltage + step_voltage, step_voltage)
        currents = []

        for voltage in voltages:
            self.instrument.set_voltage(voltage)
            time.sleep(delay)
            current = self.instrument.measure_current()
            currents.append(current)

        return voltages, currents

    def validate_parameters(self, start_voltage, stop_voltage, step_voltage, delay):
        if not all(isinstance(param, (int, float)) for param in [start_voltage, stop_voltage, step_voltage, delay]):
            raise ValueError("All parameters must be numeric values.")
        if step_voltage <= 0:
            raise ValueError("Step voltage must be greater than zero.")
        if delay < 0:
            raise ValueError("Delay time cannot be negative.")
        if start_voltage > stop_voltage:
            raise ValueError("Start voltage must be less than or equal to stop voltage.")

    def execute_measurement(self, start_voltage, stop_voltage, step_voltage, delay):
        self.validate_parameters(start_voltage, stop_voltage, step_voltage, delay)
        return self.voltage_sweep(start_voltage, stop_voltage, step_voltage, delay)