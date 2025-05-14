#!/usr/bin/env python3
"""
GPIB Connection Test Script
This script attempts to connect to a GPIB device using various backends and provides detailed feedback.
"""

import sys
import os
import time
import pyvisa

def test_gpib_connection(address="GPIB::26::INSTR"):
    """Test connection to a GPIB device using multiple methods"""
    print(f"\n{'='*60}")
    print(f" GPIB Connection Test for address: {address}")
    print(f"{'='*60}\n")
    
    print(f"System information:")
    print(f"- Python: {sys.version}")
    print(f"- OS: {sys.platform}")
    print(f"- PyVISA version: {pyvisa.__version__}")
    print()

    # Try PyVISA-py backend
    print("\nTrying PyVISA-py backend...")
    try:
        rm = pyvisa.ResourceManager('@py')
        print(f"Available resources: {rm.list_resources()}")
        
        print(f"Attempting connection to {address}...")
        try:
            inst = rm.open_resource(address)
            print(f"Connection successful!")
            
            # Try to get IDN
            try:
                print("Sending *IDN? query...")
                idn = inst.query("*IDN?").strip()
                print(f"Device response: {idn}")
            except Exception as e:
                print(f"Failed to query device: {e}")
                print("Trying Keithley 2602 specific TSP command...")
                try:
                    idn = inst.query("print(_VERSION)").strip()
                    print(f"Keithley TSP version: {idn}")
                except Exception as e2:
                    print(f"TSP command failed too: {e2}")
            
            inst.close()
            print("Connection closed")
            
        except Exception as e:
            print(f"Failed to connect: {e}")
    except Exception as e:
        print(f"Failed to initialize PyVISA-py backend: {e}")

    # Try NI-VISA backend
    print("\nTrying NI-VISA backend...")
    try:
        rm = pyvisa.ResourceManager('')
        print(f"Available resources: {rm.list_resources()}")
        
        print(f"Attempting connection to {address}...")
        try:
            inst = rm.open_resource(address)
            print(f"Connection successful!")
            
            # Try to get IDN
            try:
                print("Sending *IDN? query...")
                idn = inst.query("*IDN?").strip()
                print(f"Device response: {idn}")
            except Exception as e:
                print(f"Failed to query device: {e}")
                print("Trying Keithley 2602 specific TSP command...")
                try:
                    idn = inst.query("print(_VERSION)").strip()
                    print(f"Keithley TSP version: {idn}")
                except Exception as e2:
                    print(f"TSP command failed too: {e2}")
            
            inst.close()
            print("Connection closed")
            
        except Exception as e:
            print(f"Failed to connect: {e}")
    except Exception as e:
        print(f"Failed to initialize NI-VISA backend: {e}")

    # Check Linux-specific issues
    if sys.platform.startswith('linux'):
        print("\nChecking Linux GPIB configuration...")
        if os.path.exists('/etc/gpib.conf'):
            print("- Found /etc/gpib.conf")
            # Check if gpib_config has been run
            if os.path.exists('/dev/gpib0'):
                print("- Found /dev/gpib0 device")
                # Check permissions
                try:
                    import stat
                    mode = os.stat('/dev/gpib0').st_mode
                    if mode & stat.S_IROTH and mode & stat.S_IWOTH:
                        print("- /dev/gpib0 has read/write permissions for everyone")
                    else:
                        print("- WARNING: /dev/gpib0 may have restricted permissions")
                except Exception as e:
                    print(f"- Error checking permissions: {e}")
            else:
                print("- WARNING: /dev/gpib0 device not found. Run 'sudo gpib_config'")
        else:
            print("- WARNING: /etc/gpib.conf not found. Linux GPIB driver may not be configured")

    print("\nTroubleshooting tips:")
    print("1. If no resources are found:")
    print("   - Check physical connections (USB, GPIB cables)")
    print("   - Verify instrument power and GPIB address settings")
    print("   - For Linux: run 'sudo gpib_config' and check permissions")
    print("2. If resources are found but connection fails:")
    print("   - Verify GPIB address format (should be GPIB::xx::INSTR where xx is address)")
    print("   - Check for conflicting software using the GPIB interface")
    print("3. If connection works but communication fails:")
    print("   - Try different termination characters")
    print("   - Verify command syntax for your specific instrument model")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_gpib_connection(sys.argv[1])
    else:
        test_gpib_connection()
