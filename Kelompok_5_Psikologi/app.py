import pickle
import joblib
import os
import pandas as pd
import streamlit as st

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Stress Level Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def html(s: str) -> str:
    """Rapatkan HTML jadi satu baris supaya tidak dibaca sebagai code block."""
    return " ".join(line.strip() for line in s.strip().splitlines())


# =========================================================
# CUSTOM CSS  (terang, hangat, kuning ala Saweria)
# =========================================================

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --y: #FAAE2B;
    --yd: #D98A00;
    --ink: #1F2937;
    --muted: #6B7280;
    --line: #F1E7D3;
}

.stApp, .stApp p, .stApp label, .stMarkdown, .stButton button,
[data-testid="stWidgetLabel"], .stTabs button {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background-color: #FFF9EE;
    background-image: radial-gradient(#F3E3BE 1.3px, transparent 1.3px);
    background-size: 24px 24px;
    color: var(--ink);
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1080px; padding-top: 1.2rem; padding-bottom: 4rem; }

.stApp p, .stApp label, .stApp li { color: var(--ink); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--ink) !important; }

/* ---------- Navbar ---------- */
.nav {
    display: flex; justify-content: space-between; align-items: center;
    background: #fff; border: 1px solid var(--line); border-radius: 999px;
    padding: 10px 12px 10px 20px;
    box-shadow: 0 6px 24px rgba(217,138,0,.08);
    margin-bottom: 30px;
}
.brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 18px; color: var(--ink); }
.logo {
    width: 36px; height: 36px; border-radius: 12px; background: var(--y);
    display: grid; place-items: center; font-size: 20px;
}
.nav-pill {
    background: #FFF3D6; color: #9A5B00; font-weight: 700; font-size: 13px;
    padding: 8px 16px; border-radius: 999px;
}

/* ---------- Hero ---------- */
.hero {
    display: grid; grid-template-columns: 1.25fr 1fr; gap: 30px;
    align-items: center; margin-bottom: 34px;
}
.eyebrow {
    display: inline-block; background: #FFF3D6; color: #9A5B00;
    font-weight: 700; font-size: 13px; padding: 7px 14px;
    border-radius: 999px; margin-bottom: 16px;
}
.hero h1 {
    font-size: 54px; line-height: 1.08; font-weight: 800;
    margin: 0 0 16px 0; letter-spacing: -1.5px; padding: 0;
}
.hl {
    background: linear-gradient(transparent 58%, var(--y) 58%);
    padding: 0 4px;
}
.hero-text { font-size: 18px; color: var(--muted); max-width: 520px; line-height: 1.6; }
.hero-cards { position: relative; height: 300px; }
.fcard {
    position: absolute; background: #fff; border: 1px solid var(--line);
    border-radius: 22px; padding: 16px 22px; display: flex;
    align-items: center; gap: 14px; min-width: 240px;
    box-shadow: 0 14px 34px rgba(31,41,55,.10);
}
.fcard .em { font-size: 36px; }
.fcard b { display: block; font-size: 17px; color: var(--ink); }
.fcard small { font-size: 13px; color: var(--muted); }
.f1 { top: 0;     left: 20px; transform: rotate(-4deg); animation: bob 4s ease-in-out infinite; }
.f2 { top: 98px;  left: 90px; transform: rotate(3deg);  animation: bob 4.6s ease-in-out infinite .4s; }
.f3 { top: 196px; left: 10px; transform: rotate(-2deg); animation: bob 5.2s ease-in-out infinite .8s; }
@keyframes bob { 50% { translate: 0 -10px; } }

/* ---------- Langkah ---------- */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 38px; }
.step {
    background: #fff; border: 1px solid var(--line); border-radius: 20px;
    padding: 20px; box-shadow: 0 8px 24px rgba(217,138,0,.06);
}
.num {
    width: 34px; height: 34px; border-radius: 50%; background: var(--y);
    display: grid; place-items: center; font-weight: 800; margin-bottom: 10px; color: var(--ink);
}
.step b { font-size: 16px; display: block; margin-bottom: 4px; color: var(--ink); }
.step small { color: var(--muted); font-size: 14px; }

