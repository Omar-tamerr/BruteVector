# BruteVector

🚀 **BruteVector** is a powerful and beginner-friendly GUI tool designed to perform brute-force attacks on multiple network protocols. Whether you're a penetration tester, red teamer, or security enthusiast, this tool can help you audit login surfaces quickly and visually.

---

## ✨ Features

- 🔐 **Supports 4 major protocols**:
  - HTTP Form-based login (customizable fields)
  - SSH (via Paramiko)
  - FTP (via ftplib)
  - SMB (via smbprotocol)

- 🧠 **Smart Wordlist Generator**:
  - Combines first names, last names, special characters
  - User-defined output size (e.g., 24, 100 passwords)

- 🖥️ **User-Friendly GUI**:
  - Built with Tkinter
  - Form fields for targets, port, wordlists, protocol type
  - Verbose logging toggle
  - Real-time log output panel

- 🪵 **Verbose Logging**:
  - See which credentials succeed or fail as they are tried

- 📦 Modular codebase for easy extension

---

## 🛠️ Installation

```bash
git clone https://github.com/Omar-tamerr/BruteVector.git
cd BruteVector
pip install -r requirements.txt
python3 main.py
```

---

## 📸 Screenshots
_(Coming soon)_

---

## 🎯 Example Usage

### 1. Brute-force an HTTP login form:
- Target: `192.168.1.10`
- Port: `80`
- Protocol: `http`
- Wordlist: `generated_wordlist.txt`
- Username field: `user`
- Password field: `pass`
- Failure phrase: `Invalid credentials`

### 2. Brute-force an SSH login:
- Target: `10.10.10.100`
- Port: `22`
- Protocol: `ssh`
- Username: `admin`
- Wordlist: `passwords.txt`

---

## 🧪 Wordlist Generator Example

1. Click "Generate Wordlist" in the GUI
2. Enter:
   - First Names: `omar, ahmed`
   - Last Names: `tamer, khaled`
   - Special Characters: `!, @, #`
   - Max Size: `50`
3. Click **Generate** → Saves to `generated_wordlist.txt`

---

## 📁 Project Structure

```
BruteVector/
├── main.py                    # GUI Application
├── requirements.txt          # Dependencies
├── README.md                 # You’re reading this
├── LICENSE                   # MIT License
├── modules/
│   ├── http_brute.py         # HTTP brute logic
│   ├── ssh_brute.py          # SSH brute logic
│   ├── ftp_brute.py          # FTP brute logic
│   └── smb_brute.py          # SMB brute logic
└── wordlist_generator/
    └── generator.py          # Wordlist creation logic
```

---

## ✅ Requirements
- Python 3.7+
- Tkinter (pre-installed)
- `paramiko` for SSH
- `requests` for HTTP
- `smbprotocol` for SMB

Install them all:
```bash
pip install -r requirements.txt
```

---

## 📜 License

MIT License © 2025 Omar Tamer

---

## 🙌 Contributing
Pull requests are welcome! Found a bug or want a new feature? Feel free to open an issue or PR.

---

## 🌍 Author
**Omar Tamer** — [GitHub](https://github.com/Omar-tamerr)

Happy cracking responsibly! 🔐💻

