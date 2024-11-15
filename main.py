from flask import Flask, request
from datetime import datetime
import requests

app = Flask(__name__)

from config import loadConfig

data = loadConfig()
BOT_TOKEN = data['BOT_TOKEN']
CHAT_ID = data['CHAT_ID']
BOT_OWNER = data['BOT_OWNER']

host = data['host']
port = data['port']

def tg(message: str):
    print(message)
    requests.get(
        f"https://api.telegram.org/{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def getMe():
    print(requests.get(f"https://api.telegram.org/{BOT_TOKEN}/getMe").content)


def myIP():
    return requests.get("https://api64.ipify.org").content


def getTime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


@app.route('/', methods=['POST'])
def notify():
    message = request.get_data(as_text=True)

    x_real_ip = request.headers.get('X-Real-IP')
    remote_addr = request.remote_addr
    tg(f'{message}\n\nX-Real-IP: {x_real_ip}\nRemote Address: {remote_addr}')
    return f'I will deliver your message to {BOT_OWNER}.\nYour X-Real-IP: {x_real_ip}\nYour address: {remote_addr}\n\n**Your Message:**\n{message} '


if __name__ == '__main__':
    from waitress import serve
    tg(f"Ping! from {myIP()}.")
    print(getMe())
    serve(app, host=host, port=port)
