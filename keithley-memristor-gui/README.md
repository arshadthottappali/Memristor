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

## Usage

1. Open the application by running `src/main.py`.
2. Enter the GPIB resource name of the Keithley 2602.
3. Click the "Connect" button to establish communication with the instrument.
4. Specify the measurement parameters (start voltage, stop voltage, step voltage, delay time).
5. Click "Start Measurement" to begin the voltage sweep and visualize the I-V characteristics in real-time.
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