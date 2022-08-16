import requests
import base64
import json
from aqt import mw

config = mw.addonManager.getConfig(__name__)


def create_sound_file(text):
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"

    params = {
        "key": config["google-tts-api-key"],
    }

    data = {
        "input": {
          "text": text
        },
        "voice": {
          "languageCode": config["language-code"],
          "name": config["name"]
        },
        "audioConfig": {
           "audioEncoding": "MP3",
           "effectsProfileId": [
                "headphone-class-device"
            ],
        "speakingRate": 0.97
        }
    }

    r = requests.post(url,  params=params, data=json.dumps(data))
    return base64.b64decode(r.json()["audioContent"])
