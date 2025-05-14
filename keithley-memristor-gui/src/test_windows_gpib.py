#!/usr/bin/env python3
"""
Windows-specific GPIB Connection Test Script
This script attempts to connect to a GPIB device on Windows using various VISA DLL paths.
Run this script on the Windows system to diagnose GPIB connectivity issues.
"""

import sys
import os
import time
import pyvisa

def test_windows_gpib_connection(address="GPIB::26::INSTR"):
    """Test connection to a GPIB device on Windows using multiple VISA implementations"""
    print(f"\n{'='*60}")
    print(f" Windows GPIB Connection Test for address: {address}")
    print(f"{'='*60}\n")
    
    if not sys.platform.startswith('win'):
        print("This script is designed for Windows environments.")
        print(f"Current platform: {sys.platform}")
        print("You can still try, but results may not be useful.")
        print()
    
    print(f"System information:")
    print(f"- Python: {sys.version}")
    print(f"- OS: {sys.platform}")
    try:
        print(f"- PyVISA version: {pyvisa.__version__}")
    except:
        print("- PyVISA version: Unknown (module not imported correctly)")
    print()

    # Try PyVISA-py (pure Python backend)
    print("\n(1) Trying PyVISA-py (pure Python backend)...")
    try:
        rm = pyvisa.ResourceManager('@py')
        print(f"- Using PyVISA-py backend")
        print(f"- Available resources: {rm.list_resources()}")
        test_connection(rm, address)
    except Exception as e:
        print(f"- Error: {str(e)}")
        
    # Try default VISA implementation
    print("\n(2) Trying default VISA implementation...")
    try:
        rm = pyvisa.ResourceManager()
        print(f"- VISA DLL path: {rm.visalib.library_path}")
        print(f"- Available resources: {rm.list_resources()}")
        test_connection(rm, address)
    except Exception as e:
        print(f"- Error: {str(e)}")

    # List of common VISA DLL locations
    visa_dlls = [
        # NI-VISA paths
        r"C:\\Windows\\System32\\visa32.dll",
        r"C:\\Program Files\\IVI Foundation\\VISA\\Win64\\Bin\\visa32.dll",
        r"C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\Bin\\visa32.dll",
        
        # Keysight/Agilent VISA paths
        r"C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll",
        
        # Other possible locations
        r"C:\\VXIPNP\\WinNT\\Bin\\visa32.dll",
        r"C:\\Program Files\\IVI Foundation\\VISA\\Win64\\agvisa\\agbin\\visa32.dll"
    ]
    
    # Try each VISA DLL path
    for i, dll_path in enumerate(visa_dlls, 3):
        print(f"\n({i}) Trying VISA DLL at: {dll_path}")
        if not os.path.exists(dll_path):
            print(f"- DLL not found at this location")
            continue
            
        try:
            rm = pyvisa.ResourceManager(dll_path)
            print(f"- Successfully loaded VISA library")
            print(f"- Available resources: {rm.list_resources()}")
            test_connection(rm, address)
        except Exception as e:
            print(f"- Error: {str(e)}")
    
    print("\n\nTroubleshooting tips for Windows:")
    print("1. Pure Python approach (no vendor libraries needed):")
    print("   - Make sure pyvisa-py is installed: pip install pyvisa-py")
    print("   - For NI GPIB hardware: pip install gpib-ctypes")
    print("   - For Prologix GPIB hardware: pip install prologix-gpib-ethernet")
    print("2. Alternative: Install a vendor VISA implementation:")
    print("   - NI-VISA: https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html")
    print("   - Keysight IO Libraries: https://www.keysight.com/find/iosuite")
    print("3. Make sure your GPIB adapter is properly connected and drivers installed")
    print("3. Check Windows Device Manager for any issues with GPIB hardware")
    print("4. Try using the NI Measurement & Automation Explorer (NI MAX) to verify the instrument is visible")
    print("5. Verify the instrument is set to GPIB address 26 (or update the script with the correct address)")

def test_connection(resource_manager, address):
    """Test connection to specified address using given resource manager"""
    try:
        print(f"- Attempting connection to {address}...")
        inst = resource_manager.open_resource(address)
        print(f"- Connection successful!")
        
        # Try to get IDN
        try:
            print("- Sending *IDN? query...")
            idn = inst.query("*IDN?").strip()
            print(f"- Device response: {idn}")
        except Exception as e:
            print(f"- Failed to query device with *IDN?: {e}")
            print("- Trying Keithley 2602 specific TSP command...")
            try:
                idn = inst.query("print(_VERSION)").strip()
                print(f"- Keithley TSP version: {idn}")
            except Exception as e2:
                print(f"- TSP command failed too: {e2}")
        
        inst.close()
        print("- Connection closed")
        
    except Exception as e:
        print(f"- Failed to connect: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_windows_gpib_connection(sys.argv[1])
    else:
        test_windows_gpib_connection()
