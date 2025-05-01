import os
from dotenv import load_dotenv
import pygame
import telebot
import special_modes
import tempfile

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
    special_modes.HEART_MODE = not special_modes.HEART_MODE
    status = "aktiviert 💖" if special_modes.HEART_MODE else "deaktiviert 💔"
    bot.reply_to(message, f"Herzmodus wurde {status}.")

# 🚀 Bot starten
def start_bot():
    print("Telegram Bot wird gestartet...")
    bot.infinity_polling()
