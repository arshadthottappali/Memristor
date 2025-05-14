# Windows 11 Setup Guide for Keithley Memristor GUI

This guide provides detailed instructions for setting up the Keithley Memristor GUI application on Windows 11. Since the application was developed in a Linux environment but will run on Windows, this guide addresses specific Windows considerations.

## Prerequisites

- Windows 11 (64-bit)
- Python 3.9 or newer (3.10+ recommended)
- GPIB hardware interface (e.g., NI GPIB-USB-HS adapter)
- Keithley 2602 source meter configured with GPIB address 26

## Step 1: Install Python

1. Download Python for Windows from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer and ensure you check the box to "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

## Step 2: VISA Implementation Options

The application requires a VISA (Virtual Instrument Software Architecture) implementation to communicate with GPIB devices. You have three options:

### Option 1: Use PyVISA-py (No Additional Installation Required)

This option uses the pure Python backend for PyVISA (`pyvisa-py`), which is automatically installed when you install the application's requirements.

**Benefits:**
- No need to install vendor-specific VISA libraries like NI-VISA or IO Libraries Suite
- Works with many GPIB adapters through Python libraries
- Simpler installation process

**Setup Steps:**
1. Install the PyVISA and PyVISA-py packages:
   ```
   pip install pyvisa pyvisa-py
   ```

2. Install the appropriate Python package for your GPIB hardware:
   - For NI GPIB adapters: `pip install gpib-ctypes`
   - For Prologix GPIB adapters: `pip install prologix-gpib-ethernet`
   - For Linux-GPIB compatible adapters: `pip install linux-gpib`

3. When connecting in the application:
   - Select "No" when prompted to use the NI-VISA backend
   - This ensures the application uses the pure Python PyVISA-py backend

### Option 2: National Instruments VISA (Better Hardware Support)

If the pure Python option doesn't work with your hardware, you can install NI-VISA:

1. Download NI-VISA from [National Instruments](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html)
2. Install the package, following the on-screen instructions
3. Restart your computer after installation

### Option 3: Keysight/Agilent IO Libraries

An alternative vendor implementation:

1. Download the IO Libraries Suite from [Keysight](https://www.keysight.com/find/iosuite)
2. Install the package, following the on-screen instructions
3. Restart your computer after installation

## Step 3: Connect the GPIB Hardware

1. Connect your GPIB interface (e.g., NI GPIB-USB-HS) to your computer
2. Connect the Keithley 2602 to the GPIB interface using a GPIB cable
3. Turn on the Keithley 2602 source meter
4. If using NI hardware, open NI MAX (Measurement & Automation Explorer) to verify the instrument is detected

## Step 4: Install the Application

1. Extract the application files to a directory of your choice
2. Open Command Prompt and navigate to the application directory
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Step 5: Test GPIB Connectivity

1. Run the Windows-specific GPIB diagnostic tool:
   ```
   python src/test_windows_gpib.py
   ```
2. This tool will:
   - Check multiple VISA implementations to find which one works on your system
   - List all available GPIB devices
   - Try to connect to the device at GPIB address 26
   - Display detailed information to help troubleshoot any connection issues

3. If you need to specify a different GPIB address, you can pass it as an argument:
   ```
   python src/test_windows_gpib.py GPIB::25::INSTR
   ```

## Step 6: Launch the Application

1. Start the application by running:
   ```
   python src/main.py
   ```

2. In the GPIB Address field, enter `GPIB::26::INSTR` (or your device's actual address)
3. Click "Connect" to establish communication with the Keithley 2602

## Troubleshooting

### Connection Issues

1. **Check Hardware Connections**
   - Verify that all cables are properly connected
   - Ensure the Keithley 2602 is powered on

2. **Verify GPIB Address**
   - Double-check that the GPIB address in the application matches the address set on your Keithley 2602

3. **VISA Implementation Issues**
   - Click the "Diagnostics" button in the application to see detailed information about available VISA backends
   - In the connection dialog, try switching between VISA backends (NI-VISA and PyVISA-py)
   - For PyVISA-py issues:
     - Ensure you have installed the correct Python package for your GPIB hardware
     - Run `python -m pyvisa.cmd info` in the command prompt to get detailed PyVISA diagnostic information
     - Try running with verbose output: `python -m pyvisa.cmd list --debug`

4. **Windows Device Manager**
   - Open Windows Device Manager to check if the GPIB hardware is properly detected
   - Look for any warning icons indicating driver issues

### Python Module Issues

If you encounter errors about missing modules, install the core requirements and GPIB interface dependencies:

```
# Core application requirements
pip install pyvisa pyvisa-py matplotlib numpy pandas

# For Windows-specific features
pip install pywin32

# Choose the appropriate GPIB interface library based on your hardware
pip install gpib-ctypes  # For NI GPIB adapters
# OR
pip install prologix-gpib-ethernet  # For Prologix GPIB adapters
# OR
pip install linux-gpib  # For Linux-GPIB compatible adapters
```

For additional debugging tools, you can install:
```
pip install pyvisa-sim  # For VISA simulation capabilities
```

### Permission Issues

If the application fails to access the GPIB device:
1. Try running Command Prompt as Administrator
2. Start the application from the administrator command prompt

## Advanced Configuration

### Editing Default GPIB Address

The default GPIB address is set to 26. If you need to change it, edit the following files:

1. `src/gui.py`: Look for the line containing `GPIB::26::INSTR` 
2. `src/test_gpib.py` and `src/test_windows_gpib.py`: Change the default parameter in the test functions

### Simulation Mode

If you do not have the hardware connected, you can run the application in simulation mode:
1. Launch the application normally
2. When prompted to select a connection mode, choose "Simulation Mode"

This allows you to test the application's functionality without actual hardware.
