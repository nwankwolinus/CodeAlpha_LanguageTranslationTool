from gtts import gTTS
import uuid


def generate_speech(text, lang_code):
    """
    Converts text to speech and returns audio file path.
    Args:
        text (str): Text to convert to speech
        lang (str): Language code (e.g., 'en')
    Returns:
        str: Path to saved MP3 file
    """
    try:
        tts = gTTS(text=text, lang=lang_code)
        filename = f"{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"[TTS ERROR] {e}")
        return None


