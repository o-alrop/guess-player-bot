
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}/"

def telegram(method, data):
    return requests.post(
        API + method,
        json=data,
        timeout=20
    )

def send_message(chat_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if keyboard:
        data["reply_markup"] = keyboard

    telegram("sendMessage", data)

def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "⚽ ابدأ اللعب", "callback_data": "play"}],
            [{"text": "📖 طريقة اللعب", "callback_data": "help"}],
            [{"text": "👤 حسابي", "callback_data": "profile"}]
        ]
    }

@app.route("/", methods=["GET"])
def home():
    return "ALI BOT IS RUNNING!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            send_message(
                chat_id,
                "⚽ أهلاً بك في لعبة خمن اللاعب!\n\n"
                "استعد لاختبار معلوماتك الكروية.",
                main_menu()
            )

    elif "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        data = query.get("data", "")

        telegram("answerCallbackQuery", {
            "callback_query_id": query["id"]
        })

        if data == "play":
            send_message(
                chat_id,
                "⚽ قريباً: نظام إنشاء المباريات والتحديات!"
            )

        elif data == "help":
            send_message(
                chat_id,
                "📖 طريقة اللعب:\n"
                "اختر لاعباً سرياً، وتبادل الأسئلة "
                "مع منافسك، ثم حاول اكتشاف لاعبه."
            )

        elif data == "profile":
            send_message(
                chat_id,
                "👤 ملفك الشخصي قيد التجهيز."
            )

    return jsonify({"ok": True})

def setup_webhook():
    url = os.environ.get("RENDER_EXTERNAL_URL")
    if TOKEN and url:
        telegram("setWebhook", {
            "url": url.rstrip("/") + "/webhook"
        })

if TOKEN:
    setup_webhook()
