import os
from dotenv import load_dotenv
import pygame
import telebot
import tempfile
from datetime import datetime, timedelta
import config




# 🔄 .env laden und prüfen
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("❌ TELEGRAM_TOKEN fehlt in .env Datei!")

# 🤖 Bot initialisieren
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 📨 Startbefehl
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Willkommen beim ClockPi! 🌟")

# 📷 Screenshot der Uhr senden
@bot.message_handler(commands=['uhr'])
def send_uhr_screenshot(message):
    surface = pygame.display.get_surface()
    if surface is None:
        bot.reply_to(message, "⚠️ Kein Display verfügbar.")
        return

    with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
        pygame.image.save(surface, tmpfile.name)
        tmpfile.seek(0)
        bot.send_photo(message.chat.id, tmpfile)

# 💖 Herzmodus ein-/ausschalten
@bot.message_handler(commands=['heartmode'])
def toggle_heart_mode(message):
    config.HEART_MODE = not config.HEART_MODE
    status = "aktiviert 💖" if config.HEART_MODE else "deaktiviert 💔"
    bot.reply_to(message, f"Herzmodus wurde {status}.")


# Logs abrufen
@bot.message_handler(commands=['logs'])
def send_logs(message):
    log_path = "logs/wordclock.log"
    if not os.path.exists(log_path):
        bot.reply_to(message, "❌ Keine Logdatei gefunden.")
        return
    
    now = datetime.now()
    last_24h = now - timedelta(hours=24)
    filtered_lines = []

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                timestamp_str = line.split(" - ")[0]
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                if timestamp >= last_24h:
                    filtered_lines.append(line)
            except Exception:
                continue  # überspringe ungültige Zeilen

    if not filtered_lines:
        bot.reply_to(message, "ℹ️ Keine Logs aus den letzten 24 Stunden gefunden.")
        return

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".log", delete=False) as tmp:
        tmp.writelines(filtered_lines)
        tmp.seek(0)
        bot.send_document(message.chat.id, tmp)

    os.unlink(tmp.name) 

# 🚀 Bot starten
def start_bot():
    print("Telegram Bot wird gestartet...")
    bot.infinity_polling()
