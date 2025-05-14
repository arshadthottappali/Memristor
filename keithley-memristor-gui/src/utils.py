def save_data_to_csv(filename, voltages, currents, metadata=None):
    """
    Save voltage and current data to a CSV file with metadata
    
    Args:
        filename (str): Path to save the file
        voltages (list): List of voltage values
        currents (list): List of current values
        metadata (dict, optional): Dictionary of metadata to include in the file header
    """
    import csv
    import datetime

    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Add header with metadata
            writer.writerow(['# Keithley 2602 Memristor Measurement'])
            writer.writerow([f'# Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
            
            # Add custom metadata if provided
            if metadata:
                for key, value in metadata.items():
                    writer.writerow([f'# {key}: {value}'])
                    
            writer.writerow(['# '])  # Empty line to separate metadata from data
            writer.writerow(['Voltage (V)', 'Current (A)'])
            
            # Write data points with scientific notation for precision
            for v, c in zip(voltages, currents):
                writer.writerow([f"{v:.8e}", f"{c:.8e}"])
                
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def validate_numerical_input(value):
    """
    Validates if the input string is a valid numerical value (including negative numbers).
    
    Args:
        value (str): The input string to validate
        
    Returns:
        bool: True if the input is a valid number, False otherwise
    """
    try:
        # Allow for empty string (will use default value)
        if not value.strip():
            return False
        
        # Convert to float to check if it's a valid number (including negative)
        float(value)
        return True
    except ValueError:
        return False

def show_error_message(message):
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Error", message)
    root.destroy()