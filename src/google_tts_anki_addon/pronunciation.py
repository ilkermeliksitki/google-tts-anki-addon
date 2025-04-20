import requests
import base64
import json
import random
import time
from aqt import mw

# different seeding based on time 
random.seed(time.time())
config = mw.addonManager.getConfig(__name__)


def create_sound_file(text):
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"

    if config["language-code"] == "en":
        language_code = "en-US"
        name = random.choice(["en-US-Chirp-HD-F", "en-US-Chirp3-HD-Aoede", "en-US-Chirp3-HD-Kore", "en-US-Chirp-HD-O"])
    elif config["language-code"] == "de":
        language_code = "de-DE"
        name = random.choice(["de-DE-Chirp-HD-O", "de-DE-Chirp-HD-F", "de-DE-Chirp3-HD-Charon", "de-DE-Chirp3-HD-Kore", "de-DE-Chirp3-HD-Zephyr"])
    else:
        pass

    params = {
        "key": config["google-tts-api-key"],
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

    r = requests.post(url,  params=params, data=json.dumps(data))
    return base64.b64decode(r.json()["audioContent"])