/* ---------- Judul seksi ---------- */
.sec-title { font-size: 28px; font-weight: 800; margin: 6px 0 2px 0; letter-spacing: -.5px; color: var(--ink); }
.sec-sub { color: var(--muted); margin-bottom: 14px; font-size: 15px; }

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; padding: 4px 0; flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] {
    height: 46px; padding: 0 20px; border-radius: 999px; background: #fff;
    border: 1.5px solid var(--line); color: var(--muted); font-weight: 700;
}
.stTabs [aria-selected="true"] {
    background: var(--y) !important; border-color: var(--y) !important; color: var(--ink) !important;
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
.stTabs [data-baseweb="tab-panel"] {
    background: #fff; border: 1px solid var(--line); border-radius: 24px;
    padding: 26px 26px 12px 26px; margin-top: 12px;
    box-shadow: 0 12px 34px rgba(217,138,0,.08);
}

/* ---------- Input ---------- */
[data-testid="stWidgetLabel"] p { font-weight: 700; color: var(--ink) !important; }
[data-testid="stSlider"] [role="slider"] {
    background: var(--y) !important; border: 3px solid #fff !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.25) !important;
}
[data-testid="stThumbValue"] { color: #B45309 !important; font-weight: 800; }
div[data-baseweb="select"] > div {
    background: #fff; border-radius: 14px; border: 1.5px solid var(--line); color: var(--ink);
}

/* ---------- Tombol ---------- */
[data-testid="stBaseButton-secondary"], .stButton > button[kind="secondary"] {
    background: #fff; color: var(--ink); border: 1.5px solid var(--line);
    border-radius: 999px; font-weight: 700; height: 46px; transition: all .2s ease;
}
[data-testid="stBaseButton-secondary"]:hover, .stButton > button[kind="secondary"]:hover {
    border-color: var(--y); background: #FFF3D6; color: var(--ink);
}
[data-testid="stBaseButton-primary"], .stButton > button[kind="primary"] {
    background: var(--y); color: var(--ink); border: 2px solid var(--ink);
    border-radius: 16px; height: 62px; font-size: 19px; font-weight: 800;
    box-shadow: 0 5px 0 var(--ink); transition: all .12s ease;
}
[data-testid="stBaseButton-primary"]:hover, .stButton > button[kind="primary"]:hover {
    background: #FFBC4D; color: var(--ink); border-color: var(--ink);
    transform: translateY(2px); box-shadow: 0 3px 0 var(--ink);
}
[data-testid="stBaseButton-primary"]:active, .stButton > button[kind="primary"]:active {
    transform: translateY(5px); box-shadow: 0 0 0 var(--ink);
}

/* ---------- Hasil ---------- */
.res {
    display: grid; grid-template-columns: .9fr 1.1fr; gap: 18px;
    margin-top: 30px; animation: pop .5s ease;
}
@keyframes pop {
    from { opacity: 0; transform: translateY(18px) scale(.98); }
    to   { opacity: 1; transform: none; }
}
.card {
    background: #fff; border: 1px solid var(--line); border-radius: 24px;
    padding: 26px; box-shadow: 0 12px 34px rgba(217,138,0,.08);
}
.card + .card { margin-top: 18px; }
.card h4 { margin: 0 0 14px 0; font-size: 17px; font-weight: 800; }
.stack { display: flex; flex-direction: column; }
.res-main { text-align: center; }
.donut {
    width: 190px; height: 190px; border-radius: 50%;
    margin: 6px auto 18px auto; display: grid; place-items: center;
}
.donut-in {
    width: 146px; height: 146px; border-radius: 50%; background: #fff;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.donut-em { font-size: 46px; line-height: 1; }
.donut-pct { font-weight: 800; font-size: 22px; margin-top: 4px; color: var(--ink); }
.badge-lv { display: inline-block; padding: 8px 22px; border-radius: 999px; font-weight: 800; font-size: 22px; }
.res-desc { color: var(--muted); margin-top: 12px; font-size: 15px; line-height: 1.55; }
.chips { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-top: 16px; }
.chip {
    background: #FFF9EE; border: 1px solid var(--line); border-radius: 999px;
    padding: 6px 14px; font-size: 13px; font-weight: 700; color: var(--ink);
}
.bar-row { margin: 14px 0; }
.bar-head { display: flex; justify-content: space-between; font-size: 14px; font-weight: 700; margin-bottom: 6px; color: var(--ink); }
.bar { height: 12px; background: #F3F4F6; border-radius: 999px; overflow: hidden; }
.bar > div { height: 100%; border-radius: 999px; }
.tip {
    display: flex; gap: 12px; align-items: flex-start; padding: 12px 14px;
    border-radius: 14px; background: #FFF9EE; margin: 10px 0;
    font-size: 14px; line-height: 1.5; color: var(--ink);
}
.tip i { font-style: normal; font-size: 18px; }

/* ---------- Footer ---------- */
.foot { text-align: center; color: var(--muted); font-size: 13px; margin-top: 46px; }
.legend { display: flex; justify-content: center; gap: 10px; margin-bottom: 12px; flex-wrap: wrap; }
.lg {
    background: #fff; border: 1px solid var(--line); border-radius: 999px;
    padding: 6px 14px; font-weight: 700; font-size: 13px; color: var(--ink);
}

[data-testid="stExpander"] {
    background: #fff; border: 1px solid var(--line); border-radius: 18px;
}

@media (max-width: 800px) {
    .hero, .res, .steps { grid-template-columns: 1fr; }
    .hero h1 { font-size: 36px; }
    .hero-cards { display: none; }
}
"""

st.markdown("<style>" + html(CSS) + "</style>", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "stress_level.pkl")
    return joblib.load(model_path)

model = load_model()


# =========================================================
# DATA & KONFIGURASI
# =========================================================

# Urutan ini sama persis dengan urutan kolom saat model dilatih
FEATURES = [
    "anxiety_level", "self_esteem", "mental_health_history", "depression",
    "headache", "blood_pressure", "sleep_quality", "breathing_problem",
    "noise_level", "living_conditions", "safety", "basic_needs",
    "academic_performance", "study_load", "teacher_student_relationship",
    "future_career_concerns", "social_support", "peer_pressure",
    "extracurricular_activities", "bullying",
]

DEFAULTS = {
    "anxiety_level": 10, "self_esteem": 15, "mental_health_history": 0,
    "depression": 10, "headache": 2, "blood_pressure": 2, "sleep_quality": 3,
    "breathing_problem": 2, "noise_level": 2, "living_conditions": 3,
    "safety": 3, "basic_needs": 3, "academic_performance": 3, "study_load": 3,
    "teacher_student_relationship": 3, "future_career_concerns": 3,
    "social_support": 2, "peer_pressure": 2, "extracurricular_activities": 3,
    "bullying": 1,
}

PRESETS = {
    "Santai": {
        "anxiety_level": 4, "self_esteem": 26, "mental_health_history": 0,
        "depression": 3, "headache": 0, "blood_pressure": 1, "sleep_quality": 5,
        "breathing_problem": 0, "noise_level": 1, "living_conditions": 5,
        "safety": 5, "basic_needs": 5, "academic_performance": 4, "study_load": 1,
        "teacher_student_relationship": 4, "future_career_concerns": 1,
        "social_support": 3, "peer_pressure": 1, "extracurricular_activities": 3,
        "bullying": 0,
    },
    "Biasa": dict(DEFAULTS),
    "Tertekan": {
        "anxiety_level": 19, "self_esteem": 6, "mental_health_history": 1,
        "depression": 22, "headache": 4, "blood_pressure": 3, "sleep_quality": 1,
        "breathing_problem": 4, "noise_level": 4, "living_conditions": 1,
        "safety": 1, "basic_needs": 1, "academic_performance": 1, "study_load": 5,
        "teacher_student_relationship": 1, "future_career_concerns": 5,
        "social_support": 0, "peer_pressure": 4, "extracurricular_activities": 0,
        "bullying": 4,
    },
}

LEVELS = {
    0: {
        "label": "Rendah", "emoji": "😌",
        "color": "#16A34A", "bg": "#DCFCE7", "fg": "#166534",
        "desc": "Kondisi mental terpantau stabil. Pertahankan pola hidup sehatmu!",
        "tips": [
            ("😴", "Pertahankan jam tidur yang teratur."),
            ("🏃", "Tetap aktif bersosialisasi dan berolahraga ringan."),
            ("🎨", "Luangkan waktu untuk hobi yang kamu sukai."),
        ],
    },
    1: {
        "label": "Sedang", "emoji": "😐",
        "color": "#F59E0B", "bg": "#FEF3C7", "fg": "#92400E",
        "desc": "Ada beberapa tekanan yang perlu diperhatikan sebelum membesar.",
        "tips": [
            ("🗓️", "Atur ulang jadwal belajar agar beban lebih seimbang."),
            ("🌬️", "Coba teknik pernapasan 5 menit setiap hari."),
            ("💬", "Ceritakan beban pikiranmu ke teman atau keluarga."),
        ],
    },
    2: {
        "label": "Tinggi", "emoji": "😰",
        "color": "#EF4444", "bg": "#FEE2E2", "fg": "#991B1B",
        "desc": "Tingkat stres tinggi. Sebaiknya segera cari dukungan yang tepat.",
        "tips": [
            ("🩺", "Pertimbangkan bicara dengan konselor kampus atau psikolog."),
            ("🛌", "Prioritaskan istirahat dan kurangi beban yang tidak mendesak."),
            ("🤝", "Jangan dipendam sendiri, hubungi orang yang kamu percaya."),
        ],
    },
}

# Nilai awal widget (hanya diisi sekali)
for _k, _v in DEFAULTS.items():
    st.session_state.setdefault(_k, _v)


def apply_preset(name: str):
    for k, v in PRESETS[name].items():
        st.session_state[k] = v


# =========================================================
# NAVBAR + HERO
# =========================================================

st.markdown(html("""
<div class="nav">
    <div class="brand"><div class="logo">🧠</div> Stress Level Predictor</div>
    <div class="nav-pill">🌲 Random Forest • 20 Fitur</div>
</div>

<div class="hero">
    <div>
        <div class="eyebrow">✨ Gratis &amp; instan</div>
        <h1>Seberapa <span class="hl">stres</span> kamu hari ini?</h1>
        <div class="hero-text">
            Isi beberapa faktor tentang kondisi mahasiswa, lalu model Random Forest
            akan memprediksi tingkat stresnya: Rendah, Sedang, atau Tinggi.
        </div>
    </div>
    <div class="hero-cards">
        <div class="fcard f1"><span class="em">😌</span><div><b>Rendah</b><small>Kelas 0 • Aman terkendali</small></div></div>
        <div class="fcard f2"><span class="em">😐</span><div><b>Sedang</b><small>Kelas 1 • Perlu diperhatikan</small></div></div>
        <div class="fcard f3"><span class="em">😰</span><div><b>Tinggi</b><small>Kelas 2 • Butuh dukungan</small></div></div>
    </div>
</div>

<div class="steps">
    <div class="step"><div class="num">1</div><b>Isi data</b><small>Geser slider di 4 kategori faktor.</small></div>
    <div class="step"><div class="num">2</div><b>Klik prediksi</b><small>Model langsung menghitung hasilnya.</small></div>
    <div class="step"><div class="num">3</div><b>Lihat hasil</b><small>Level stres, probabilitas, dan saran.</small></div>
</div>
"""), unsafe_allow_html=True)


# =========================================================
# INPUT DATA
# =========================================================

st.markdown(html("""
<div class="sec-title">📝 Masukkan Data Mahasiswa</div>
<div class="sec-sub">Atur sendiri tiap slider, atau coba contoh cepat dulu.</div>
"""), unsafe_allow_html=True)

p1, p2, p3, _ = st.columns([1, 1, 1, 1.4])
p1.button("😌 Contoh Santai", on_click=apply_preset, args=("Santai",), use_container_width=True, key="btn_santai")
p2.button("😐 Contoh Biasa", on_click=apply_preset, args=("Biasa",), use_container_width=True, key="btn_biasa")
p3.button("😰 Contoh Tertekan", on_click=apply_preset, args=("Tertekan",), use_container_width=True, key="btn_tertekan")


def slider(label, key, lo, hi, tip):
    return st.slider(label, min_value=lo, max_value=hi, key=key, help=tip)


tab_psi, tab_fisik, tab_akademik, tab_sosial = st.tabs([
    "🧠 Psikologis",
    "🏠 Fisik & Lingkungan",
    "🎓 Akademik",
    "👥 Sosial",
])

# ---------- Psikologis ----------
with tab_psi:
    c1, c2, c3 = st.columns(3)
    with c1:
        slider("Anxiety Level", "anxiety_level", 0, 21, "0 = tenang, 21 = sangat cemas")
    with c2:
        slider("Self Esteem", "self_esteem", 0, 30, "0 = rendah, 30 = sangat percaya diri")
    with c3:
        slider("Depression", "depression", 0, 27, "0 = tidak ada, 27 = sangat berat")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox(
            "Mental Health History",
            options=[0, 1],
            key="mental_health_history",
            format_func=lambda x: "Tidak" if x == 0 else "Ya",
        )
    with c2:
        slider("Headache", "headache", 0, 5, "Seberapa sering sakit kepala (0–5)")
    with c3:
        slider("Breathing Problem", "breathing_problem", 0, 5, "Seberapa sering sesak napas (0–5)")

# ---------- Fisik & Lingkungan ----------
with tab_fisik:
    c1, c2, c3 = st.columns(3)
    with c1:
        slider("Blood Pressure", "blood_pressure", 1, 3, "1 = rendah, 3 = tinggi")
    with c2:
        slider("Sleep Quality", "sleep_quality", 0, 5, "0 = buruk, 5 = sangat baik")
    with c3:
        slider("Noise Level", "noise_level", 0, 5, "0 = tenang, 5 = sangat bising")

    c1, c2, c3 = st.columns(3)
    with c1:
        slider("Living Conditions", "living_conditions", 0, 5, "0 = buruk, 5 = sangat baik")
    with c2:
        slider("Safety", "safety", 0, 5, "0 = tidak aman, 5 = sangat aman")
    with c3:
        slider("Basic Needs", "basic_needs", 0, 5, "0 = kurang terpenuhi, 5 = terpenuhi")

# ---------- Akademik ----------
with tab_akademik:
    c1, c2, c3 = st.columns(3)
    with c1:
        slider("Academic Performance", "academic_performance", 0, 5, "0 = rendah, 5 = sangat baik")
    with c2:
        slider("Study Load", "study_load", 0, 5, "0 = ringan, 5 = sangat berat")
    with c3:
        slider("Teacher Student Relationship", "teacher_student_relationship", 0, 5, "0 = buruk, 5 = sangat baik")

    c1, c2 = st.columns(2)
    with c1:
        slider("Future Career Concerns", "future_career_concerns", 0, 5, "0 = tidak khawatir, 5 = sangat khawatir")
    with c2:
        slider("Extracurricular Activities", "extracurricular_activities", 0, 5, "0 = tidak ikut, 5 = sangat aktif")

# ---------- Sosial ----------
with tab_sosial:
    c1, c2, c3 = st.columns(3)
    with c1:
        slider("Social Support", "social_support", 0, 3, "0 = tidak ada, 3 = sangat besar")
    with c2:
        slider("Peer Pressure", "peer_pressure", 0, 5, "0 = tidak ada, 5 = sangat besar")
    with c3:
        slider("Bullying", "bullying", 0, 5, "0 = tidak pernah, 5 = sangat sering")


# =========================================================
# PREDIKSI
# =========================================================

st.write("")

predict_button = st.button(
    "🔮 Prediksi Stress Level",
    type="primary",
    use_container_width=True,
)

if predict_button:

    # -----------------------------------------------------
    # DATAFRAME INPUT (urutan kolom sama seperti sebelumnya)
    # -----------------------------------------------------

    input_data = pd.DataFrame([{k: st.session_state[k] for k in FEATURES}])

    # -----------------------------------------------------
    # PREDIKSI + PROBABILITAS
    # -----------------------------------------------------

    prediction = int(model.predict(input_data)[0])

    probabilities = None
    confidence = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        confidence = max(probabilities) * 100

    level = LEVELS.get(prediction, LEVELS[2])
    pct_main = confidence if confidence is not None else 100

    # -----------------------------------------------------
    # BAR PROBABILITAS
    # -----------------------------------------------------

    if probabilities is not None:
        classes = getattr(model, "classes_", range(len(probabilities)))
        rows = ""
        for cls, prob in zip(classes, probabilities):
            lv = LEVELS.get(int(cls), LEVELS[2])
            p = prob * 100
            rows += (
                f'<div class="bar-row">'
                f'<div class="bar-head"><span>{lv["emoji"]} {lv["label"]}</span><span>{p:.1f}%</span></div>'
                f'<div class="bar"><div style="width:{p:.1f}%;background:{lv["color"]};"></div></div>'
                f'</div>'
            )
    else:
        rows = "<p>Probabilitas tidak tersedia untuk model ini.</p>"

    # -----------------------------------------------------
    # SARAN
    # -----------------------------------------------------

    tips_html = "".join(
        f'<div class="tip"><i>{icon}</i><span>{text}</span></div>'
        for icon, text in level["tips"]
    )

    # -----------------------------------------------------
    # KARTU HASIL
    # -----------------------------------------------------

    conf_text = f"{confidence:.1f}%" if confidence is not None else "N/A"

    st.markdown(html(f"""
    <div class="res">
        <div class="card res-main">
            <div class="donut" style="background:conic-gradient({level['color']} {pct_main:.1f}%, #F3F4F6 0);">
                <div class="donut-in">
                    <div class="donut-em">{level['emoji']}</div>
                    <div class="donut-pct">{conf_text}</div>
                </div>
            </div>
            <div class="badge-lv" style="background:{level['bg']};color:{level['fg']};">Stres {level['label']}</div>
            <div class="res-desc">{level['desc']}</div>
            <div class="chips">
                <span class="chip">Class: {prediction}</span>
                <span class="chip">Kategori: {level['label']}</span>
                <span class="chip">Confidence: {conf_text}</span>
            </div>
        </div>
        <div class="stack">
            <div class="card"><h4>📊 Distribusi Probabilitas</h4>{rows}</div>
            <div class="card"><h4>💡 Saran Untukmu</h4>{tips_html}</div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # -----------------------------------------------------
    # FAKTOR PALING BERPENGARUH (kalau model mendukung)
    # -----------------------------------------------------

    if hasattr(model, "feature_importances_"):

        names = list(getattr(model, "feature_names_in_", input_data.columns))
        imps = list(model.feature_importances_)

        if len(names) == len(imps):
            top = sorted(zip(names, imps), key=lambda x: x[1], reverse=True)[:6]
            max_imp = top[0][1] if top[0][1] > 0 else 1
            imp_rows = ""
            for name, imp in top:
                nice = str(name).replace("_", " ").title()
                imp_rows += (
                    f'<div class="bar-row">'
                    f'<div class="bar-head"><span>{nice}</span><span>{imp * 100:.1f}%</span></div>'
                    f'<div class="bar"><div style="width:{imp / max_imp * 100:.1f}%;background:#FAAE2B;"></div></div>'
                    f'</div>'
                )

            st.markdown(html(f"""
            <div class="card" style="margin-top:18px;">
                <h4>🔎 Faktor Paling Berpengaruh pada Model</h4>
                {imp_rows}
            </div>
            """), unsafe_allow_html=True)

    st.write("")

    with st.expander("🔍 Lihat Data Input"):
        st.dataframe(input_data, use_container_width=True)

    if prediction == 0:
        st.balloons()


# =========================================================
# FOOTER
# =========================================================

legend = "".join(
    f'<span class="lg">{k} — {v["label"]} {v["emoji"]}</span>' for k, v in LEVELS.items()
)

st.markdown(html(f"""
<div class="foot">
    <div class="legend">{legend}</div>
    Dibuat dengan ❤️ memakai Streamlit • Hasil prediksi bukan diagnosis medis,
    silakan temui profesional bila kamu butuh bantuan.
</div>
"""), unsafe_allow_html=True)
