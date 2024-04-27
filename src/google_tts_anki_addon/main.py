from anki.media import MediaManager
import time
from aqt import mw
from aqt.sound import av_player
from aqt.utils import showInfo, qconnect, showText
# from aqt.qt import QKeySequence, QAction
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMenu
from aqt.utils import tooltip, getText

from anki.template import TemplateRenderContext, TemplateRenderOutput
from anki import hooks

from .pronunciation import create_sound_file, config


def rreplace(s:str, old:str, new:str, max_replace=1):
    """
    this function work from the opposite direction of str.replace function.
    >>> rreplace("mississipi", "p", "P", 1)
    'mississiPi'
    """
    ls = s.rsplit(old, max_replace)
    return new.join(ls)


def append_sound_to_note(text, filename):
    """
    append sound file to the last field of the card.
    If the text of the sound is found in that field, it will only append the play button in front of it.
    """
    try:
        note = mw.reviewer.card.note()
        ls_tp = note.items()
        first_field_name = ls_tp[0][0]
        first_field_content= ls_tp[0][1]
        last_field_name = ls_tp[-1][0]
        last_field_content = ls_tp[-1][1]

        state = mw.reviewer.state
        if state == "question":
            # the sound will be added to the question side at the end without writing the sound contents
            # this is done because of the pronunciation of the words puts at the end of first field.
            note[first_field_name] = first_field_content + f" [sound:{filename}]"
        else:
            # this part is for answer state.
            if text in last_field_content:
                note[last_field_name] = rreplace(last_field_content, text, f"{text} [sound:{filename}]")
            else:
                note[last_field_name] = last_field_content + f"\n<br>\n{text} [sound:{filename}]"
        mw.col.update_note(note)
        mw.reviewer._redraw_current_card()
        tooltip("Sound is added.", 500)
    except AttributeError:
        showText(
            "The sound did not append to any note. Because you have to be in review mode"
        )


def append_sound_to_media_file(desired_name, binary_text):
    """write binary data to media file of anki and return the written file's name"""
    media_manager = MediaManager(mw.col, server=True)
    return media_manager.write_data(desired_name, data=binary_text)


def prompt_search():
    text, number = getText("Enter a text:", title="Pronunciation from Google-API")
    text = text.strip()
    if len(text) > 1 and number == 1:
        """number 1 means, user click to okay."""
        if text.endswith("~~"):
            text = text[:-2] + " jemand oder etwas Akkusativ"
        elif text.endswith("~"):
            text = text[:-1] + " etwas Akkusativ"
        binary_data = create_sound_file(text)
        filename = append_sound_to_media_file(desired_name="google_api.mp3", binary_text=binary_data)
        # tooltip("Playing...", period=1000)
        av_player.play_file(filename)
        append_sound_to_note(text, filename)
    elif number == 0:
        """number 0 means, user click cancel"""
        pass
    else:
        showInfo("Text should be grater than one letter.")


action = QAction("&Google-TTS API", mw)
action.setShortcut(QKeySequence(config["shortcut"]))
qconnect(action.triggered, prompt_search)
mw.form.menuTools.addAction(action)
