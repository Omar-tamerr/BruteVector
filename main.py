# BruteVector - Full Project Version

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os

from wordlist_generator.generator import generate_wordlist, save_wordlist
from modules.http_brute import start_http_brute
from modules.ssh_brute import start_ssh_brute
from modules.ftp_brute import start_ftp_brute
from modules.smb_brute import start_smb_brute

class BruteVectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BruteVector - Multi-Protocol Brute Forcer")
        self.root.geometry("800x700")

        self.protocol_var = tk.StringVar(value="http")
        self.verbose = tk.BooleanVar(value=False)

        self.build_gui()

    def build_gui(self):
        top_frame = ttk.LabelFrame(self.root, text="Target Configuration")
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Target IP/Host:").grid(row=0, column=0, padx=5, pady=5)
        self.target_entry = ttk.Entry(top_frame, width=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top_frame, text="Port:").grid(row=0, column==2, padx=5, pady=5)
        self.port_entry = ttk.Entry(top_frame, width=10)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(top_frame, text="Protocol:").grid(row=0, column=4, padx=5, pady=5)
        protocol_menu = ttk.Combobox(top_frame, textvariable=self.protocol_var, values=["http", "ssh", "ftp", "smb"], width=10)
        protocol_menu.grid(row=0, column=5, padx=5, pady=5)

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

        http_frame = ttk.LabelFrame(self.root, text="HTTP Form Settings")
        http_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(http_frame, text="Username Field Name:").grid(row=0, column=0, padx=5, pady=5)
        self.field_user_entry = ttk.Entry(http_frame, width=20)
        self.field_user_entry.insert(0, "username")
        self.field_user_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(http_frame, text="Password Field Name:").grid(row=0, column=2, padx=5, pady=5)
        self.field_pass_entry = ttk.Entry(http_frame, width=20)
        self.field_pass_entry.insert(0, "password")
        self.field_pass_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(http_frame, text="Failure Phrase:").grid(row=1, column=0, padx=5, pady=5)
        self.fail_phrase_entry = ttk.Entry(http_frame, width=40)
        self.fail_phrase_entry.insert(0, "Invalid username or password")
        self.fail_phrase_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(action_frame, text="Start Attack", command=self.start_attack).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Generate Wordlist", command=self.generate_wordlist_window).pack(side="left", padx=5)

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

        if protocol == "http":
            field_user = self.field_user_entry.get()
            field_pass = self.field_pass_entry.get()
            fail_phrase = self.fail_phrase_entry.get()
            threading.Thread(target=start_http_brute, args=(
                target, port, user, wordlist, field_user, field_pass, fail_phrase,
                self.verbose.get(), self.log)).start()

        elif protocol == "ssh":
            threading.Thread(target=start_ssh_brute, args=(
                target, port, user, wordlist, self.verbose.get(), self.log)).start()

        elif protocol == "ftp":
            threading.Thread(target=start_ftp_brute, args=(
                target, port, user, wordlist, self.verbose.get(), self.log)).start()

        elif protocol == "smb":
            threading.Thread(target=start_smb_brute, args=(
                target, port, user, wordlist, self.verbose.get(), self.log)).start()

        else:
            self.log(f"[!] Protocol '{protocol}' not supported.")

    def generate_wordlist_window(self):
        win = tk.Toplevel(self.root)
        win.title("Generate Wordlist")
        win.geometry("400x400")

        ttk.Label(win, text="First Names (comma-separated):").pack(pady=5)
        fn_entry = ttk.Entry(win, width=50)
        fn_entry.pack(pady=5)

        ttk.Label(win, text="Last Names (comma-separated):").pack(pady=5)
        ln_entry = ttk.Entry(win, width=50)
        ln_entry.pack(pady=5)

        ttk.Label(win, text="Special Characters (comma-separated):").pack(pady=5)
        sp_entry = ttk.Entry(win, width=50)
        sp_entry.pack(pady=5)

        ttk.Label(win, text="Max Words to Generate:").pack(pady=5)
        count_entry = ttk.Entry(win, width=20)
        count_entry.insert(0, "100")
        count_entry.pack(pady=5)

        def generate_and_save():
            fns = [x.strip() for x in fn_entry.get().split(",") if x.strip()]
            lns = [x.strip() for x in ln_entry.get().split(",") if x.strip()]
            sps = [x.strip() for x in sp_entry.get().split(",") if x.strip()]
            try:
                count = int(count_entry.get())
            except ValueError:
                count = 100

            if not fns or not lns:
                messagebox.showerror("Input Error", "Please enter at least one first and one last name.")
                return

            wl = generate_wordlist(fns, lns, sps, count)
            save_wordlist(wl)
            messagebox.showinfo("Success", f"Wordlist saved to generated_wordlist.txt")
            self.wordlist_path.delete(0, tk.END)
            self.wordlist_path.insert(0, "generated_wordlist.txt")
            win.destroy()

        ttk.Button(win, text="Generate", command=generate_and_save).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = BruteVectorApp(root)
    root.mainloop()

