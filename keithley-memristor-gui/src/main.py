import tkinter as tk
from tkinter import messagebox
from gui import KeithleyMemristorGUI

def main():
    root = tk.Tk()
    root.title("Keithley Memristor GUI")
    
    app = KeithleyMemristorGUI(root)
    
    try:
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()