
import socket
import requests
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
EMAIL_SENDER = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVER = "receiver_email@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

CSV_FILE = "ip_data.csv"

def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unavailable"

def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return response.get('city', 'N/A'), response.get('region', 'N/A'), response.get('country', 'N/A'), response.get('org', 'N/A')
    except:
        return 'N/A', 'N/A', 'N/A', 'N/A'

def save_to_csv(local_ip, public_ip, city, region, country, org):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = ["Timestamp", "Local IP", "Public IP", "City", "Region", "Country", "ISP/Org"]

    try:
        with open(CSV_FILE, "x", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    except FileExistsError:
        pass

    with open(CSV_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, local_ip, public_ip, city, region, country, org])

def send_email_report(local_ip, public_ip, city, region, country, org):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = "🔔 IP Collector Report"
    body = f"""
    Timestamp: {now}
    Local IP : {local_ip}
    Public IP: {public_ip}
    Location : {city}, {region}, {country}
    ISP/Org  : {org}
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    print("🔎 Collecting IP and location info...")

    local_ip = get_local_ip()
    public_ip = get_public_ip()
    city, region, country, org = get_geolocation(public_ip)

    print(f"Local IP : {local_ip}")
    print(f"Public IP: {public_ip}")
    print(f"Location : {city}, {region}, {country}")
    print(f"Org/ISP  : {org}")

    save_to_csv(local_ip, public_ip, city, region, country, org)
    send_email_report(local_ip, public_ip, city, region, country, org)
    print(f"✅ Data saved to {CSV_FILE}")

if __name__ == "__main__":
    main()
