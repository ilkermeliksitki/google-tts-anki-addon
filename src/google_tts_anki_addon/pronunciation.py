import requests
import base64
import json
import random
from aqt import mw

# configuration for supported voices
VOICES = {
    "en": {
        "language_code": "en-US",
        "names": [
            "en-US-Chirp-HD-F",
            "en-US-Chirp3-HD-Aoede",
            "en-US-Chirp3-HD-Kore",
            "en-US-Chirp-HD-O"
        ]
    },
    "de": {
        "language_code": "de-DE",
        "names": [
            "de-DE-Chirp-HD-O",
            "de-DE-Chirp-HD-F",
            "de-DE-Chirp3-HD-Charon",
            "de-DE-Chirp3-HD-Kore",
            "de-DE-Chirp3-HD-Zephyr"
        ]
    }
}

config = mw.addonManager.getConfig(__name__)


def create_sound_file(text):
    """
    generates a sound file for the given text using google tts api.
    """
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"

    lang_key = config.get("language-code")
    if lang_key not in VOICES:
        raise ValueError(f"Unsupported or missing language-code in config: {lang_key}")

    voice_config = VOICES[lang_key]
    language_code = voice_config["language_code"]
    name = random.choice(voice_config["names"])

    params = {
        "key": config.get("google-tts-api-key"),
    }

    data = {
        "input": {
            "text": text
        },
        "voice": {
            "languageCode": language_code,
            "name": name
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "effectsProfileId": [
                "headphone-class-device"
            ],
        }
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()

        response_data = response.json()
        if "audioContent" not in response_data:
            raise KeyError("API response missing 'audioContent' field")

        return base64.b64decode(response_data["audioContent"])

    except requests.exceptions.RequestException as e:
        # log the error or handle it appropriately for the addon context
        print(f"Network error in create_sound_file: {e}")
        raise
    except (KeyError, ValueError) as e:
        print(f"Data error in create_sound_file: {e}")
        raise
