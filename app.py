from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# Simulated database
users = {}

@app.route('/')
def home():
    return "<h1>Welcome to Mining Power Bot</h1><p>Connect via Telegram to start mining.</p>"

@app.route('/start/<user_id>')
def start(user_id):
    if user_id not in users:
        users[user_id] = {
            'mining_power': 100,
            'referrals': 0
        }
    return redirect(f'/dashboard/{user_id}')

@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    user = users.get(user_id)
    if not user:
        return "User not found", 404
    return f"<h2>Welcome User {user_id}</h2><p>Mining Power: {user['mining_power']}</p><p>Referrals: {user['referrals']}</p><br><a href='/withdraw/{user_id}'>Withdraw</a>"

@app.route('/refer/<referrer_id>/<new_user_id>')
def refer(referrer_id, new_user_id):
    if referrer_id in users:
        users[referrer_id]['referrals'] += 1
        users[referrer_id]['mining_power'] += 70
    users[new_user_id] = {
        'mining_power': 100,
        'referrals': 0
    }
    return redirect(f'/dashboard/{new_user_id}')

@app.route('/withdraw/<user_id>')
def withdraw(user_id):
    user = users.get(user_id)
    if not user:
        return "User not found", 404
    # Reset mining power after withdraw
    user['mining_power'] = 0
    return f"<h3>Withdraw initiated for User {user_id}. You will receive your tokens shortly!</h3>"

if __name__ == '__main__':
    app.run(debug=True)
