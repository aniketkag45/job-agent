import json


def load_user_preferences():

    with open(
        "config/user_preferences.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)