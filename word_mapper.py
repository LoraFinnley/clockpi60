def map_time_to_words(hour, minute):
    
    """
    Gibt eine Liste von Wörtern zur Uhrzeit zurück.
    Beispiel: 13:20 -> ["es", "isch", "zwänzg", "ab", "eis"]
    """
    hour = hour % 12 or 12
    words = ["es", "isch"]

    if minute == 0:
        words += ["punkt"]
    elif minute == 5:
        words += ["füf", "ab"]
    elif minute == 10:
        words += ["zäh", "ab"]
    elif minute == 15:
        words += ["viertu", "ab"]
    elif minute == 20:
        words += ["zwänzg", "ab"]
    elif minute == 25:
        words += ["füf", "vor", "haubi"]
    elif minute == 30:
        words += ["haubi"]
    elif minute == 35:
        words += ["füf", "ab", "haubi"]
    elif minute == 40:
        words += ["zwänzg", "vor"]
    elif minute == 45:
        words += ["viertu", "vor"]
    elif minute == 50:
        words += ["zäh", "vor"]
    elif minute == 55:
        words += ["füf", "vor"]

    if minute >= 25:
        hour = (hour + 1) % 12 or 12

    hour_words = {
        1: "eis", 2: "zwöi", 3: "drü", 4: "vieri", 5: "füfi", 6: "sächsi",
        7: "sibni", 8: "achti", 9: "nüni", 10: "zähni", 11: "eufi", 12: "zwöufi"
    }
    words.append(hour_words[hour])
    return words