import os
import streamlit as st
import base64
from openai import OpenAI
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="🌿 Bosque de Bocetos",
    page_icon="🧚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# FUNCIONES
# =========================================================

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(
                image_file.read()
            ).decode("utf-8")
    except FileNotFoundError:
        return None


# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Quicksand:wght@400;500;600;700&display=swap');


/* ---------- FONDO GENERAL ---------- */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(220, 247, 220, 0.9), transparent 25%),
        radial-gradient(circle at 90% 15%, rgba(235, 220, 255, 0.8), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(255, 245, 190, 0.7), transparent 30%),
        linear-gradient(135deg, #f4fff3, #f7f0ff 50%, #fffbea);
}


/* ---------- FUENTES ---------- */

html, body, [class*="css"] {
    font-family: 'Quicksand', sans-serif;
}

h1, h2, h3 {
    font-family: 'Fredoka', sans-serif !important;
}


/* ---------- TITULO ---------- */

.main-title {
    text-align: center;
    font-family: 'Fredoka', sans-serif;
    font-size: 52px;
    font-weight: 700;
    color: #49734f;
    margin-top: -20px;
    margin-bottom: 0px;
    text-shadow: 2px 3px 0px #dff1d9;
}

.subtitle {
    text-align: center;
    font-size: 19px;
    color: #66756a;
    margin-bottom: 25px;
}


/* ---------- TARJETA DE INSTRUCCIONES ---------- */

.instruction-card {
    background: rgba(255,255,255,0.82);
    border: 2px solid #dcefd7;
    border-radius: 25px;
    padding: 18px 25px;
    text-align: center;
    box-shadow: 0px 8px 25px rgba(86, 112, 83, 0.10);
    margin-bottom: 20px;
}

.instruction-card b {
    color: #638b68;
}


/* ---------- DECORACIONES ---------- */

.decor-card {
    background: rgba(255,255,255,0.72);
    border: 2px solid #e5dff3;
    border-radius: 25px;
    padding: 18px 8px;
    text-align: center;
    box-shadow: 0px 8px 20px rgba(90, 70, 110, 0.10);
    font-size: 30px;
    line-height: 1.8;
}


/* ---------- CANVAS ---------- */

.canvas-card {
    background: rgba(255,255,255,0.90);
    padding: 15px;
    border-radius: 28px;
    border: 3px solid #dcefd7;
    box-shadow:
        0px 10px 30px rgba(77, 105, 75, 0.13),
        0px 0px 0px 5px rgba(255,255,255,0.5);
}


/* ---------- RESULTADO ---------- */

.result-card {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.95),
        rgba(246,239,255,0.95)
    );
    border: 2px solid #ded1f3;
    border-radius: 28px;
    padding: 25px;
    margin-top: 25px;
    box-shadow: 0px 10px 30px rgba(100, 80, 130, 0.12);
}

.result-title {
    font-family: 'Fredoka', sans-serif;
    color: #735c91;
    font-size: 28px;
}


/* ---------- BOTÓN ---------- */

