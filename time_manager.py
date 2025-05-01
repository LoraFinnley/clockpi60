from datetime import datetime, timedelta

def get_current_time():
    """Liefert aktuelle Zeit, auf 5 Minuten gerundet: bis 2:29 runter, ab 2:30 hoch."""
    now = datetime.now()
    print(f"Current time: {now}")

    if now.second >= 30:
        minute = now.minute + 1
    else:
        minute = now.minute

    minute = ((minute + 2) // 5) * 5

    if minute == 60:
        now += timedelta(hours=1)
        minute = 0

    rounded_time = now.replace(minute=minute, second=0, microsecond=0)
    print(f"Rounded time: {rounded_time}")
    return rounded_time


