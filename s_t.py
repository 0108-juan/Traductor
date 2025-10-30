import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
from gtts import gTTS
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Traductor de Voz",
    page_icon="🌐",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-header {
        font-size: 1.4rem;
        color: #2563EB;
        border-bottom: 2px solid #2563EB;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .speech-btn-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .result-box {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0EA5E9;
        margin: 1rem 0;
    }
    .audio-container {
        background: linear-gradient(135deg, #E0F7FA 0%, #B2EBF2 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #00ACC1;
        margin: 1rem 0;
    }
    .config-box {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin: 1rem 0;
    }
    .stButton button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    .sidebar-section {
        background-color: #F1F5F9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<div class="main-title">🌐 Traductor de Voz</div>', unsafe_allow_html=True)

# Imagen
try:
    image = Image.open('OIG7.jpg')
    st.image(image, width=250, use_column_width=False)
except:
    st.info("Imagen representativa del traductor")

# Sidebar mejorado
with st.sidebar:
    st.markdown("### 🎯 Instrucciones")
    st.markdown("""
    <div class="sidebar-section">
    1. Presiona el botón <strong>Escuchar 🎤</strong><br>
    2. Habla cuando veas la señal<br>
    3. Selecciona los idiomas<br>
    4. Convierte a audio
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Información")
    st.markdown("""
    <div class="sidebar-section">
    • Traducción en tiempo real<br>
    • Soporte múltiples idiomas<br>
    • Conversión a voz<br>
    • Descarga de audio
    </div>
    """, unsafe_allow_html=True)

# Sección de reconocimiento de voz
st.markdown('<div class="section-header">🎤 Reconocimiento de Voz</div>', unsafe_allow_html=True)
st.write("Presiona el botón y habla lo que quieres traducir")

# Botón de reconocimiento de voz
st.markdown('<div class="speech-btn-container">', unsafe_allow_html=True)
stt_button = Button(label=" 🎤 ESCUCHAR - Habla ahora", width=400, height=60, 
                   css_classes=["speech-button"], styles={"font-size": "18px"})

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
    override_height=100,
    debounce_time=0)
st.markdown('</div>', unsafe_allow_html=True)

# Procesar resultado del reconocimiento de voz
if result:
    if "GET_TEXT" in result:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### 📝 Texto Reconocido:")
        st.success(result.get("GET_TEXT"))
        st.markdown('</div>', unsafe_allow_html=True)
    
    try:
        os.mkdir("temp")
    except:
        pass
    
    # Configuración de traducción
    st.markdown('<div class="section-header">⚙️ Configuración de Traducción</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="config-box">', unsafe_allow_html=True)
        in_lang = st.selectbox(
            "**Idioma de Entrada**",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
            key="in_lang"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="config-box">', unsafe_allow_html=True)
        out_lang = st.selectbox(
            "**Idioma de Salida**",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
            key="out_lang"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Mapeo de idiomas
    lang_map = {
        "Inglés": "en", "Español": "es", "Bengali": "bn", 
        "Coreano": "ko", "Mandarín": "zh-cn", "Japonés": "ja"
    }
    
    input_language = lang_map[in_lang]
    output_language = lang_map[out_lang]
    
    # Configuración de acento
    st.markdown('<div class="config-box">', unsafe_allow_html=True)
    english_accent = st.selectbox(
        "**Acento de Voz**",
        (
            "Defecto", "Español", "Reino Unido", "Estados Unidos", 
            "Canada", "Australia", "Irlanda", "Sudáfrica",
        ),
        key="accent"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mapeo de acentos
    accent_map = {
        "Defecto": "com", "Español": "com.mx", "Reino Unido": "co.uk",
        "Estados Unidos": "com", "Canada": "ca", "Australia": "com.au",
        "Irlanda": "ie", "Sudáfrica": "co.za"
    }
    tld = accent_map[english_accent]
    
    # Función de traducción y texto a voz
    def text_to_speech(input_language, output_language, text, tld):
        translator = Translator()
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = "".join(c for c in text[:20] if c.isalnum()).rstrip()
            if not my_file_name:
                my_file_name = "audio"
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    # Checkbox para mostrar texto
    display_output_text = st.checkbox("📄 Mostrar texto traducido", value=True)
    
    # Botón de conversión
    if st.button("🔊 Convertir a Audio", use_container_width=True):
        text = str(result.get("GET_TEXT"))
        with st.spinner('Traduciendo y generando audio...'):
            result_file, output_text = text_to_speech(input_language, output_language, text, tld)
            
            # Mostrar audio
            st.markdown('<div class="audio-container">', unsafe_allow_html=True)
            st.markdown("## 🎧 Audio Traducido")
            audio_file = open(f"temp/{result_file}.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", start_time=0)
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar Audio",
                data=audio_bytes,
                file_name=f"traduccion_{output_language}.mp3",
                mime="audio/mp3",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Mostrar texto traducido
            if display_output_text:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown("### 📝 Texto Traducido:")
                st.info(output_text)
                st.markdown('</div>', unsafe_allow_html=True)

# Función de limpieza
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

