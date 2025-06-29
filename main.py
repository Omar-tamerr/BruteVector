# main.py - BruteVector GUI Launcher

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import pyperclip
import itertools

# Wordlist generator embedded

def generate_wordlist(first_names, last_names, specials, extras, birthday, min_len, max_len):
    words = set()

    if birthday:
        parts = birthday.split("-")
        if len(parts) == 3:
            day, month, year = parts
            specials += [day, month, year, day+month+year]

    base = first_names + last_names + extras
    base = [word.lower() for word in base]

    for i in range(1, 4):  # Up to 3 combinations of base
        for combo in itertools.permutations(base, i):
            word = ''.join(combo)
            if min_len <= len(word) <= max_len:
                words.add(word)
            for sp in specials:
                mixed1 = combo[0] + sp + ''.join(combo[1:])
                mixed2 = sp + ''.join(combo)
                if min_len <= len(mixed1) <= max_len:
                    words.add(mixed1)
                if min_len <= len(mixed2) <= max_len:
                    words.add(mixed2)

    return list(words)

def save_wordlist(words, filename):
    with open(filename, "w") as f:
        for word in words:
            f.write(word + "\n")

from modules.ssh_brute import start_ssh_brute
from modules.ftp_brute import start_ftp_brute
from modules.smb_brute import start_smb_brute

class BruteVectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BruteVector - Multi-Protocol Brute Forcer")
        self.root.geometry("800x900")

        self.protocol_var = tk.StringVar(value="ssh")
        self.verbose = tk.BooleanVar(value=False)
        self.brute_mode = tk.StringVar(value="username")
        self.attack_thread = None
        self.stop_flag = threading.Event()

        self.success_creds = []
        self.progress_var = tk.StringVar(value="Progress: 0%")

        self.build_gui()

    def build_gui(self):
        self.root.configure(bg="#1e1e1e")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#1e1e1e", foreground="white", fieldbackground="#333", font=('Segoe UI', 12))

        top_frame = ttk.LabelFrame(self.root, text="Target Configuration")
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Target IP/Host: *", foreground="red").grid(row=0, column=0, padx=5, pady=5)
        self.target_entry = ttk.Entry(top_frame, width=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top_frame, text="Port: *", foreground="red").grid(row=0, column=2, padx=5, pady=5)
        self.port_entry = ttk.Entry(top_frame, width=10)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(top_frame, text="Protocol: *", foreground="red").grid(row=0, column=4, padx=5, pady=5)
        protocol_menu = ttk.Combobox(top_frame, textvariable=self.protocol_var, values=["ssh", "ftp", "smb"], width=10)
        protocol_menu.grid(row=0, column=5, padx=5, pady=5)

        middle_frame = ttk.LabelFrame(self.root, text="Options")
        middle_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(middle_frame, text="🔍 Brute Mode: *", foreground="red").grid(row=0, column=0, padx=5, pady=5)
        mode_menu = ttk.Combobox(middle_frame, textvariable=self.brute_mode, values=["username", "password", "both"], width=12)
        mode_menu.grid(row=0, column=1, padx=5, pady=5)
        mode_menu.bind("<<ComboboxSelected>>", self.toggle_wordlist_fields)

        ttk.Label(middle_frame, text="🔑 Known Value(s) (comma-separated if multiple):").grid(row=0, column=2, padx=5, pady=5)
        self.known_entry = ttk.Entry(middle_frame, width=30)
        self.known_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(middle_frame, text="📄 Username Wordlist (required for username/both):").grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.userlist_path = ttk.Entry(middle_frame, width=40)
        self.userlist_path.grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(middle_frame, text="Browse", command=lambda: self.browse_list(self.userlist_path)).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(middle_frame, text="📄 Password Wordlist (required for password/both):").grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.passlist_path = ttk.Entry(middle_frame, width=40)
        self.passlist_path.grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(middle_frame, text="Browse", command=lambda: self.browse_list(self.passlist_path)).grid(row=2, column=3, padx=5, pady=5)

        ttk.Checkbutton(middle_frame, text="📢 Verbose Output", variable=self.verbose).grid(row=3, column=0, padx=5, pady=5)

        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(action_frame, text="▶️ Start Attack", command=self.start_attack).pack(side="left", padx=5)
        ttk.Button(action_frame, text="⛔ Stop Attack", command=self.stop_attack).pack(side="left", padx=5)
        ttk.Button(action_frame, text="🛠️ Generate Wordlist", command=self.generate_wordlist_window).pack(side="left", padx=5)
        ttk.Button(action_frame, text="🔄 Reset Fields", command=self.reset_fields).pack(side="left", padx=5)
        ttk.Button(action_frame, text="📋 Copy Output", command=self.copy_output).pack(side="right", padx=5)
        ttk.Button(action_frame, text="💾 Save Output", command=self.save_output_to_file).pack(side="right", padx=5)

        self.progress_label = ttk.Label(self.root, textvariable=self.progress_var)
        self.progress_label.pack(pady=5)

        self.log_text = tk.Text(self.root, height=20, bg="#111", fg="#0f0", font=('Courier', 12))
        self.log_text.pack(fill="both", padx=10, pady=10, expand=True)

        self.toggle_wordlist_fields()

    def toggle_wordlist_fields(self, event=None):
        mode = self.brute_mode.get()
        self.userlist_path.configure(state="normal" if mode in ["username", "both"] else "disabled")
        self.passlist_path.configure(state="normal" if mode in ["password", "both"] else "disabled")

    def start_attack(self):
        self.log("[+] Attack started...")
        # TODO: actual attack logic

    def stop_attack(self):
        self.stop_flag.set()
        self.log("[!] Attack stopped by user.")

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def browse_list(self, target_entry):
        path = filedialog.askopenfilename(title="Select Wordlist", filetypes=[("Text Files", "*.txt")])
        if path:
            target_entry.delete(0, tk.END)
            target_entry.insert(0, path)

    def generate_wordlist_window(self):
        win = tk.Toplevel(self.root)
        win.title("Generate Wordlist")
        win.geometry("420x600")
        win.configure(bg="#1e1e1e")

        style = ttk.Style(win)
        style.configure("TLabel", foreground="white", background="#1e1e1e", font=('Segoe UI', 12))
        style.configure("TEntry", foreground="white", background="#333", fieldbackground="#333", font=('Segoe UI', 12))
        style.configure("TButton", font=('Segoe UI', 12))

        ttk.Label(win, text="📛 First Names (comma-separated, optional):").pack(pady=5)
        fn_entry = ttk.Entry(win, width=50)
        fn_entry.pack(pady=5)

        ttk.Label(win, text="👨 Last Names (comma-separated, optional):").pack(pady=5)
        ln_entry = ttk.Entry(win, width=50)
        ln_entry.pack(pady=5)

        ttk.Label(win, text="✨ Special Characters (optional):").pack(pady=5)
        sp_entry = ttk.Entry(win, width=50)
        sp_entry.pack(pady=5)

        ttk.Label(win, text="🎂 Birthday (DD-MM-YYYY, optional):").pack(pady=5)
        bd_entry = ttk.Entry(win, width=50)
        bd_entry.pack(pady=5)

        ttk.Label(win, text="📝 Extra Words (comma-separated, optional):").pack(pady=5)
        extra_entry = ttk.Entry(win, width=50)
        extra_entry.pack(pady=5)

        ttk.Label(win, text="🔢 Min Length:").pack(pady=5)
        min_entry = ttk.Entry(win, width=10)
        min_entry.insert(0, "4")
        min_entry.pack(pady=5)

        ttk.Label(win, text="🔢 Max Length:").pack(pady=5)
        max_entry = ttk.Entry(win, width=10)
        max_entry.insert(0, "16")
        max_entry.pack(pady=5)

        ttk.Label(win, text="💾 Filename to Save As:").pack(pady=5)
        file_entry = ttk.Entry(win, width=50)
        file_entry.insert(0, "generated_wordlist.txt")
        file_entry.pack(pady=5)

        ttk.Button(win, text="🚀 Generate Wordlist", command=lambda: self.generate_and_save_wordlist(
            fn_entry.get(), ln_entry.get(), sp_entry.get(), extra_entry.get(), bd_entry.get(),
            min_entry.get(), max_entry.get(), file_entry.get(), win)).pack(pady=20)

    def generate_and_save_wordlist(self, fn, ln, sp, extra, birthday, min_len, max_len, filename, window):
        fns = [x.strip() for x in fn.split(",") if x.strip()]
        lns = [x.strip() for x in ln.split(",") if x.strip()]
        sps = [x.strip() for x in sp.split(",") if x.strip()]
        extras = [x.strip() for x in extra.split(",") if x.strip()]
        try:
            min_len = int(min_len)
            max_len = int(max_len)
        except ValueError:
            messagebox.showerror("Error", "Min/Max length must be integers.")
            return
        if not filename:
            filename = "generated_wordlist.txt"
        words = generate_wordlist(fns, lns, sps, extras, birthday.strip(), min_len, max_len)
        save_wordlist(words, filename)
        messagebox.showinfo("Success", f"Wordlist saved to {filename}")
        window.destroy()

    def reset_fields(self):
        self.target_entry.delete(0, tk.END)
        self.port_entry.delete(0, tk.END)
        self.userlist_path.delete(0, tk.END)
        self.passlist_path.delete(0, tk.END)
        self.known_entry.delete(0, tk.END)
        self.log_text.delete("1.0", tk.END)
        self.progress_var.set("Progress: 0%")

    def copy_output(self):
        pyperclip.copy(self.log_text.get("1.0", tk.END))
        messagebox.showinfo("Copied", "Output copied to clipboard!")

    def save_output_to_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "w") as f:
                f.write(self.log_text.get("1.0", tk.END))
            messagebox.showinfo("Saved", f"Output saved to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BruteVectorApp(root)
    root.mainloop()

