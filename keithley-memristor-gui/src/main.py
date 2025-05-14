import tkinter as tk
from tkinter import messagebox
from gui import ApplicationGUI

def main():
    root = tk.Tk()
    root.title("Keithley Memristor GUI")
    
    app = ApplicationGUI(root)
    
    try:
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()