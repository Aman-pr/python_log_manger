import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext


class LogManager:
    def __init__(self, filename='application.log'):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("Log file created on {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def write_log(self, message):
        with open(self.filename, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write("[{}] {}\n".format(timestamp, message))

    def read_logs(self):
        with open(self.filename, 'r') as f:
            logs = f.readlines()
        return logs

    def clear_logs(self):
        with open(self.filename, 'w') as f:
            f.write("Log file cleared on {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def delete_old_logs(self, days):
        current_time = datetime.now()
        with open(self.filename, 'r') as f:
            logs = f.readlines()

        with open(self.filename, 'w') as f:
            for log in logs:
                log_time_str = log.split(']')[0][1:]  
                log_time = datetime.strptime(log_time_str, '%Y-%m-%d %H:%M:%S')
                if (current_time - log_time).days <= days:
                    f.write(log)


class LogManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Manager")
        self.root.geometry("600x500")
        self.root.config(bg="#2E2E2E")

        self.log_manager = LogManager()

        # Frame for log display
        self.log_frame = tk.Frame(root, bg="#2E2E2E")
        self.log_frame.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(self.log_frame, width=70, height=20, bg="#1E1E1E", fg="white")
        self.log_text.pack()

        # Frame for log input and buttons
        self.input_frame = tk.Frame(root, bg="#2E2E2E")
        self.input_frame.pack(pady=10)

        self.message_label = tk.Label(self.input_frame, text="Log Message:", bg="#2E2E2E", fg="white")
        self.message_label.grid(row=0, column=0)

        self.entry = tk.Entry(self.input_frame, width=40)
        self.entry.grid(row=0, column=1)

        self.write_button = tk.Button(self.input_frame, text="Write Log", command=self.write_log, bg="#4CAF50", fg="white")
        self.write_button.grid(row=0, column=2)

        # Frame for additional log management
        self.management_frame = tk.Frame(root, bg="#2E2E2E")
        self.management_frame.pack(pady=10)

        self.read_button = tk.Button(self.management_frame, text="Read Logs", command=self.read_logs, bg="#2196F3", fg="white")
        self.read_button.grid(row=0, column=0)

        self.clear_button = tk.Button(self.management_frame, text="Clear Logs", command=self.clear_logs, bg="#F44336", fg="white")
        self.clear_button.grid(row=0, column=1)

        self.days_label = tk.Label(self.management_frame, text="Delete Logs Older Than (days):", bg="#2E2E2E", fg="white")
        self.days_label.grid(row=1, column=0)

        self.days_entry = tk.Entry(self.management_frame, width=5)
        self.days_entry.grid(row=1, column=1)
        self.days_entry.insert(0, "Days")

        self.delete_button = tk.Button(self.management_frame, text="Delete Old Logs", command=self.delete_old_logs, bg="#FF9800", fg="white")
        self.delete_button.grid(row=1, column=2)

    def write_log(self):
        message = self.entry.get()
        if message:
            self.log_manager.write_log(message)
            self.entry.delete(0, tk.END)
            messagebox.showinfo("Info", "Log written!")
        else:
            messagebox.showwarning("Warning", "Please enter a log message.")

    def read_logs(self):
        self.log_text.delete(1.0, tk.END)  
        logs = self.log_manager.read_logs()
        self.log_text.insert(tk.END, ''.join(logs))

    def clear_logs(self):
        self.log_manager.clear_logs()
        self.log_text.delete(1.0, tk.END)
        messagebox.showinfo("Info", "Log file cleared.")

    def delete_old_logs(self):
        days = self.days_entry.get()
        if days.isdigit():
            days = int(days)
            self.log_manager.delete_old_logs(days)
            self.log_text.delete(1.0, tk.END)
            messagebox.showinfo("Info", f"Old logs deleted, keeping logs from the last {days} days.")
        else:
            messagebox.showwarning("Warning", "Please enter a valid number of days.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = LogManagerGUI(root)
    root.mainloop()

