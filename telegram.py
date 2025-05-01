from clockpi.config import TELEGRAM_TOKEN
import telebot
import pygame
import io

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Willkommen beim ClockPi! 🌟")

@bot.message_handler(commands=['uhr'])
def send_uhr_screenshot(message):
    # Screenshot vom aktuellen Pygame Fenster
    screenshot = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))
    screenshot.blit(pygame.display.get_surface(), (0, 0))
    
    buffer = io.BytesIO()
    pygame.image.save(screenshot, buffer)
    buffer.seek(0)
    
    bot.send_photo(message.chat.id, buffer)

def start_bot():
    print("Telegram Bot wird gestartet...")
    bot.infinity_polling()
