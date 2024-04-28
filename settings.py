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

# def get_high_score():
#     try:
#         with open("high_score.txt", "r") as f:
#             high_score = int(f.read())
#     except (FileNotFoundError, ValueError):
#         high_score = 0
#     return high_score

def get_high_score(user_data):
    """Retrieve the high score from the user's profile."""
    return user_data.get('high_score', 0)

def save_high_score(high_score):
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))