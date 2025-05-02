from flask import Flask, request, jsonify
import requests
from threading import Thread
import time

app = Flask(__name__)

# Settings
BOT_TOKEN = "8149199696:AAEAu8ommIbD2nhCaBrnATgc9gfW_iQMBmA"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
USERS = {}
REFERRAL_POWER = 70
MINING_TOKENS = ["ETH", "BNB", "USDT"]

# Dummy function to simulate mining
def simulate_mining(user_id):
    while USERS[user_id]["active"]:
        USERS[user_id]["power"] += 1
        time.sleep(3)

def send_message(chat_id, text):
    requests.post(API_URL + "sendMessage", json={"chat_id": chat_id, "text": text})

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.startswith("/start"):
            ref = text.split(" ")[-1] if len(text.split(" ")) > 1 else None
            if chat_id not in USERS:
                USERS[chat_id] = {"power": 100, "active": True, "ref": ref}
                if ref and ref.isdigit() and int(ref) in USERS:
                    USERS[int(ref)]["power"] += REFERRAL_POWER
                    send_message(int(ref), f"Your mining power increased by {REFERRAL_POWER} from a referral!")
                Thread(target=simulate_mining, args=(chat_id,)).start()
            send_message(chat_id, f"Welcome to the miner bot!\nYour current mining power: {USERS[chat_id]['power']}")

        elif text == "/power":
            power = USERS.get(chat_id, {}).get("power", 0)
            send_message(chat_id, f"Your current mining power: {power}")

        elif text == "/withdraw":
            send_message(chat_id, "Withdrawal initiated. You will receive tokens soon!")

    return jsonify({"ok": True})

@app.route("/")
def index():
    return "Bot is running."

# Main function for local dev; Render will use gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
