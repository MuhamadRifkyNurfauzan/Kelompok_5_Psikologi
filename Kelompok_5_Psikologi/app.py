import streamlit as st
import pandas as pd
import pickle
import joblib
import os
import streamlit.components.v1 as components

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Stress Level Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS — FUTURISTIC GLASS UI
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.18), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(168,85,247,.16), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(14,165,233,.10), transparent 30%),
        #070b17;
    color: #eef2ff;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Glass cards */
.glass {
    background: rgba(17, 24, 39, .68);
    border: 1px solid rgba(255,255,255,.09);
    box-shadow: 0 18px 55px rgba(0,0,0,.28);
    backdrop-filter: blur(18px);
    border-radius: 24px;
}

.hero {
    padding: 42px 38px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(99,102,241,.22), rgba(168,85,247,.10)),
        rgba(17,24,39,.72);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 30px;
    box-shadow: 0 25px 70px rgba(0,0,0,.35);
}

.hero:before, .hero:after {
    content: "";
    position: absolute;
    border-radius: 999px;
    filter: blur(2px);
    opacity: .55;
    animation: floatOrb 7s ease-in-out infinite;
}
.hero:before {
    width: 170px; height: 170px;
    background: rgba(99,102,241,.22);
    right: -45px; top: -55px;
}
.hero:after {
    width: 120px; height: 120px;
    background: rgba(168,85,247,.18);
    left: 45%; bottom: -70px;
    animation-delay: -3s;
}

.hero-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: rgba(99,102,241,.14);
    border: 1px solid rgba(129,140,248,.28);
    color: #c7d2fe;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.hero h1 {
    font-size: clamp(2.2rem, 5vw, 4.2rem);
    line-height: 1.02;
    margin: 15px 0 12px;
    font-weight: 800;
    letter-spacing: -0.05em;
    background: linear-gradient(90deg,#fff,#c7d2fe,#e9d5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 760px;
    color: #aab4cf;
    font-size: 1rem;
    line-height: 1.7;
    margin: 0;
}

.section-title {
    margin-top: 30px;
    margin-bottom: 8px;
    font-size: 1.35rem;
    font-weight: 800;
    color: #f8fafc;
}

.section-subtitle {
    color: #8f9ab5;
    margin-bottom: 18px;
}

/* Scroll-ish reveal: cards animate into place as Streamlit rerenders sections */
.reveal {
    animation: revealUp .75s cubic-bezier(.2,.7,.2,1) both;
}
.delay1 { animation-delay: .08s; }
.delay2 { animation-delay: .16s; }
.delay3 { animation-delay: .24s; }
.delay4 { animation-delay: .32s; }

