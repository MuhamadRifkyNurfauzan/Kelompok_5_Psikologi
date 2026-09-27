import streamlit as st
import pandas as pd
import pickle

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="MindCheck — Stress Level Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS — MODERN PSYCHOLOGY DASHBOARD
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --primary: #6C63FF;
    --primary-dark: #5148E5;
    --secondary: #8B5CF6;
    --ink: #172033;
    --muted: #697386;
    --surface: #FFFFFF;
    --soft: #F5F6FF;
    --border: #E7E9F2;
    --success: #16A34A;
    --warning: #D97706;
    --danger: #DC2626;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(108,99,255,.10), transparent 25%),
        radial-gradient(circle at 92% 15%, rgba(139,92,246,.08), transparent 25%),
        #F7F8FC;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17152F 0%, #24204B 100%);
    border-right: 0;
}

[data-testid="stSidebar"] * {
    color: #F7F7FF !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.15);
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 34px 38px;
    border-radius: 28px;
    color: white;
    background:
        radial-gradient(circle at 85% 20%, rgba(255,255,255,.18), transparent 24%),
        radial-gradient(circle at 10% 100%, rgba(255,255,255,.10), transparent 30%),
        linear-gradient(135deg, #5B55E8 0%, #7C5CFA 55%, #9B6CFF 100%);
    box-shadow: 0 18px 45px rgba(91,85,232,.20);
    margin-bottom: 26px;
}

.hero h1 {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(32px, 5vw, 52px);
    line-height: 1.05;
    margin: 0 0 12px 0;
    font-weight: 800;
    letter-spacing: -1.5px;
}

.hero p {
    margin: 0;
    max-width: 720px;
    font-size: 16px;
    line-height: 1.65;
    color: rgba(255,255,255,.88);
}

.hero-badge {
    display: inline-block;
    padding: 7px 12px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,.24);
    border-radius: 999px;
    background: rgba(255,255,255,.12);
    font-size: 13px;
    font-weight: 700;
}

.section-card {
    background: rgba(255,255,255,.88);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 22px 24px 8px;
    margin: 18px 0;
    box-shadow: 0 10px 30px rgba(23,32,51,.05);
}

.section-heading {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 0 0 2px 0;
    font-family: 'Manrope', sans-serif;
    color: var(--ink);
    font-size: 21px;
    font-weight: 800;
}

.section-description {
    color: var(--muted);
    font-size: 13px;
    margin: 4px 0 18px 0;
}

.input-label {
    font-size: 12px;
    font-weight: 700;
    color: #687086;
    letter-spacing: .3px;
}

[data-testid="stSlider"] {
    padding-top: 2px;
}

[data-testid="stSlider"] label p,
[data-testid="stSelectbox"] label p {
    font-weight: 600 !important;
    color: #293247 !important;
}

.stSlider [data-baseweb="slider"] {
    padding-top: 3px;
}

div.stButton > button {
    border: 0;
    border-radius: 14px;
    min-height: 54px;
    font-family: 'Manrope', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: white;
    background: linear-gradient(135deg, #5B55E8, #815CF5);
    box-shadow: 0 10px 24px rgba(91,85,232,.22);
    transition: all .2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(91,85,232,.28);
}

.result-card {
    border-radius: 24px;
    padding: 28px;
    margin-top: 22px;
    text-align: center;
    background: white;
    border: 1px solid var(--border);
    box-shadow: 0 14px 38px rgba(23,32,51,.08);
}

.result-kicker {
    color: #7A8295;
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.4px;
}

.result-value {
    font-family: 'Manrope', sans-serif;
    font-size: 46px;
    font-weight: 800;
    line-height: 1.1;
    margin: 9px 0;
}

.result-desc {
    color: var(--muted);
    margin-bottom: 18px;
}

.result-low { color: var(--success); }
.result-medium { color: var(--warning); }
.result-high { color: var(--danger); }

.info-strip {
    display: flex;
    gap: 12px;
    align-items: center;
    padding: 14px 16px;
    border-radius: 14px;
    background: #F5F6FF;
    border: 1px solid #E6E5FF;
    color: #454C68;
    font-size: 13px;
    line-height: 1.5;
    margin: 12px 0 20px;
}

.metric-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 17px;
    box-shadow: 0 7px 20px rgba(23,32,51,.045);
}

.footer {
    text-align: center;
    padding: 28px 0 5px;
    color: #8A91A3;
    font-size: 12px;
}

.disclaimer {
    font-size: 11px;
    line-height: 1.55;
    color: rgba(255,255,255,.65);
    margin-top: 16px;
}

