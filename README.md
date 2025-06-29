# 🛠️ BruteVector - GUI-Based Multi-Protocol Brute Forcer

🚀 **BruteVector** is a powerful and beginner-friendly GUI tool designed to perform brute-force attacks on SSH, FTP, and SMB protocols. Whether you're a penetration tester, red teamer, or security enthusiast, this tool helps you audit login surfaces quickly, visually, and responsibly.

---

## ✨ Features

- 🔐 **Supports 3 protocols**:
  - SSH (via `paramiko`)
  - FTP (via `ftplib`)
  - SMB (via `smbprotocol`)

- 🧠 **Smart Wordlist Generator**:
  - Combines first/last names, birthday, special characters, extra words
  - Allows control over **min/max password length**
  - Generates all realistic combinations and permutations

- 🖥️ **User-Friendly GUI**:
  - Built with Tkinter (dark hacker-themed)
  - Select protocol, port, mode (username / password / both)
  - Browse or generate custom wordlists
  - Copy or save brute-force output

- 🧪 **Brute Modes**:
  - Username brute with known password
  - Password brute with known username
  - Full login brute (username + password list)

- 📋 **Live Output & Verbose Logging**
  - Track progress and results in real time
  - Optional verbose toggle

---

## 🛠️ Installation

```bash
git clone https://github.com/Omar-tamerr/BruteVector.git
cd BruteVector
pip install -r requirements.txt
python3 main.py
```

---

## 📁 Project Structure

```
BruteVector/
├── main.py                    # GUI Application
├── requirements.txt           # Dependencies
├── README.md                  # You're reading this
├── LICENSE                    # MIT License
├── modules/
│   ├── ssh_brute.py           # SSH brute logic
│   ├── ftp_brute.py           # FTP brute logic
│   └── smb_brute.py           # SMB brute logic
└── wordlist_generator/
    └── generator.py           # Wordlist generation logic
```

---

## 🎯 Example Usage

### ✅ Brute-force SSH login:
- Target: `10.10.10.100`
- Port: `22`
- Mode: `password`
- Known Username: `admin`
- Password Wordlist: `rockyou.txt`

### ✅ Brute-force FTP login:
- Target: `192.168.1.5`
- Port: `21`
- Mode: `both`
- Username Wordlist: `users.txt`
- Password Wordlist: `generated_wordlist.txt`

---

## 🧠 Wordlist Generator

1. Click **🛠️ Generate Wordlist**
2. Input (any optional):
   - 📛 First Names: `omar,ahmed`
   - 👨 Last Names: `tamer,khaled`
   - ✨ Special Chars: `!,@,#`
   - 🎂 Birthday: `05-01-2001`
   - 📝 Extra Words: `admin,root,egypt`
   - 🔢 Min Length: `4`
   - 🔢 Max Length: `12`
   - 💾 Filename: `custom.txt`
3. Click **🚀 Generate Wordlist**  
✔️ Wordlist saved in project directory.

---

## ✅ Requirements

- Python 3.8+
- Tkinter (pre-installed on most systems)
- `paramiko` — SSH
- `pysmb` — SMB
- `pyperclip` — Copy to clipboard

Install them all with:

```bash
pip install -r requirements.txt
```

---

## 📸 Screenshots

_(Coming soon)_

---

## 📜 License

MIT License © 2025 Omar Tamer

---

## 🙌 Contributing

Pull requests are welcome!  
Found a bug or want a new feature? Open an issue or PR!

---

## 🌍 Author

**Omar Tamer**  
🔗 GitHub: [github.com/Omar-tamerr](https://github.com/Omar-tamerr)

---

Happy hacking responsibly! 💻🔐

