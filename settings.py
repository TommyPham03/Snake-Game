import json

themes = {
    "light": {"background": (240, 240, 240), "snake": (0, 0, 0), "food": (0, 255, 0)},
    "dark": {"background": (20, 20, 20), "snake": (255, 255, 255), "food": (255, 165, 0)},
}

def load_preferences():
    try:
        with open("user_preferences.json", "r") as f:
            preferences = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        preferences = {"theme": "dark"}
    return preferences

def save_preferences(preferences):
    with open("user_preferences.json", "w") as f:
        json.dump(preferences, f)

def update_theme(new_theme):
    if new_theme in themes:
        save_preferences({"theme": new_theme})

