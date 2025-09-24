import os
import requests

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
    """Checks the LeetCode contest page for redeemable LeetCoins."""
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
        page_content = response.text.lower() # Convert to lower case for easy searching

        # Keywords to look for that indicate LeetCoins are available
        if "redeem" in page_content or "leetcodes" in page_content:
            print("Success! LeetCoins might be available.")
            message = f"🪙 **LeetCoins might be available!**\n\nCheck the contest page now:\n{LEETCODE_CONTEST_URL}"
            send_telegram_message(message)
        else:
            print("No LeetCoins found on the page this time.")

    except Exception as e:
        print(f"An error occurred while fetching the LeetCode page: {e}")

if __name__ == "__main__":
    check_for_leetcoins()
