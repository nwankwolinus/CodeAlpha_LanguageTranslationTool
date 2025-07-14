import streamlit as st
import os
from utils.supported_languages import get_supported_languages, get_all_translate_languages, get_language_name
from translator import translate_text
from utils.text_to_speech import generate_speech
from langdetect import detect

st.set_page_config(page_title="AI Language Translator", layout="centered")

# Toggle for all vs common
show_all = st.sidebar.checkbox("Show all available languages", value=False)

# Get appropriate language list
if show_all:
    LANGUAGES = get_all_translate_languages()
else:
    LANGUAGES = get_supported_languages()

# Sidebar instructions
st.sidebar.title("How to Use")
st.sidebar.markdown("""
1. **Enter or paste text** in the box above.
2. Language will **auto-detect** once you click outside the text area.
3. Select the **target language** to translate into.
4. Click **Translate** to see the result.
5. Optionally:
   - **Play audio** of the translated text.
   - **Copy the result** (via code block).
6. Use **"Show all languages"** to see extended options.
7. Click **Reset** to clear all inputs and start over.
""")

st.title("AI Language Translator")
st.markdown("Translate text from one language to another using Google Translate.")

# Text input
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

text = st.text_area("Enter text to translate", height=150, key="text_input")

translated = ""
detected_lang_code = None
detected_lang_name = None

# Auto-detect language if text exists
if len(text.strip()) > 20:
    try:
        detected_lang_code = detect(text)
        detected_lang_name = get_language_name(detected_lang_code)
        st.markdown(f"**Auto-detected language:** `{detected_lang_name}` (`{detected_lang_code}`)")
    except:
        st.warning("Could not detect language. Please type a bit more text.")
else:
    st.info("Enter at least 20 characters for language auto-detection.")

# Set default source language based on detection
language_keys = list(LANGUAGES.keys())
language_values = list(LANGUAGES.values())
default_index = 0

if detected_lang_code in language_values:
    default_index = language_values.index(detected_lang_code)

# Input
col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("From", language_keys, index=default_index)
with col2:
    tgt_lang = st.selectbox("To", language_keys)

# Translate
if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter text to translate.")
    elif src_lang == tgt_lang:
        st.warning("Source and target languages cannot be the same.")
    else:
        with st.spinner("Translating..."):
            translated = translate_text(text, LANGUAGES[src_lang], LANGUAGES[tgt_lang])
            st.session_state.translated = translated
        st.success("Translation Complete!")

# Output
if 'translated' in st.session_state:
    translated = st.session_state.translated
    st.subheader("Translated Text")
    st.markdown("Click the copy icon in the top-right of the box")
    st.code(translated, language=None) # Streamlit-native copy

    col_reset, _ = st.columns([1, 5])
    with col_reset:
        if st.button("🔄 Reset"):
             # Clear everything: input text, translated result, detected language
            st.session_state.clear()
            st.rerun()

    if st.checkbox("Play Translated Audio"):
        try:
            audio_file = generate_speech(translated, LANGUAGES[tgt_lang])
            if audio_file and os.path.exists(audio_file):
                st.audio(audio_file)
            else:
                st.error("Audio not generated. Language might not be supported.")
        except Exception as e:
            st.error(f"TTS Error: {e}")
