import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
from gtts import gTTS

# Configuración simple de colores
st.markdown("""
<style>
    .stTitle {
        color: #1E3A8A;
        font-size: 2.5rem;
    }
    .stHeader {
        color: #2563EB;
        font-size: 1.8rem;
    }
    .stSubheader {
        color: #374151;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("TRADUCTOR DE VOZ")
st.subheader("Escucha y traduce en tiempo real")

image = Image.open('OIG7.jpg')
st.image(image, width=300)

with st.sidebar:
    st.subheader("Configuración")
    st.write("Presiona el botón, cuando escuches la señal habla lo que quieres traducir, luego selecciona la configuración de lenguaje que necesites.")

st.write("🎤 Toca el Botón y habla lo que quieres traducir")

stt_button = Button(label=" 🎤 ESCUCHAR AHORA", width=300, height=50)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.success("Texto reconocido:")
        st.write(result.get("GET_TEXT"))
        
    try:
        os.mkdir("temp")
    except:
        pass
    
    st.subheader("Configuración de traducción")
    
    text = str(result.get("GET_TEXT"))
    
    # Solo permitimos español para evitar problemas de traducción
    st.info("Actualmente disponible solo para texto en español")
    
    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        ("Español", "Inglés"),
    )
    if out_lang == "Inglés":
        output_language = "en"
    else:
        output_language = "es"
    
    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
        ),
    )
    
    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    
    def text_to_speech(text, output_language, tld):
        # Simulamos la traducción - en una app real aquí iría el servicio de traducción
        if output_language == "en":
            # Traducción simple de ejemplo
            translation_map = {
                "hola": "hello",
                "cómo estás": "how are you", 
                "gracias": "thank you",
                "adiós": "goodbye"
            }
            trans_text = translation_map.get(text.lower(), f"Translation of: {text}")
        else:
            trans_text = text
            
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20].replace(" ", "_")
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    display_output_text = st.checkbox("Mostrar texto traducido")
    
    if st.button("CONVERTIR A AUDIO"):
        result, output_text = text_to_speech(text, output_language, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("**Audio generado:**")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("**Texto de salida:**")
            st.info(output_text)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
