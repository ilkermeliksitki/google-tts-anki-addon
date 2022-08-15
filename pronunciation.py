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
<<<<<<< HEAD
          "languageCode": config["language-code"],
          "name": config["name"]
        },
        "audioConfig": {
           "audioEncoding": "MP3",
           "effectsProfileId": [
                "headphone-class-device"
            ],
        "speakingRate": 0.97
=======
          "languageCode": config["language-code"]
        },
        "audioConfig": {
           "audioEncoding": "MP3"
>>>>>>> c55ba66d693f0c9febfae10229f2268b188f05af
        }
    }

    r = requests.post(url,  params=params, data=json.dumps(data))
<<<<<<< HEAD
=======

>>>>>>> c55ba66d693f0c9febfae10229f2268b188f05af
    return base64.b64decode(r.json()["audioContent"])