.stButton > button {
    border-radius: 18px;
    border: none;
    background: linear-gradient(
        135deg,
        #7fae83,
        #9a7db8
    );
    color: white;
    font-family: 'Fredoka', sans-serif;
    font-size: 18px;
    font-weight: 600;
    padding: 12px 25px;
    box-shadow: 0px 6px 15px rgba(100, 90, 120, 0.20);
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 9px 20px rgba(100, 90, 120, 0.25);
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 20% 10%, #e6f6df, transparent 30%),
        linear-gradient(180deg, #f4fff0, #f7f0ff);
    border-right: 2px solid #dfead8;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #58795c;
    font-family: 'Fredoka', sans-serif !important;
}


/* ---------- LABELS ---------- */

label {
    font-weight: 600 !important;
    color: #617264 !important;
}


/* ---------- API CARD ---------- */

.api-card {
    background: rgba(255,255,255,0.75);
    border-radius: 20px;
    padding: 15px;
    border: 1px solid #e4dff0;
}


/* ---------- ESTRELLITAS ---------- */

.sparkles {
    text-align: center;
    font-size: 24px;
    letter-spacing: 12px;
    margin: 5px 0 15px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TÍTULO
# =========================================================

st.markdown(
    '<div class="sparkles">✨ 🌿 🧚 🌸 🍄 ✨</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🌿 Bosque de Bocetos 🧚</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Dibuja algo y deja que la inteligencia artificial descubra qué esconde tu boceto ✨'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# INSTRUCCIONES
# =========================================================

st.markdown("""
<div class="instruction-card">
    🎨 <b>Tu misión:</b> dibuja libremente en el bosque.
    <br>
    Puedes crear un personaje, un animal, una planta, una casa,
    una criatura mágica o cualquier cosa que imagines.
    <br><br>
    🌱 Cuando termines, presiona <b>“Analizar mi dibujo”</b>.
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🎨 Herramientas")

    drawing_mode = st.selectbox(
        "🖌️ Herramienta de dibujo",
        (
            "freedraw",
            "line",
            "rect",
            "circle",
            "point"
        ),
        format_func=lambda x: {
            "freedraw": "✏️ Dibujar",
            "line": "📏 Línea",
            "rect": "⬜ Rectángulo",
            "circle": "⭕ Círculo",
            "point": "• Punto"
        }[x]
    )

    stroke_width = st.slider(
        "✏️ Grosor del trazo",
        min_value=1,
        max_value=30,
        value=5
    )

    stroke_color = st.color_picker(
        "🎨 Color del trazo",
        "#58745B"
    )

    bg_color = st.color_picker(
        "🌈 Color del fondo",
        "#FFFFFF"
    )

    st.markdown("---")

    st.markdown("### 🌲 Sobre el bosque")

    st.write(
        "Este pequeño espacio convierte tus dibujos "
        "en una experiencia interactiva. 🌸"
    )

    st.markdown("---")

    st.markdown("### 🔐 Inteligencia artificial")

    ke = st.text_input(
        "Ingresa tu API Key",
        type="password"
    )


# =========================================================
# API KEY
# =========================================================

os.environ["OPENAI_API_KEY"] = ke

api_key = os.environ.get(
    "OPENAI_API_KEY",
    ""
)

client = None

if api_key:
    client = OpenAI(api_key=api_key)


# =========================================================
# CANVAS + DECORACIONES
# =========================================================

left, center, right = st.columns(
    [1, 6, 1],
    gap="medium"
)


# ---------- IZQUIERDA ----------

with left:

    st.markdown("""
    <div class="decor-card">
        🍄<br>
        🌸<br>
        🦋<br>
        🍃<br>
        🌱
    </div>
    """, unsafe_allow_html=True)


# ---------- CENTRO ----------

with center:

    st.markdown(
        '<div class="canvas-card">',
        unsafe_allow_html=True
    )

    canvas_result = st_canvas(
        fill_color="rgba(170, 120, 220, 0.20)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=700,
        drawing_mode=drawing_mode,
        key="fairy_canvas"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ---------- DERECHA ----------

with right:

    st.markdown("""
    <div class="decor-card">
        ✨<br>
        🌙<br>
        🧚<br>
        ⭐<br>
        🌼
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# BOTÓN
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

button_col1, button_col2, button_col3 = st.columns(
    [1, 2, 1]
)

with button_col2:

    analyze_button = st.button(
        "✨ Analizar mi dibujo ✨",
        use_container_width=True
    )


# =========================================================
# ANALIZAR DIBUJO
# =========================================================

if analyze_button:

    if not api_key:

        st.warning(
            "🔐 Primero ingresa tu API Key en el panel lateral."
        )

    elif client is None:

        st.error(
            "No se pudo iniciar la conexión con la inteligencia artificial."
        )

    else:

        try:

            image_data = canvas_result.image_data

        except RuntimeError:

            image_data = None


        if image_data is None:

            st.warning(
                "🎨 Primero haz un dibujo en el lienzo."
            )

        else:

            with st.spinner("🌿 Las hadas están observando tu dibujo..."):

                try:

                    # Convertir canvas a imagen
                    input_numpy_array = np.array(
                        image_data
                    )

                    input_image = Image.fromarray(
                        input_numpy_array.astype("uint8"),
                        "RGBA"
                    )

                    input_image.save(
                        "img.png"
                    )

                    # Convertir a Base64
                    base64_image = encode_image_to_base64(
                        "img.png"
                    )

                    # Prompt
                    prompt_text = """
                    Observa este dibujo infantil y descríbelo
                    de manera positiva, imaginativa y sencilla.

                    No juzgues la calidad artística del dibujo.

                    Identifica qué parece representar y describe
                    brevemente sus elementos principales.

                    Responde en español y de manera amigable
                    para un niño.

                    Organiza la respuesta así:

                    🌟 ¿QUÉ VEO?
                    Describe brevemente el dibujo.

                    🌿 ¿QUÉ PODRÍA SER?
                    Interpreta qué representa.

                    ✨ UN DETALLE ESPECIAL
                    Menciona un detalle interesante del dibujo.

                    🧚 UNA IDEA MÁGICA
                    Inventa una pequeña idea sobre el personaje
                    o mundo que aparece en el dibujo.
                    """

                    # Petición a OpenAI
                    response = client.chat.completions.create(

                        model="gpt-4o-mini",

                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": prompt_text
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url":
                                            f"data:image/png;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],

                        max_tokens=500
                    )

                    full_response = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    # Mostrar resultado
                    st.markdown(
                        '<div class="result-card">',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '<div class="result-title">'
                        '🌟 El bosque descubrió algo...'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.write(full_response)

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(
                        f"🌧️ No pudimos analizar el dibujo: {e}"
                    )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.markdown("""
<br><br>

<div style="
    text-align:center;
    color:#7a887b;
    font-family:'Quicksand';
    font-size:14px;
">
    🌱 Cada dibujo es una pequeña puerta hacia otro mundo ✨
</div>
""", unsafe_allow_html=True)
