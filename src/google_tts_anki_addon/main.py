from anki.media import MediaManager
from aqt import mw
from aqt.sound import av_player
from aqt.utils import showInfo, qconnect, showText, tooltip, getText
from PyQt6.QtGui import QAction, QKeySequence

from .pronunciation import create_sound_file, config


def rreplace(s: str, old: str, new: str, max_replace=1):
    """
    this function works from the opposite direction of str.replace function.
    >>> rreplace("mississippi", "p", "P", 1)
    'mississipPi'
    """
    ls = s.rsplit(old, max_replace)
    return new.join(ls)


def append_sound_to_note(text, filename):
    """
    append sound file to the last field of the card.
    if the text of the sound is found in that field,
    it will only append the play button in front of it.
    """
    # ensure we are in a state where we can access the note
    if mw.reviewer.card is None:
        showText("The sound did not append to any note. You must be in review mode.")
        return

    try:
        note = mw.reviewer.card.note()
        if note is None:
             showText("The sound did not append to any note. Note is None.")
             return

        ls_tp = note.items()
        if not ls_tp:
             showText("The sound did not append to any note. Note has no fields.")
             return

        first_field_name = ls_tp[0][0]
        first_field_content = ls_tp[0][1]
        last_field_name = ls_tp[-1][0]
        last_field_content = ls_tp[-1][1]

        state = mw.reviewer.state
        if state == "question":
            # the sound will be added to the question side at the end without writing the sound contents
            # this is done because the pronunciation of the words puts at the end of first field.
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

    except Exception as e:
        showText(f"An error occurred while appending sound: {e}")


def append_sound_to_media_file(desired_name, binary_text):
    """write binary data to media file of anki and return the written file's name"""
    media_manager = MediaManager(mw.col, server=True)
    return media_manager.write_data(desired_name, data=binary_text)


def prompt_search():
    text, number = getText("Enter a text:", title="Pronunciation from Google-API")
    text = text.strip()

    if len(text) > 1 and number == 1:
        # number 1 means, user clicked okay.
        try:
            binary_data = create_sound_file(text)
            filename = append_sound_to_media_file(desired_name="google_api.mp3", binary_text=binary_data)
            av_player.play_file(filename)
            append_sound_to_note(text, filename)
        except Exception as e:
            showInfo(f"Failed to create or play sound: {e}")

    elif number == 0:
        # number 0 means, user clicked cancel
        pass
    else:
        showInfo("Text should be greater than one letter.")


action = QAction("&Google-TTS API", mw)
action.setShortcut(QKeySequence(config["shortcut"]))
qconnect(action.triggered, prompt_search)
mw.form.menuTools.addAction(action)
