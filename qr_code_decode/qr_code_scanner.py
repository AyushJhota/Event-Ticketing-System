import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

class QRCodeScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.root.geometry("540x600")
        self.root.configure(bg='black')

        self.capture = None
        self.stop_scan = False
        self.scan_active = False
        self.df = None
        self.selected_column = None

        self.init_ui()

    def init_ui(self):
        self.label_file = ttk.Label(self.root, text="Select Excel File:", font=("Comic Sans MS", 14), foreground='sea green', background='black')
        self.label_file.pack(pady=5)

        self.entry_file_path = ttk.Entry(self.root, width=40, font=("Comic Sans MS", 12), foreground='red')
        self.entry_file_path.pack(pady=5)

        self.button_file = ttk.Button(self.root, text="Browse", command=self.select_file, style='Accent.TButton')
        self.button_file.pack(pady=15)

        self.label_column = ttk.Label(self.root, text="Select Column:", font=("Comic Sans MS", 14), foreground='sea green', background='black')
        self.label_column.pack(pady=5)

        self.column_var = tk.StringVar()
        self.column_menu = ttk.OptionMenu(self.root, self.column_var, "")
        self.column_menu.pack(pady=5)

        self.button_start = ttk.Button(self.root, text="Start Scanning", command=self.start_scan, style='Accent.TButton')
        self.button_start.pack(pady=15)

        self.message_label = tk.Label(self.root, text="", font=("Comic Sans MS", 16), fg="lime", bg="black")
        self.message_label.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_scan, bg="green", fg="white", font=("Comic Sans MS", 12))
        self.next_button.pack(side=tk.LEFT, padx=10, pady=20)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_scan_thread, bg="blue", fg="white", font=("Comic Sans MS", 12))
        self.stop_button.pack(side=tk.RIGHT, padx=10, pady=20)

        self.camera_label = tk.Label(self.root, borderwidth=0, highlightthickness=0)
        self.camera_label.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            self.excel_file = file_path
            self.entry_file_path.delete(0, tk.END)
            self.entry_file_path.insert(0, file_path)
            self.load_columns()

    def load_columns(self):
        try:
            self.df = pd.read_excel(self.excel_file)
            columns = self.df.columns.tolist()
            menu = self.column_menu["menu"]
            menu.delete(0, "end")
            for col in columns:
                menu.add_command(label=col, command=lambda value=col: self.column_var.set(value))
            self.column_var.set(columns[0] if columns else "")
            if "Scanned" not in self.df.columns:
                self.df["Scanned"] = "No"
        except Exception as e:
            messagebox.showerror("Error", f"Error loading columns: {str(e)}")

    def start_scan(self):
        self.selected_column = self.column_var.get()
        if not self.excel_file or not self.selected_column:
            messagebox.showwarning("Warning", "Please select Excel file and column!")
            return
        
        self.capture = cv2.VideoCapture(0)
        self.scan_active = True
        self.update_camera()

    def stop_scan_thread(self):
        self.stop_scan = True
        self.scan_active = False
        if self.capture:
            self.capture.release()
        self.root.destroy()

    def next_scan(self):
        self.scan_active = True

    def update_camera(self):
        if not self.stop_scan:
            if self.scan_active:
                ret, frame = self.capture.read()
                if ret:
                    frame = cv2.resize(frame, (320, 240))
                    decoded_objects = decode(frame)
                    for obj in decoded_objects:
                        data = obj.data.decode('utf-8')
                        access_status, attendee_name = self.check_access(data)
                        self.show_access_message(access_status, attendee_name, data)
                        if access_status.startswith("Welcome"):
                            self.update_excel(data)
                            self.scan_active = False
                            break

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.camera_label.imgtk = imgtk
                    self.camera_label.config(image=imgtk)
                    
            self.root.after(10, self.update_camera)
        else:
            if self.capture:
                self.capture.release()
            cv2.destroyAllWindows()

    def check_access(self, data):
        if self.selected_column not in self.df.columns:
            return "Selected column not found in the Excel file.", None

        if self.selected_column not in self.df.columns:
            return "Selected column not found in the Excel file.", None

        if data in self.df[self.selected_column].values:
            idx = self.df.index[self.df[self.selected_column] == data].tolist()[0]
            if "Scanned" in self.df.columns and self.df.at[idx, "Scanned"] == "Yes":
                return "Sorry, this ticket has already been scanned.", None
            attendee_name = self.df.loc[self.df[self.selected_column] == data, 'Name'].values[0]
            return f"Welcome {attendee_name}!!!", attendee_name
        else:
            return "Sorry Not Allowed,\nAccess Denied.", None

    def update_excel(self, data):
        idx_list = self.df.index[self.df[self.selected_column] == data].tolist()
        if idx_list:
            idx = idx_list[0]
            self.df.at[idx, "Scanned"] = "Yes"
            self.df.to_excel(self.excel_file, index=False)
            self.show_access_message(f"Welcome {self.df.at[idx, 'Name']}!!!\n File updated", self.df.at[idx, 'Name'], data)
        else:
            self.show_access_message("Ticket code not found in Excel file.", None, data)

    def show_access_message(self, message, attendee_name, decoded_data):
        if "Welcome" in message:
            self.message_label.config(text=message, fg="green")
        elif "Excel file updated" in message:
            self.message_label.config(text=message, fg="blue")
        else:
            self.message_label.config(text=message, fg="red")
        
        if decoded_data:
            self.message_label.config(text=f"{message}\nTicket ID: {decoded_data}")

if __name__ == "__main__":
    root = tk.Tk()
    scanner = QRCodeScanner(root)

    style = ttk.Style()
    style.configure('Accent.TButton', foreground='purple', background='magenta', font=('Comic Sans MS', 16, 'italic'))

    root.mainloop()
