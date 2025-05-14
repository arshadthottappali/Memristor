import pyvisa

class Instrument:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.instrument = None

    def connect(self, resource_name):
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
        if self.instrument:
            self.instrument.write(f"VOLT {voltage}")

    def measure_current(self):
        if self.instrument:
            return float(self.instrument.query("MEAS:CURR?"))

    def set_voltage_source_mode(self):
        if self.instrument:
            self.instrument.write("FUNC 'VOLT'")

    def set_current_measurement_mode(self):
        if self.instrument:
            self.instrument.write("FUNC 'CURR'")