@media (max-width: 768px) {
    .block-container { padding: 1rem .8rem 2rem; }
    .hero { padding: 26px 22px; border-radius: 22px; }
    .hero h1 { font-size: 34px; }
    .section-card { padding: 18px 16px 5px; border-radius: 18px; }
    .result-value { font-size: 38px; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================
@st.cache_resource
def load_model():
    with open("stress_level.pkl", "rb") as file:
        return pickle.load(file)

model = load_model()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🧠 MindCheck")
    st.caption("Stress Level Predictor")
    st.divider()

    st.markdown("### 📌 Tentang Aplikasi")
    st.write(
        "Aplikasi ini menggunakan **Random Forest Classification** "
        "untuk memprediksi tingkat stres berdasarkan faktor psikologis, "
        "fisik, akademik, sosial, dan lingkungan."
    )

    st.divider()

    st.markdown("### 📊 Kategori Stress Level")
    st.markdown("🟢 **0 — Rendah**")
    st.markdown("🟠 **1 — Sedang**")
    st.markdown("🔴 **2 — Tinggi**")

    st.divider()
    st.markdown("### 🔎 Cara Menggunakan")
    st.write(
        "1. Isi semua indikator sesuai kondisi.\n"
        "2. Tekan tombol prediksi.\n"
        "3. Lihat kategori dan confidence model."
    )

    st.markdown(
        '<div class="disclaimer">Catatan: hasil merupakan prediksi model machine learning, '
        'bukan diagnosis medis atau psikologis.</div>',
        unsafe_allow_html=True
    )

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-badge">KELOMPOK 5 • PROJECT PSIKOLOGI</div>
    <h1>🧠 MindCheck</h1>
    <p>
        Prediksi tingkat stres mahasiswa dengan pendekatan
        <b>Random Forest Classification</b>. Masukkan kondisi pada setiap
        indikator untuk mendapatkan hasil prediksi dari model.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="info-strip">💡 <b>Tips:</b>&nbsp; Isi setiap indikator berdasarkan kondisi yang paling menggambarkan keadaan mahasiswa.</div>',
    unsafe_allow_html=True
)

# =========================================================
# INPUT — PSYCHOLOGICAL
# =========================================================
st.markdown("""
<div class="section-card">
    <div class="section-heading">🧠 Faktor Psikologis</div>
    <div class="section-description">Indikator yang berkaitan dengan kondisi psikologis dan kesehatan mental.</div>
""", unsafe_allow_html=True)

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

# =========================================================
# INPUT — PHYSICAL & ENVIRONMENT
# =========================================================
st.markdown("""
<div class="section-card">
    <div class="section-heading">🏠 Kondisi Fisik & Lingkungan</div>
    <div class="section-description">Faktor lingkungan dan kondisi fisik yang dapat menjadi bagian dari pola data model.</div>
""", unsafe_allow_html=True)

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

# =========================================================
# INPUT — ACADEMIC
# =========================================================
st.markdown("""
<div class="section-card">
    <div class="section-heading">🎓 Faktor Akademik</div>
    <div class="section-description">Indikator yang berkaitan dengan pengalaman dan tuntutan akademik.</div>
""", unsafe_allow_html=True)

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

# =========================================================
# INPUT — SOCIAL
# =========================================================
st.markdown("""
<div class="section-card">
    <div class="section-heading">👥 Faktor Sosial</div>
    <div class="section-description">Indikator yang berkaitan dengan dukungan dan tekanan sosial.</div>
""", unsafe_allow_html=True)

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
st.markdown("<br>", unsafe_allow_html=True)

predict_button = st.button("🔮  PREDIKSI STRESS LEVEL", use_container_width=True)

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
        description = "Tingkat stres berada pada kategori rendah."
        result_class = "result-low"
        icon = "🟢"
    elif prediction == 1:
        stress_label = "Sedang"
        description = "Tingkat stres berada pada kategori sedang."
        result_class = "result-medium"
        icon = "🟠"
    else:
        stress_label = "Tinggi"
        description = "Tingkat stres berada pada kategori tinggi."
        result_class = "result-high"
        icon = "🔴"

    # =====================================================
    # RESULT
    # =====================================================
    confidence_html = ""
    if confidence is not None:
        confidence_html = f"""
        <div style="margin-top:20px;">
            <div style="display:flex;justify-content:space-between;font-size:12px;
                        font-weight:700;color:#737B8E;margin-bottom:7px;">
                <span>CONFIDENCE MODEL</span>
                <span>{confidence:.2f}%</span>
            </div>
        </div>
        """

    st.markdown(f"""
    <div class="result-card">
        <div class="result-kicker">Hasil Prediksi</div>
        <div class="result-value {result_class}">{icon} {stress_label}</div>
        <div class="result-desc">{description}</div>
        {confidence_html}
    </div>
    """, unsafe_allow_html=True)

    if confidence is not None:
        st.progress(
            min(int(confidence), 100),
            text=f"Confidence Model: {confidence:.2f}%"
        )

    # =====================================================
    # DETAIL
    # =====================================================
    st.markdown("### 📊 Detail Hasil")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Class Prediksi", str(prediction))
    with col2:
        st.metric("Kategori", stress_label)
    with col3:
        st.metric(
            "Confidence",
            f"{confidence:.2f}%" if confidence is not None else "N/A"
        )

    with st.expander("🔍 Lihat Data Input"):
        st.dataframe(input_data, use_container_width=True, hide_index=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    <b>🧠 MindCheck — Stress Level Predictor</b><br>
    Kelompok 5 • Project Psikologi • Random Forest Classification
</div>
""", unsafe_allow_html=True)
