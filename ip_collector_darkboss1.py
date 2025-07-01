import socket
import requests
from datetime import datetime

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def get_public_ip():
    try:
        public_ip = requests.get('https://api.ipify.org').text
        return public_ip
    except requests.exceptions.RequestException as e:
        return f"Error getting public IP: {e}"

def save_to_file(local_ip, public_ip):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("ip_log.txt", "a") as file:
        file.write(f"\n--- {now} ---\n")
        file.write(f"Local IP  : {local_ip}\n")
        file.write(f"Public IP : {public_ip}\n")

def main():
    print("Collecting IP addresses...\n")
    local_ip = get_local_ip()
    public_ip = get_public_ip()

    print(f"Local IP Address : {local_ip}")
    print(f"Public IP Address: {public_ip}")

    save_to_file(local_ip, public_ip)
    print("\nIP addresses saved to ip_log.txt")

if __name__ == "__main__":
    main()
