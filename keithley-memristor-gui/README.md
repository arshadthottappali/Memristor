# Keithley Memristor GUI

This project is a user-friendly graphical user interface (GUI) developed in Python for controlling a Keithley 2602 source meter connected via GPIB. The application is designed to perform memristor measurements, allowing users to define and execute voltage sweep experiments while visualizing the resulting current-voltage (I-V) characteristics in real-time.

## Features

- **Instrument Connection**: 
  - Input for GPIB resource name.
  - Connect button to establish communication with the Keithley 2602.
  - Status indicator for connection status and instrument identification.
  - Robust error handling for connection failures.

- **Measurement Parameter Input**: 
  - Input fields for start voltage, stop voltage, step voltage, and delay time.
  - Basic input validation to ensure numerical values are entered.

- **Voltage Sweep Execution**: 
  - Start Measurement button to initiate the voltage sweep.
  - Non-blocking measurement process to prevent GUI freezing.

- **Real-time Data Visualization**: 
  - Dynamic plotting of measured current versus applied voltage.
  - Clear labels and grid for better readability.

- **Data Saving**: 
  - Save Data button to export measured data to a CSV file.
  - File dialog for user to choose save location and filename.

## Installation

To set up the project, you need to install the required libraries. You can do this using pip. First, ensure you have Python installed, then run the following command:

```
pip install -r requirements.txt
```

### Windows-Specific Setup

When running on Windows 11, you can use a pure Python approach (no vendor libraries needed) or install vendor drivers:

1. **Pure Python Approach (Recommended)**:
   - No need to install vendor VISA libraries
   - Install the required Python packages:
     ```
     pip install pyvisa pyvisa-py
     ```
   - Install the appropriate GPIB interface library for your hardware:
     ```
     pip install gpib-ctypes  # For NI GPIB adapters
     # OR
     pip install prologix-gpib-ethernet  # For Prologix adapters
     ```

2. **GPIB Interface Hardware**:
   - Ensure your GPIB interface hardware (such as a NI GPIB-USB-HS adapter) is properly connected
   - Install any required hardware drivers from the manufacturer

3. **Test Connectivity**:
   - Use the included diagnostic tool to verify GPIB communication:
     ```
     python src/test_windows_gpib.py
     ```
   - This tool will scan for GPIB devices using various VISA implementations

4. **GPIB Address**:
   - The default GPIB address is set to 26
   - If your Keithley 2602 is configured with a different address, you'll need to enter it in the GUI or modify the address in the instrument settings

For detailed Windows 11 setup instructions, see the [Windows Setup Guide](windows_setup.md).

## Usage

1. Open the application by running `src/main.py`.
2. Enter the GPIB resource name of the Keithley 2602 (default is "GPIB::26::INSTR").
3. Click the "Connect" button to establish communication with the instrument.
   - If the connection fails, click "Diagnostics" to troubleshoot connection issues
   - You can also click "List Resources" to see available GPIB devices
4. Specify the measurement parameters (start voltage, stop voltage, step voltage, delay time, current compliance).
5. Click "Start Measurement" to begin the voltage sweep and visualize the I-V characteristics in real-time.
   - If needed, you can click "Abort" to safely stop the measurement
6. Use the "Save Data" button to save the measured data to a file.

## Identifying GPIB Address

To identify the correct GPIB address of the Keithley 2602, you can use the following steps:

1. Connect the Keithley 2602 to your computer via GPIB.
2. Use a GPIB controller or software that can scan for connected devices.
3. Note the GPIB address displayed for the Keithley 2602.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.