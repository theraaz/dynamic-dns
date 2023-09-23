import os
import requests
from time import sleep
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define constants using environment variables
API_URL = "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}"
PUBLIC_IP_URL = "http://api.ipify.org"
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
DNS_RECORD_ID = os.getenv("CLOUDFLARE_DNS_RECORD_ID")
DOMAIN = os.getenv("DOMAIN")


def get_public_ip():
    try:
        response = requests.get(PUBLIC_IP_URL)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error getting public IP: {e}")
        return None


def get_cloudflare_record():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(API_URL.format(zone_id=ZONE_ID, dns_record_id=DNS_RECORD_ID), headers=headers)
        response.raise_for_status()
        return response.json()['result']['content']
    except requests.RequestException as e:
        print(f"Error getting Cloudflare A record: {e}")
        return None


def update_cloudflare_record(new_ip):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "type": "A",
        "name": DOMAIN,
        "content": new_ip,
        "proxied": True,
    }

    try:
        response = requests.put(API_URL.format(zone_id=ZONE_ID, dns_record_id=DNS_RECORD_ID), headers=headers, json=data)
        response.raise_for_status()
        print(f"Successfully updated Cloudflare A record to {new_ip}")
    except requests.RequestException as e:
        print(f"Error updating Cloudflare A record: {e}")


def main():
    print("init..")
    while True:
        public_ip = get_public_ip()
        if public_ip:
            cloudflare_ip = get_cloudflare_record()
            if cloudflare_ip and public_ip != cloudflare_ip:
                print(f"Public IP changed from {cloudflare_ip} to {public_ip}. updating for DNS A record now")
                update_cloudflare_record(public_ip)
        sleep(300)  # Sleep for 5 minutes


if __name__ == "__main__":
    main()
