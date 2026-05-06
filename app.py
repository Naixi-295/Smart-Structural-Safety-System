import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Structural Safety System",
    page_icon="🏗️",
    layout="wide"
)

# ------------------ PROFESSIONAL THEME ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
h1, h2, h3 {
    text-align: center;
    color: #00FFD1;
}
.sidebar .sidebar-content {
    background: #111;
}
.stButton>button {
    background-color: #00FFD1;
    color: black;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Smart Structural Safety System")
st.markdown("### ⚙️ ICT-Based Engineering Analysis Dashboard")

# ------------------ NAVIGATION ------------------
module = st.sidebar.radio("📂 Select Module", [
    "Beam Deflection & Safety",
    "Bridge Health Monitoring",
    "Crack Detection"
])

# =========================================================
# 🟢 MODULE 1: BEAM DEFLECTION
# =========================================================
if module == "Beam Deflection Predictor":
    st.title("📐 Smart Beam Deflection & Failure Predictor")

    L = st.number_input("Beam Length (m)", 1.0, 20.0, 5.0)
    F = st.number_input("Load (N)", 100.0, 50000.0, 1000.0)
    b = st.number_input("Beam Width (m)", 0.01, 1.0, 0.1)
    h = st.number_input("Beam Height (m)", 0.01, 1.0, 0.2)

    # ---------------- EXPANDED MATERIAL DATABASE ---------------- #
    materials = {
        "Structural Steel": {"E": 200e9, "density": 7850},
        "High Strength Steel (HSS)": {"E": 210e9, "density": 7850},
        "Reinforced Concrete": {"E": 30e9, "density": 2500},
        "Prestressed Concrete": {"E": 38e9, "density": 2450},

        "Aluminum Alloy 6061": {"E": 69e9, "density": 2700},
        "Titanium Alloy (Ti-6Al-4V)": {"E": 116e9, "density": 4500},

        "Carbon Fiber (CFRP)": {"E": 150e9, "density": 1600},
        "Kevlar Composite": {"E": 83e9, "density": 1440},

        "Glass Fiber Composite (GFRP)": {"E": 40e9, "density": 2000},

        "Wood (Timber - Pine)": {"E": 12e9, "density": 600},
        "Bamboo (Engineered)": {"E": 20e9, "density": 700},

        "Cast Iron": {"E": 100e9, "density": 7200},
        "Brass": {"E": 90e9, "density": 8500},
        "Copper": {"E": 110e9, "density": 8960},

        "Magnesium Alloy": {"E": 45e9, "density": 1800},
        "High Performance Polymer": {"E": 3e9, "density": 1200}
    }

    material = st.selectbox("Select Material", list(materials.keys()))
    E = materials[material]["E"]

    # ---------------- CALCULATIONS ---------------- #
    I = (b * h**3) / 12
    x = np.linspace(0, L, 100)
    deflection = (F * x * (3*L**2 - 4*x**2)) / (24 * E * I)

    max_deflection = np.max(deflection)

    # ---------------- VISUALIZATION ---------------- #
    st.subheader("📊 Deflection Curve")
    fig, ax = plt.subplots()
    ax.plot(x, deflection, linewidth=2)
    ax.set_title("Beam Deflection Diagram")
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Deflection (m)")
    st.pyplot(fig)

    # ---------------- ENGINEERING INTERPRETATION ---------------- #
    st.subheader("🧠 Engineering Analysis")

    stiffness_rank = E / 1e9  # GPa scale

    st.write(f"**Selected Material:** {material}")
    st.write(f"**Young's Modulus:** {stiffness_rank:.2f} GPa")

    if max_deflection > L / 250:
        st.error("❌ FAILURE RISK: Excessive deflection detected")
    elif max_deflection > L / 500:
        st.warning("⚠️ Moderate deflection – monitor design")
    else:
        st.success("✅ SAFE DESIGN – within elastic limit")

# =========================================================
# 🔵 MODULE 2: BRIDGE MONITORING (UPGRADED)
# =========================================================
elif module == "Bridge Health Monitoring":

    st.header("🌉 Bridge Health Monitoring Dashboard")

    # ----------- CONTROL FEATURE -----------
    st.sidebar.subheader("🎛️ Bridge Condition Control")

    condition = st.sidebar.slider(
        "Bridge Health Level (%)",
        0, 100, 80
    )

    t = np.arange(0, 50)

    # Dynamic simulation based on condition
    noise_level = (100 - condition) / 10

    strain = np.random.normal(40 + (100-condition)*0.3, noise_level*5, 50)
    vibration = np.random.normal(3 + (100-condition)*0.05, noise_level, 50)
    temperature = np.random.normal(30 + (100-condition)*0.1, 2, 50)

    # Status logic
    if condition > 70:
        status = "✅ HEALTHY"
        color = "green"
    elif condition > 40:
        status = "⚠️ MODERATE CONDITION"
        color = "orange"
    else:
        status = "❌ CRITICAL CONDITION"
        color = "red"

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Strain")
        fig1, ax1 = plt.subplots()
        ax1.plot(t, strain)
        ax1.set_title("Strain Variation")
        ax1.grid()
        st.pyplot(fig1)

        st.subheader("🌡 Temperature")
        fig2, ax2 = plt.subplots()
        ax2.plot(t, temperature)
        ax2.set_title("Temperature Variation")
        ax2.grid()
        st.pyplot(fig2)

    with col2:
        st.subheader("📊 Vibration")
        fig3, ax3 = plt.subplots()
        ax3.plot(t, vibration)
        ax3.set_title("Vibration Response")
        ax3.grid()
        st.pyplot(fig3)

        st.subheader("🚨 System Status")
        st.markdown(f"<h2 style='color:{color};'>{status}</h2>", unsafe_allow_html=True)

    st.markdown("---")
    st.metric("Bridge Health (%)", condition)
    st.metric("Avg Strain", f"{np.mean(strain):.2f}")
    st.metric("Avg Vibration", f"{np.mean(vibration):.2f}")
    st.metric("Avg Temperature", f"{np.mean(temperature):.2f}")

# =========================================================
# 🔴 MODULE 3: CRACK DETECTION
# =========================================================
elif module == "Crack Detection":

    st.header("🔍 Structural Crack Detection")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        img = np.array(image)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        crack_pixels = np.sum(edges > 0)
        total_pixels = edges.size

        severity = crack_pixels / total_pixels

        if severity < 0.01:
            status = "✅ SAFE"
            color = "green"
        elif severity < 0.03:
            status = "⚠️ MINOR CRACK"
            color = "orange"
        else:
            status = "❌ SEVERE CRACK"
            color = "red"

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Original Image")

        with col2:
            st.image(edges, caption="Detected Cracks")

        st.markdown(f"<h2 style='color:{color};'>{status}</h2>", unsafe_allow_html=True)
        st.metric("Crack Severity", f"{severity:.4f}")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("💡 Developed as ICT Project | BSc Mechanical Engineering")
