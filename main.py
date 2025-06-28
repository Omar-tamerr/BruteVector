# BruteVector - Main GUI Shell (Tkinter)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os

# Placeholder imports for each module
# from modules.http_brute import start_http_brute
# from modules.ssh_brute import start_ssh_brute
# from modules.ftp_brute import start_ftp_brute
# from modules.smb_brute import start_smb_brute
# from wordlist_generator import generate_wordlist

class BruteVectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BruteVector - Multi-Protocol Brute Forcer")
        self.root.geometry("800x600")

        self.protocol_var = tk.StringVar(value="http")
        self.verbose = tk.BooleanVar(value=False)

        self.build_gui()

    def build_gui(self):
        # Top Frame for target settings
        top_frame = ttk.LabelFrame(self.root, text="Target Configuration")
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Target IP/Host:").grid(row=0, column=0, padx=5, pady=5)
        self.target_entry = ttk.Entry(top_frame, width=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5)
        self.port_entry = ttk.Entry(top_frame, width=10)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(top_frame, text="Protocol:").grid(row=0, column=4, padx=5, pady=5)
        protocol_menu = ttk.Combobox(top_frame, textvariable=self.protocol_var, values=["http", "ssh", "ftp", "smb"], width=10)
        protocol_menu.grid(row=0, column=5, padx=5, pady=5)

        # Mid Frame for wordlist + verbose
        middle_frame = ttk.LabelFrame(self.root, text="Options")
        middle_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(middle_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(middle_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(middle_frame, text="Wordlist:").grid(row=0, column=2, padx=5, pady=5)
        self.wordlist_path = ttk.Entry(middle_frame, width=40)
        self.wordlist_path.grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(middle_frame, text="Browse", command=self.browse_wordlist).grid(row=0, column=4, padx=5, pady=5)

        ttk.Checkbutton(middle_frame, text="Verbose Output", variable=self.verbose).grid(row=1, column=0, padx=5, pady=5)

        # Action buttons
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(action_frame, text="Start Attack", command=self.start_attack).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Generate Wordlist", command=self.generate_wordlist_window).pack(side="left", padx=5)

        # Log output
        self.log_text = tk.Text(self.root, height=20)
        self.log_text.pack(fill="both", padx=10, pady=10, expand=True)

    def browse_wordlist(self):
        path = filedialog.askopenfilename(title="Select Wordlist", filetypes=[("Text Files", "*.txt")])
        if path:
            self.wordlist_path.delete(0, tk.END)
            self.wordlist_path.insert(0, path)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def start_attack(self):
        target = self.target_entry.get()
        port = self.port_entry.get()
        user = self.username_entry.get()
        wordlist = self.wordlist_path.get()
        protocol = self.protocol_var.get()

        if not all([target, port, user, wordlist]):
            messagebox.showerror("Error", "Please fill all required fields.")
            return

        self.log(f"[+] Starting {protocol.upper()} brute-force on {target}:{port} with user '{user}'")

        # This will later dispatch the correct brute module
        # threading.Thread(target=start_http_brute, args=(target, port, user, wordlist, self.verbose.get(), self.log)).start()

    def generate_wordlist_window(self):
        messagebox.showinfo("Coming Soon", "Wordlist generator UI will be added next.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BruteVectorApp(root)
    root.mainloop()
