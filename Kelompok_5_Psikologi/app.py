import streamlit as st
import pandas as pd
import pickle
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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    .main {
        background-color: #f7f9fc;
    }

    .title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .result-card {
        padding: 25px;
        border-radius: 18px;
        background-color: white;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin-top: 20px;
    }

    .result-title {
        font-size: 20px;
        font-weight: 600;
        color: #555;
    }

    .result-value {
        font-size: 42px;
        font-weight: 700;
        margin-top: 10px;
    }

    .info-card {
        padding: 18px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "stress_level.pkl")

    with open(model_path, "rb") as file:
        model = pickle.load(file)

    return model

model = load_model()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">🧠 Stress Level Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Prediksi tingkat stres mahasiswa menggunakan Random Forest Classification'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📌 Tentang Aplikasi")

    st.write(
        """
        Aplikasi ini menggunakan model **Random Forest Classification**
        untuk memprediksi tingkat stres berdasarkan beberapa faktor
        psikologis, akademik, sosial, dan lingkungan.
        """
    )

    st.divider()

    st.subheader("📊 Kategori Stress Level")

    st.write("**0 — Rendah**")
    st.write("**1 — Sedang**")
    st.write("**2 — Tinggi**")

    st.divider()

    st.caption("Machine Learning Project")
    st.caption("Random Forest Classification")


# =========================================================
# INPUT DATA
# =========================================================

st.subheader("📝 Masukkan Data Mahasiswa")

st.write(
    "Silakan masukkan nilai sesuai dengan kondisi mahasiswa."
)


# =========================================================
# PSYCHOLOGICAL FACTORS
# =========================================================

st.markdown("### 🧠 Faktor Psikologis")

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


# =========================================================
# PHYSICAL & ENVIRONMENT
# =========================================================

st.markdown("### 🏠 Kondisi Fisik & Lingkungan")

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


# =========================================================
# ACADEMIC FACTORS
# =========================================================

st.markdown("### 🎓 Faktor Akademik")

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


# =========================================================
# SOCIAL FACTORS
# =========================================================

st.markdown("### 👥 Faktor Sosial")

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

st.divider()

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

    prediction = model.predict(input_data)[0]


    # -----------------------------------------------------
    # PROBABILITY
    # -----------------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(input_data)[0]

        confidence = max(probabilities) * 100

    else:

        confidence = None


    # -----------------------------------------------------
    # LABEL PREDICTION
    # -----------------------------------------------------

    if prediction == 0:

        stress_label = "Rendah"
        description = (
            "Tingkat stres berada pada kategori rendah."
        )

    elif prediction == 1:

        stress_label = "Sedang"
        description = (
            "Tingkat stres berada pada kategori sedang."
        )

    else:

        stress_label = "Tinggi"
        description = (
            "Tingkat stres berada pada kategori tinggi."
        )


    # -----------------------------------------------------
    # HASIL
    # -----------------------------------------------------

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-title">Hasil Prediksi</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="result-value">{stress_label}</div>',
        unsafe_allow_html=True
    )

    st.write(description)

    if confidence is not None:

        st.progress(
            int(confidence),
            text=f"Confidence Model: {confidence:.2f}%"
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # DETAIL PREDIKSI
    # -----------------------------------------------------

    st.markdown("### 📊 Detail Hasil")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Class Prediksi",
            str(prediction)
        )

    with col2:

        st.metric(
            "Kategori",
            stress_label
        )

    with col3:

        if confidence is not None:

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

        else:

            st.metric(
                "Confidence",
                "N/A"
            )


    # -----------------------------------------------------
    # DATA INPUT
    # -----------------------------------------------------

    with st.expander("🔍 Lihat Data Input"):

        st.dataframe(
            input_data,
            use_container_width=True
        )
