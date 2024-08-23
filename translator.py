import streamlit as st
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = "translated_audio.mp3"
    tts.save(filename)
    return filename

def transcribe_speech(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Could not request results; check your network connection"


st.set_page_config(page_title="Language Translator", page_icon="🌐", layout="centered")
st.title("🌐 Language Translator")

st.markdown("""
<style>
body {
    background-color: #87ceeb;
    color: #E1E1E1;
    font-family: 'Arial', sans-serif;
}
.stApp {
    background-color: #6f5fe9;
}
.stButton>button {
    background-color: #FFA500;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
}
.stButton>button:hover {
    background-color: #FF8C00;
}
</style>
""", unsafe_allow_html=True)

input_text = st.text_area("Enter text to translate", height=150, key="input_text")
languages = {
    'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Azerbaijani': 'az',
    'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca',
    'Cebuano': 'ceb', 'Chichewa': 'ny', 'Chinese (Traditional)': 'zh-tw', 'Corsican': 'co', 'Croatian': 'hr',
    'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Filipino': 'tl',
    'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el',
    'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw', 'Hindi': 'hi',
    'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it',
    'Japanese': 'ja', 'Javanese': 'jw', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Korean': 'ko', 'Kurdish': 'ku',
    'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb',
    'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi',
    'Marathi': 'mr', 'Mongolian': 'mn', 'Myanmar': 'my', 'Nepali': 'ne', 'Norwegian': 'no', 'Odia': 'or', 'Pashto': 'ps',
    'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm',
    'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk',
    'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg',
    'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug',
    'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'
}

target_language = st.selectbox("Select Target Language", list(languages.keys()), index=29)


uploaded_file = st.file_uploader("Upload a text file to translate", type=["jpg", "jpeg", "txt"])


audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
if audio_file:
    transcribed_text = transcribe_speech(audio_file)
    st.write("Transcribed Text:")
    st.write(transcribed_text)
    
   
    target_language_voice = st.selectbox("Select target language for transcribed text", list(languages.keys()), index=29)
    translated_text_voice = translate_text(transcribed_text, languages[target_language_voice])
    st.write("Translated Text:")
    st.write(translated_text_voice)
    
    # Text-to-speech
    if st.button("Convert Transcribed Text to Speech"):
        audio_file_voice = text_to_speech(translated_text_voice, languages[target_language_voice])
        audio_bytes = open(audio_file_voice, "rb").read()
        st.audio(audio_bytes, format='audio/mp3')


if st.button("Translate"):
    input_text = st.session_state.get("input_text", "")
    if uploaded_file is not None:
        
        if uploaded_file.type == "text/plain":
            try:
                content = uploaded_file.read().decode("utf-8")
                translated_text = translate_text(content, languages[target_language])
                st.subheader("Original Text:")
                st.write(content)
                st.subheader("Translated Text:")
                st.write(translated_text)
                audio_file = text_to_speech(translated_text, languages[target_language])
                st.audio(audio_file, format='audio/mp3')
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        if input_text:
            try:
                translated_text = translate_text(input_text, languages[target_language])
                st.subheader("Original Text:")
                st.write(input_text)
                st.subheader("Translated Text:")
                st.write(translated_text)
                audio_file = text_to_speech(translated_text, languages[target_language])
                st.audio(audio_file, format='audio/mp3')
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Your uploaded file is translated.")