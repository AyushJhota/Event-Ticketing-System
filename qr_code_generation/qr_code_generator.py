import os
import pandas as pd
import hashlib
import qrcode
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x600")  # Set initial size of the window
        self.root.configure(bg='black')  # Set background color of the window

        # Define custom fonts
        self.title_font = ("Comic Sans MS", 18, "bold italic")
        self.label_font = ("Comic Sans MS", 14)
        self.button_font = ("Comic Sans MS", 12)
        self.entry_font = ("Comic Sans MS", 12)

        self.label = ttk.Label(root, text="Generate QR Codes", font=self.title_font, foreground='sky blue', background='black')
        self.label.pack(pady=20)

        self.label_file = ttk.Label(root, text="Select Excel File:", font=self.label_font, foreground='sea green', background='black')
        self.label_file.pack(pady=5)

        self.entry_file_path = ttk.Entry(root, width=40, font=self.entry_font, foreground='red')
        self.entry_file_path.pack(pady=5)

        self.button_file = ttk.Button(root, text="Browse", command=self.select_file, style='Accent.TButton')
        self.button_file.pack(pady=15)

        self.label_column = ttk.Label(root, text="Select Column:", font=self.label_font, foreground='sea green', background='black')
        self.label_column.pack(pady=5)

        self.column_var = tk.StringVar()
        self.column_menu = ttk.OptionMenu(root, self.column_var, "")
        self.column_menu.pack(pady=5)

        self.label_folder = ttk.Label(root, text="Select Output Folder:", font=self.label_font, foreground='sea green', background='black')
        self.label_folder.pack(pady=5)

        self.entry_folder_path = ttk.Entry(root, width=40, font=self.entry_font, foreground='red')
        self.entry_folder_path.pack(pady=5)

        self.button_folder = ttk.Button(root, text="Browse", command=self.select_folder, style='Accent.TButton')
        self.button_folder.pack(pady=5)

        self.button_generate = ttk.Button(root, text="Generate QR Codes", command=self.generate_qr_codes, style='Accent.TButton')
        self.button_generate.pack(pady=5)

        # Initialize variables
        self.excel_file = ""
        self.output_folder = ""
        self.df = None

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
        except Exception as e:
            messagebox.showerror("Error", f"Error loading columns: {str(e)}")

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder = folder_path
            self.entry_folder_path.delete(0, tk.END)
            self.entry_folder_path.insert(0, folder_path)

    def generate_ticket_code(self, data):
        hashed_id = hashlib.sha256(data.encode()).hexdigest()
        return hashed_id[:8]

    def generate_qr_code(self, data, name):
        ticket_code = self.generate_ticket_code(data)
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(ticket_code)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_location = os.path.join(self.output_folder, f"{name}.png")
        qr_img.save(qr_location)
        return ticket_code, qr_location

    def generate_qr_codes(self):
        if not self.excel_file or not self.output_folder:
            messagebox.showwarning("Warning", "Please select Excel file and output folder!")
            return
        
        selected_column = self.column_var.get()
        if not selected_column:
            messagebox.showwarning("Warning", "Please select a column!")
            return

        try:
            df = self.df
            df['Ticket Code'] = ""
            df['QR Location'] = ""
            for index, row in df.iterrows():
                data = str(row[selected_column])
                name = row['Name']
                ticket_code, qr_location = self.generate_qr_code(data, name)
                df.at[index, 'Ticket Code'] = ticket_code
                df.at[index, 'QR Location'] = qr_location
            df.to_excel(self.excel_file, index=False)
            messagebox.showinfo("Success", "QR codes generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating QR codes: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    
    # Define custom style for buttons (Accent color scheme)
    style = ttk.Style()
    style.configure('Accent.TButton', foreground='purple', background='magenta', font=('Comic Sans MS', 16, 'italic'))

    root.mainloop()
