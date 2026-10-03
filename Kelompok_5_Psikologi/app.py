import streamlit as st
import pandas as pd
import pickle
import joblIb
import os


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
# CUSTOM CSS  (tema gelap + glassmorphism + animasi)
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Poppins', sans-serif;
}

/* ---------- Background ---------- */
.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(99,102,241,0.35), transparent 40%),
        radial-gradient(circle at 85% 20%, rgba(236,72,153,0.28), transparent 40%),
        radial-gradient(circle at 50% 95%, rgba(20,184,166,0.25), transparent 45%),
        #0b1020;
    color: #e5e7eb;
}

header[data-testid="stHeader"] { background: transparent; }

.block-container { padding-top: 2rem; max-width: 1150px; }

/* ---------- Teks ---------- */
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp p, .stApp li, .stApp span, .stApp label {
    color: #e5e7eb;
}
[data-testid="stWidgetLabel"] p {
    color: #cbd5e1 !important;
    font-weight: 500;
}

/* ---------- Hero ---------- */
.hero {
    text-align: center;
    padding: 38px 20px 30px 20px;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(236,72,153,0.18));
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(14px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    margin-bottom: 28px;
}
.hero-emoji {
    font-size: 64px;
    display: inline-block;
    animation: float 3.5s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(-4deg); }
    50%      { transform: translateY(-12px) rotate(4deg); }
}
.hero-title {
    font-size: 46px;
    font-weight: 800;
    line-height: 1.15;
    background: linear-gradient(90deg, #818cf8, #f472b6, #2dd4bf, #818cf8);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 6s linear infinite;
}
@keyframes shine { to { background-position: 300% center; } }
.hero-sub {
    color: #cbd5e1;
    font-size: 17px;
    margin-top: 8px;
}
.badges { margin-top: 18px; }
.badge {
    display: inline-block;
    padding: 6px 14px;
    margin: 4px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 500;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    color: #e2e8f0;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.05);
    padding: 8px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    height: 46px;
    border-radius: 12px;
    padding: 0 18px;
    color: #94a3b8;
    font-weight: 600;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #ec4899) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ---------- Panel input ---------- */
.panel-title {
    font-size: 22px;
    font-weight: 700;
    margin: 18px 0 2px 0;
}
.panel-desc {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 14px;
}

/* ---------- Slider ---------- */
div[data-baseweb="slider"] div[role="slider"] {
    background: #ec4899 !important;
    box-shadow: 0 0 0 6px rgba(236,72,153,0.25);
}

/* ---------- Tombol ---------- */
.stButton > button {
    height: 60px;
    border: none;
    border-radius: 16px;
    font-size: 19px;
    font-weight: 700;
    color: white;
    background: linear-gradient(90deg, #6366f1, #ec4899, #f59e0b);
    background-size: 200% auto;
    transition: all .35s ease;
    box-shadow: 0 10px 30px rgba(236,72,153,0.35);
}
.stButton > button:hover {
    background-position: right center;
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 16px 40px rgba(236,72,153,0.5);
    color: white;
}

/* ---------- Kartu hasil ---------- */
.result-card {
    position: relative;
    overflow: hidden;
    padding: 36px 26px;
    border-radius: 28px;
    text-align: center;
    color: white;
    margin-top: 22px;
    box-shadow: 0 25px 70px rgba(0,0,0,0.45);
    animation: pop .6s cubic-bezier(.2,.9,.3,1.3);
}
@keyframes pop {
    from { opacity: 0; transform: scale(.85) translateY(20px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}
.result-emoji { font-size: 70px; }
.result-title {
    font-size: 15px;
    letter-spacing: 3px;
    text-transform: uppercase;
    opacity: .9;
    font-weight: 600;
}
.result-value {
    font-size: 58px;
    font-weight: 800;
    margin: 4px 0 6px 0;
}
.result-desc { font-size: 17px; opacity: .95; }

/* ---------- Glass card ---------- */
.glass {
    padding: 20px 22px;
    border-radius: 20px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    margin-bottom: 14px;
}
.glass h4 { margin: 0 0 10px 0; font-size: 17px; }

.prob-row { margin: 12px 0; }
.prob-head {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    margin-bottom: 5px;
    color: #e2e8f0;
}
.prob-bar {
    height: 12px;
    border-radius: 999px;
    background: rgba(255,255,255,0.1);
    overflow: hidden;
}
.prob-fill {
    height: 100%;
    border-radius: 999px;
}

.tip {
    padding: 10px 14px;
    margin: 8px 0;
    border-radius: 12px;
    background: rgba(255,255,255,0.06);
    border-left: 4px solid;
    font-size: 14px;
}

/* ---------- Metric ---------- */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 16px;
    border-radius: 18px;
}
[data-testid="stMetricValue"] { color: #fff; font-weight: 700; }
[data-testid="stMetricLabel"] p { color: #94a3b8 !important; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1e1b4b);
    border-right: 1px solid rgba(255,255,255,0.08);
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    margin: 8px 0;
    border-radius: 12px;
    background: rgba(255,255,255,0.06);
    font-size: 14px;
    font-weight: 500;
}
.dot { width: 12px; height: 12px; border-radius: 50%; }

.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 40px;
}

hr { border-color: rgba(255,255,255,0.1) !important; }

[data-testid="stExpander"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
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


model = load_model()


# =========================================================
# KONFIGURASI LEVEL
# =========================================================

LEVELS = {
    0: {
        "label": "Rendah",
        "emoji": "😌",
        "color": "#22c55e",
        "gradient": "linear-gradient(135deg, #16a34a, #14b8a6)",
        "desc": "Kondisi mental terpantau stabil. Pertahankan pola hidup sehatmu!",
        "tips": [
            "Pertahankan jam tidur yang teratur.",
            "Tetap aktif bersosialisasi dan berolahraga ringan.",
            "Luangkan waktu untuk hobi yang kamu sukai.",
        ],
    },
    1: {
        "label": "Sedang",
        "emoji": "😐",
        "color": "#f59e0b",
        "gradient": "linear-gradient(135deg, #f59e0b, #f97316)",
        "desc": "Ada beberapa tekanan yang perlu diperhatikan sebelum membesar.",
        "tips": [
            "Atur ulang jadwal belajar agar beban lebih seimbang.",
            "Coba teknik relaksasi atau pernapasan 5 menit setiap hari.",
            "Ceritakan beban pikiranmu ke teman atau keluarga.",
        ],
    },
    2: {
        "label": "Tinggi",
        "emoji": "😰",
        "color": "#ef4444",
        "gradient": "linear-gradient(135deg, #dc2626, #be185d)",
        "desc": "Tingkat stres tinggi. Sebaiknya segera cari dukungan yang tepat.",
        "tips": [
            "Pertimbangkan berbicara dengan konselor kampus atau psikolog.",
            "Prioritaskan istirahat dan kurangi beban yang tidak mendesak.",
            "Jangan memendam sendiri, hubungi orang yang kamu percaya.",
        ],
    },
}


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📌 Tentang Aplikasi")

    st.write(
        """
        Aplikasi ini memakai model **Random Forest Classification**
        untuk memprediksi tingkat stres berdasarkan faktor psikologis,
        fisik, akademik, dan sosial.
        """
    )

    st.divider()

    st.markdown("### 📊 Kategori Stress Level")

    for key, lv in LEVELS.items():
        st.markdown(
            f'<div class="legend-item">'
            f'<span class="dot" style="background:{lv["color"]}"></span>'
            f'{key} — {lv["label"]} {lv["emoji"]}'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.caption("⚠️ Hasil prediksi bukan diagnosis medis.")
    st.caption("Machine Learning Project • Random Forest")


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-emoji">🧠</div>
        <div class="hero-title">Stress Level Predictor</div>
        <div class="hero-sub">
            Prediksi tingkat stres mahasiswa dengan Machine Learning
        </div>
        <div class="badges">
            <span class="badge">🌲 Random Forest</span>
            <span class="badge">20 Fitur</span>
            <span class="badge">⚡ Prediksi Instan</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INPUT DATA (TAB)
# =========================================================

st.markdown(
    '<div class="panel-title">📝 Masukkan Data Mahasiswa</div>'
    '<div class="panel-desc">Geser slider di setiap tab sesuai kondisi mahasiswa.</div>',
    unsafe_allow_html=True
)

tab_psi, tab_fisik, tab_akademik, tab_sosial = st.tabs([
    "🧠 Psikologis",
    "🏠 Fisik & Lingkungan",
    "🎓 Akademik",
    "👥 Sosial"
])


# ---------------------------------------------------------
# PSYCHOLOGICAL FACTORS
# ---------------------------------------------------------

with tab_psi:

    col1, col2, col3 = st.columns(3)

    with col1:
        anxiety_level = st.slider(
            "Anxiety Level",
            min_value=0,
            max_value=21,
            value=10
        )

    with col2:
        self_esteem = st.slider(
            "Self Esteem",
            min_value=0,
            max_value=30,
            value=15
        )

    with col3:
        depression = st.slider(
            "Depression",
            min_value=0,
            max_value=27,
            value=10
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        mental_health_history = st.selectbox(
            "Mental Health History",
            options=[0, 1],
            format_func=lambda x:
                "Tidak" if x == 0 else "Ya"
        )

    with col2:
        headache = st.slider(
            "Headache",
            min_value=0,
            max_value=5,
            value=2
        )

    with col3:
        breathing_problem = st.slider(
            "Breathing Problem",
            min_value=0,
            max_value=5,
            value=2
        )


# ---------------------------------------------------------
# PHYSICAL & ENVIRONMENT
# ---------------------------------------------------------

with tab_fisik:

    col1, col2, col3 = st.columns(3)

    with col1:
        blood_pressure = st.slider(
            "Blood Pressure",
            min_value=1,
            max_value=3,
            value=2
        )

    with col2:
        sleep_quality = st.slider(
            "Sleep Quality",
            min_value=0,
            max_value=5,
            value=3
        )

    with col3:
        noise_level = st.slider(
            "Noise Level",
            min_value=0,
            max_value=5,
            value=2
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        living_conditions = st.slider(
            "Living Conditions",
            min_value=0,
            max_value=5,
            value=3
        )

    with col2:
        safety = st.slider(
            "Safety",
            min_value=0,
            max_value=5,
            value=3
        )

    with col3:
        basic_needs = st.slider(
            "Basic Needs",
            min_value=0,
            max_value=5,
            value=3
        )


# ---------------------------------------------------------
# ACADEMIC FACTORS
# ---------------------------------------------------------

with tab_akademik:

    col1, col2, col3 = st.columns(3)

    with col1:
        academic_performance = st.slider(
            "Academic Performance",
            min_value=0,
            max_value=5,
            value=3
        )

    with col2:
        study_load = st.slider(
            "Study Load",
            min_value=0,
            max_value=5,
            value=3
        )

    with col3:
        teacher_student_relationship = st.slider(
            "Teacher Student Relationship",
            min_value=0,
            max_value=5,
            value=3
        )

    col1, col2 = st.columns(2)

    with col1:
        future_career_concerns = st.slider(
            "Future Career Concerns",
            min_value=0,
            max_value=5,
            value=3
        )

    with col2:
        extracurricular_activities = st.slider(
            "Extracurricular Activities",
            min_value=0,
            max_value=5,
            value=3
        )


# ---------------------------------------------------------
# SOCIAL FACTORS
# ---------------------------------------------------------

with tab_sosial:

    col1, col2, col3 = st.columns(3)

    with col1:
        social_support = st.slider(
            "Social Support",
            min_value=0,
            max_value=3,
            value=2
        )

    with col2:
        peer_pressure = st.slider(
            "Peer Pressure",
            min_value=0,
            max_value=5,
            value=2
        )

    with col3:
        bullying = st.slider(
            "Bullying",
            min_value=0,
            max_value=5,
            value=1
        )


# =========================================================
# PREDICTION
# =========================================================

st.write("")

predict_button = st.button(
    "🔮 Prediksi Stress Level",
    use_container_width=True
)


if predict_button:

    # -----------------------------------------------------
    # MEMBUAT DATAFRAME INPUT
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    prediction = int(model.predict(input_data)[0])

    # -----------------------------------------------------
    # PROBABILITY
    # -----------------------------------------------------

    probabilities = None
    confidence = None

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(input_data)[0]
        confidence = max(probabilities) * 100

    level = LEVELS.get(prediction, LEVELS[2])

    # -----------------------------------------------------
    # KARTU HASIL
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="result-card" style="background:{level['gradient']};">
            <div class="result-emoji">{level['emoji']}</div>
            <div class="result-title">Hasil Prediksi</div>
            <div class="result-value">Stres {level['label']}</div>
            <div class="result-desc">{level['desc']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # -----------------------------------------------------
    # DETAIL: PROBABILITAS + SARAN
    # -----------------------------------------------------

    left, right = st.columns([1.1, 1])

    with left:

        rows = ""

        if probabilities is not None:

            classes = getattr(model, "classes_", range(len(probabilities)))

            for cls, prob in zip(classes, probabilities):

                lv = LEVELS.get(int(cls), LEVELS[2])
                pct = prob * 100

                rows += (
                    f'<div class="prob-row">'
                    f'<div class="prob-head">'
                    f'<span>{lv["emoji"]} {lv["label"]}</span>'
                    f'<span><b>{pct:.1f}%</b></span>'
                    f'</div>'
                    f'<div class="prob-bar">'
                    f'<div class="prob-fill" '
                    f'style="width:{pct:.1f}%;background:{lv["color"]};"></div>'
                    f'</div></div>'
                )

        else:
            rows = "<p>Probabilitas tidak tersedia untuk model ini.</p>"

        st.markdown(
            f'<div class="glass"><h4>📊 Distribusi Probabilitas</h4>{rows}</div>',
            unsafe_allow_html=True
        )

    with right:

        tips_html = "".join(
            f'<div class="tip" style="border-color:{level["color"]};">{t}</div>'
            for t in level["tips"]
        )

        st.markdown(
            f'<div class="glass"><h4>💡 Saran Untukmu</h4>{tips_html}</div>',
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # METRIC
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Class Prediksi", str(prediction))

    with col2:
        st.metric("Kategori", level["label"])

    with col3:
        st.metric(
            "Confidence",
            f"{confidence:.2f}%" if confidence is not None else "N/A"
        )

    # -----------------------------------------------------
    # DATA INPUT
    # -----------------------------------------------------

    with st.expander("🔍 Lihat Data Input"):

        st.dataframe(
            input_data,
            use_container_width=True
        )


st.markdown(
    '<div class="footer">Dibuat dengan ❤️ menggunakan Streamlit • '
    'Hasil prediksi bukan pengganti diagnosis profesional</div>',
    unsafe_allow_html=True
)