@keyframes revealUp {
    from { opacity: 0; transform: translateY(24px) scale(.985); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes floatOrb {
    0%,100% { transform: translate3d(0,0,0) scale(1); }
    50% { transform: translate3d(-18px,18px,0) scale(1.08); }
}

/* Streamlit widgets */
[data-testid="stSlider"] {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    padding: 14px 16px 7px;
    border-radius: 17px;
    margin-bottom: 10px;
}

[data-testid="stSelectbox"] {
    background: rgba(255,255,255,.025);
    border-radius: 17px;
}

.stButton > button {
    border: 0 !important;
    border-radius: 16px !important;
    min-height: 52px;
    font-weight: 800 !important;
    color: white !important;
    background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    box-shadow: 0 12px 30px rgba(99,102,241,.28);
    transition: transform .2s ease, box-shadow .2s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 38px rgba(139,92,246,.35);
}

div[data-testid="stMetric"] {
    background: rgba(17,24,39,.68);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 20px;
    padding: 18px;
}

.result-card {
    padding: 30px;
    margin: 24px 0;
    text-align: center;
    border-radius: 26px;
    background: linear-gradient(135deg,rgba(99,102,241,.18),rgba(168,85,247,.10)),rgba(17,24,39,.8);
    border: 1px solid rgba(255,255,255,.10);
    box-shadow: 0 22px 65px rgba(0,0,0,.30);
    animation: revealUp .65s ease both;
}

.result-title {
    color: #9aa6c1;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: .12em;
    font-weight: 700;
}

.result-value {
    font-size: clamp(2.6rem,6vw,4.5rem);
    font-weight: 800;
    margin: 6px 0;
    background: linear-gradient(90deg,#a5b4fc,#e9d5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.info-card {
    padding: 20px;
    border-radius: 20px;
    background: rgba(17,24,39,.60);
    border: 1px solid rgba(255,255,255,.07);
}

.footer {
    text-align: center;
    color: #69758f;
    font-size: 12px;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,.06);
}

[data-testid="stSidebar"] {
    background: rgba(7,11,23,.92);
    border-right: 1px solid rgba(255,255,255,.07);
}

[data-testid="stSidebar"] * {
    color: #dbe4ff;
}

hr {
    border-color: rgba(255,255,255,.07) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "stress_level.pkl")
    return joblib.load(model_path)

model = load_model()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🌿 Stress Predictor")
    st.markdown("<div style='text-align:center;font-size:42px;margin:8px 0;'>🌱</div>", unsafe_allow_html=True)
    st.caption("Machine Learning • Random Forest")
    st.divider()

    st.markdown("### 📌 Tentang Aplikasi")
    st.write(
        "Aplikasi ini menggunakan **Random Forest Classification** "
        "untuk memprediksi tingkat stres berdasarkan faktor psikologis, "
        "akademik, sosial, fisik, dan lingkungan."
    )

    st.divider()
    st.markdown("### 📊 Kategori")
    st.markdown("🟢 **0 — Rendah**")
    st.markdown("🟡 **1 — Sedang**")
    st.markdown("🔴 **2 — Tinggi**")

    st.divider()
    st.markdown("### 🎵 Study Corner")
    st.caption("Isi data sambil dengerin playlist favoritmu ✨")
    spotify_url = st.text_input(
        "Spotify Embed URL",
        value="https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M",
        help="Masukkan URL embed Spotify playlist/album/track."
    )

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero reveal">
    <span class="hero-badge">AI • STUDENT WELLNESS • RANDOM FOREST</span>
    <h1>Stress Level<br>Predictor</h1>
    <p>
        Analisis tingkat stres mahasiswa dengan tampilan futuristik,
        input interaktif, confidence model, dan Study Mode berbasis Spotify.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SPOTIFY
# =========================================================
with st.expander("🎵 Buka Spotify Study Mode", expanded=False):
    st.caption("Playlist Spotify dapat diputar langsung dari halaman ini.")
    safe_spotify = spotify_url.strip()
    if safe_spotify:
        components.html(
            f"""
            <div style="border-radius:16px;overflow:hidden;">
                <iframe
                    src="{safe_spotify}"
                    width="100%"
                    height="152"
                    frameborder="0"
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy">
                </iframe>
            </div>
            """,
            height=170
        )

# =========================================================
# INPUT
# =========================================================
st.markdown('<div class="section-title">📝 Data Mahasiswa</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Geser parameter sesuai kondisi yang ingin dianalisis.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="reveal delay1">', unsafe_allow_html=True)
st.markdown("#### 🧠 Faktor Psikologis", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    anxiety_level = st.slider("Anxiety Level", 0, 21, 10)
with col2:
    self_esteem = st.slider("Self Esteem", 0, 30, 15)
with col3:
    depression = st.slider("Depression", 0, 27, 10)

col1, col2, col3 = st.columns(3)
with col1:
    mental_health_history = st.selectbox(
        "Mental Health History", [0, 1],
        format_func=lambda x: "Tidak" if x == 0 else "Ya"
    )
with col2:
    headache = st.slider("Headache", 0, 5, 2)
with col3:
    breathing_problem = st.slider("Breathing Problem", 0, 5, 2)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="reveal delay2">', unsafe_allow_html=True)
st.markdown("#### 🏠 Kondisi Fisik & Lingkungan", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    blood_pressure = st.slider("Blood Pressure", 1, 3, 2)
with col2:
    sleep_quality = st.slider("Sleep Quality", 0, 5, 3)
with col3:
    noise_level = st.slider("Noise Level", 0, 5, 2)

col1, col2, col3 = st.columns(3)
with col1:
    living_conditions = st.slider("Living Conditions", 0, 5, 3)
with col2:
    safety = st.slider("Safety", 0, 5, 3)
with col3:
    basic_needs = st.slider("Basic Needs", 0, 5, 3)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="reveal delay3">', unsafe_allow_html=True)
st.markdown("#### 🎓 Faktor Akademik", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    academic_performance = st.slider("Academic Performance", 0, 5, 3)
with col2:
    study_load = st.slider("Study Load", 0, 5, 3)
with col3:
    teacher_student_relationship = st.slider("Teacher Student Relationship", 0, 5, 3)

col1, col2 = st.columns(2)
with col1:
    future_career_concerns = st.slider("Future Career Concerns", 0, 5, 3)
with col2:
    extracurricular_activities = st.slider("Extracurricular Activities", 0, 5, 3)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="reveal delay4">', unsafe_allow_html=True)
st.markdown("#### 👥 Faktor Sosial", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    social_support = st.slider("Social Support", 0, 3, 2)
with col2:
    peer_pressure = st.slider("Peer Pressure", 0, 5, 2)
with col3:
    bullying = st.slider("Bullying", 0, 5, 1)
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PREDICTION
# =========================================================
st.divider()
predict_button = st.button("🔮  ANALISIS STRESS LEVEL", use_container_width=True)

if predict_button:
    input_data = pd.DataFrame([{
        "anxiety_level": anxiety_level,
        "self_esteem": self_esteem,
        "mental_health_history": mental_health_history,
        "depression": depression,
        "headache": headache,
        "blood_pressure": blood_pressure,
        "sleep_quality": sleep_quality,
        "breathing_problem": breathing_problem,
        "noise_level": noise_level,
        "living_conditions": living_conditions,
        "safety": safety,
        "basic_needs": basic_needs,
        "academic_performance": academic_performance,
        "study_load": study_load,
        "teacher_student_relationship": teacher_student_relationship,
        "future_career_concerns": future_career_concerns,
        "social_support": social_support,
        "peer_pressure": peer_pressure,
        "extracurricular_activities": extracurricular_activities,
        "bullying": bullying
    }])

    prediction = model.predict(input_data)[0]

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        confidence = max(probabilities) * 100
    else:
        confidence = None

    if prediction == 0:
        stress_label = "Rendah"
        icon = "🟢"
        description = "Tingkat stres berada pada kategori rendah."
    elif prediction == 1:
        stress_label = "Sedang"
        icon = "🟡"
        description = "Tingkat stres berada pada kategori sedang."
    else:
        stress_label = "Tinggi"
        icon = "🔴"
        description = "Tingkat stres berada pada kategori tinggi."

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Hasil Prediksi</div>
        <div class="result-value">{icon} {stress_label}</div>
        <div style="color:#aab4cf">{description}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Ringkasan Analisis")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Class Prediksi", str(prediction))
    with col2:
        st.metric("Kategori", stress_label)
    with col3:
        st.metric("Confidence", f"{confidence:.2f}%" if confidence is not None else "N/A")

    if confidence is not None:
        st.progress(
            min(int(confidence), 100),
            text=f"Confidence Model: {confidence:.2f}%"
        )

    with st.expander("🔍 Lihat Data Input"):
        st.dataframe(input_data, use_container_width=True)

st.markdown("""
<div class="footer">
    🧠 Stress Level Predictor &nbsp;•&nbsp; Random Forest Classification
    <br>Student Wellness Machine Learning Project
</div>
""", unsafe_allow_html=True)
