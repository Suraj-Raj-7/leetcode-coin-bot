import os
import requests
from bs4 import BeautifulSoup

# --- Configuration (Loaded from GitHub Secrets) ---
LEETCODE_COOKIE = os.environ.get("LEETCODE_COOKIE")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

LEETCODE_CONTEST_URL = "https://leetcode.com/contest/"

def send_telegram_message(message):
    """Sends a message to your Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram notification sent successfully!")
        else:
            print(f"Failed to send notification: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_for_leetcoins():
    """Checks the LeetCode contest page for the reward element."""
    if not all([LEETCODE_COOKIE, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
        print("Error: Required secrets are not set. Aborting.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie": LEETCODE_COOKIE,
    }

    print("Checking LeetCode contest page...")
    try:
        response = requests.get(LEETCODE_CONTEST_URL, headers=headers)
        response.raise_for_status()
        page_content = response.text

        soup = BeautifulSoup(page_content, 'html.parser')

        # Find the container div by the unique positional class you confirmed.
        # <-- THIS IS THE KEY LINE YOU CONFIRMED
        reward_element = soup.find('div', class_='z-base-1')

        if reward_element:
            # Get the text from the button to include in the message
            reward_text = reward_element.get_text(strip=True)
            print(f"Success! Found reward element with text: '{reward_text}'")
            message = f"🪙 **A special reward might be available on LeetCode!**\n\nButton text: *\"{reward_text}\"*\n\nCheck the contest page now:\n{LEETCODE_CONTEST_URL}"
            send_telegram_message(message)
        else:
            print("No special reward element found on the page this time.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_for_leetcoins()
