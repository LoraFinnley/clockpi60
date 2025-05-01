import threading
import time
from time_manager import get_current_time
from word_mapper import map_time_to_words
from display import start_display
from telegram import start_bot

# Optional: Funktion zum Anzeigen der Wörter im Terminal
def display_words(words):
    print("\nAktuelle Anzeige: ")
    print(" ".join(words))


def main_loop(refresh_seconds=30):
    try:
        while True:
            current_time = get_current_time()
            hour = current_time.hour
            minute = current_time.minute

            words = map_time_to_words(hour, minute)
            display_words(words)

            time.sleep(refresh_seconds)

    except KeyboardInterrupt:
        print("\nUhr wurde beendet.")


if __name__ == "__main__":
     # Telegram-Bot starten
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    # Zeitloop in Hintergrund-Thread
    background_thread = threading.Thread(target=main_loop, daemon=True)
    background_thread.start()

    # 🖼️ Pygame im Hauptthread (macOS-konform)
    start_display()
