import requests
import base64
import json
import random
from aqt import mw

config = mw.addonManager.getConfig(__name__)


def create_sound_file(text):
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    
    # randomize accents if it is random is true in config file.
    if config["random"]:
        name, language_code = random.choice(seq=[('en-US-Neural2-F', 'en-US'), ('en-AU-Neural2-C', 'en-AU'), ('en-GB-Neural2-C', 'en-GB')])
    else:
        name = config['name']
        language_code = config['language_code']

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
        "speakingRate": 0.97
        }
    }

    r = requests.post(url,  params=params, data=json.dumps(data))
    return base64.b64decode(r.json()["audioContent"])
