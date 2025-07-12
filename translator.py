# translator.py
from googletrans import Translator

def translate_text(text, source, target):
    """
    Translate text using the unofficial Google Translate API (via googletrans).

    Args:
      text (str): The text to translate
      source (str): Source language code (e.g. 'en')
      target (str): Target language code (e.g. 'fr')
    
    Returns:
       str: Translated text
    """
    try: 
        translator = Translator()
        result = translator.translate(text, src=source, dest=target)
        return result.text
    except Exception as e:
        return f"Error during translation: {str(e)}"