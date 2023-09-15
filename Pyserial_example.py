import tkinter as tk
from tkinter import ttk
import serial

class SerialCommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Communication")
        
        self.serial_port = ttk.Combobox(root, values=self.get_serial_ports())
        self.serial_port.set("Select Port")
        self.serial_port.pack(pady=10)
        
        self.connect_button = tk.Button(root, text="Connect", command=self.connect_serial)
        self.connect_button.pack(pady=5)
        
        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.pack(pady=5)
        
        self.serial = None

    def get_serial_ports(self):
        # Return a list of available serial ports
        # You may need to adjust this based on your operating system
        return ["COM1", "COM2", "COM3", "/dev/ttyUSB0", "/dev/ttyS0"]
    
    def connect_serial(self):
        port = self.serial_port.get()
        try:
            self.serial = serial.Serial(port, baudrate=9600, timeout=1)
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
        except serial.SerialException as e:
            print("Error:", e)
        
    def disconnect_serial(self):
        if self.serial:
            self.serial.close()
            self.serial = None
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialCommunicationApp(root)
    root.mainloop()