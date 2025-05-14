def save_data_to_csv(filename, voltages, currents):
    import csv

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Voltage (V)', 'Current (A)'])
        for v, c in zip(voltages, currents):
            writer.writerow([v, c])

def validate_numerical_input(value):
    try:
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