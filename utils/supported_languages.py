from googletrans import LANGUAGES as GOOGLE_LANGUAGES
from gtts.lang import tts_langs
from babel.core import get_global
import pycountry

def get_language_name(lang_code):
    try:
        lang = pycountry.languages.get(alpha_2=lang_code)
        if lang and hasattr(lang, 'name'):
            return lang.name
    except:
        pass
    return lang_code.upper() # fallbact to code if name not found

def country_code_to_flag(cc):
    """Convert country code to emoji flag."""
    try:
        return ''.join(chr(127397 + ord(c)) for c in cc.upper())
    except:
        return '🌐'

def get_likely_country_for_lang(lang_code):
    """Use babel to get most likely country for a given language."""
    try:
        likely_subtags = get_global('likely_subtags')
        if lang_code in likely_subtags:
            tag = likely_subtags[lang_code]
            if '_' in tag:
                return tag.split('_')[-1].lower()
    except:
        pass
    return None

def get_flag_for_language(lang_code):
    country = get_likely_country_for_lang(lang_code)
    return country_code_to_flag(country) if country else '🌐'

def format_language_display(lang_code, lang_name):
    flag = get_flag_for_language(lang_code)
    return f"{flag} {lang_name.title()}"

def get_supported_languages():
    """
    Returns a dictionary of language names to ISO codes
    that are supported by both Google Translate and gTTS.
    (for cases where TTS/audio playback is required).
    """
    gtts_supported = tts_langs()
    return {
        format_language_display(code, GOOGLE_LANGUAGES[code]): code
        for code in GOOGLE_LANGUAGES
        if code in gtts_supported
    }

def get_all_translate_languages():
    """
    Returns all languages supported by Google Translate,
    even if they don't support TTS.
    """
    return {
        format_language_display(code, name): code
        for code, name in GOOGLE_LANGUAGES.items()
    }

