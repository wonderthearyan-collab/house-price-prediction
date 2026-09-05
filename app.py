import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# Folder this script lives in (so model files load correctly no matter
# what folder you launch "streamlit run" from)
APP_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(APP_DIR, "house_price_city_model.pkl"))
feature_columns = joblib.load(os.path.join(APP_DIR, "city_feature_columns.pkl"))

# =========================================================
# CUSTOM CSS
# NOTE: st.html() is used instead of st.markdown(unsafe_allow_html=True).
# Newer Streamlit versions sanitize <style> tags out of st.markdown, which
# makes raw CSS text show up on the page. st.html() renders it correctly.
# =========================================================
CUSTOM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* SMOOTH ANIMATED GRADIENT BACKGROUND (pure CSS, no image file needed) */
.stApp {
    background: linear-gradient(120deg, #1b1035, #2c1250, #4a1942, #7a2b4a, #a8455a, #d97b4f, #7a2b4a, #2c1250);
    background-size: 400% 400%;
    animation: gradientMove 22s ease infinite;
}

@keyframes gradientMove {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1150px;
}

/* ===== FONT ANIMATIONS ===== */
@keyframes textFadeIn {
    0% { opacity: 0; transform: translateY(12px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes glowPulse {
    0%, 100% { text-shadow: 0 0 6px rgba(255,255,255,0.15); }
    50% { text-shadow: 0 0 18px rgba(255,255,255,0.45); }
}

@keyframes gradientShift {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* Main title */
h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
    animation: textFadeIn 0.9s ease, glowPulse 4s ease-in-out infinite;
    letter-spacing: 0.5px;
}

/* Section headers */
h2 {
    color: #ffffff !important;
    font-weight: 700 !important;
    animation: textFadeIn 0.9s ease;
}

/* Body / caption / write text */
p, span, label, .stMarkdown, .stCaption {
    animation: textFadeIn 0.9s ease;
}

/* Input + widget labels */
.stNumberInput label p, .stSelectbox label p, .stCheckbox label p {
    color: rgba(255,255,255,0.92) !important;
    font-weight: 500 !important;
    animation: textFadeIn 0.7s ease;
}

/* Input boxes styling to sit well on the gradient background */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: #ffffff !important;
}

.stNumberInput input {
    background-color: rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: #ffffff !important;
}

/* Predict button */
div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #ff6a88 0%, #ff9a44 100%);
    color: #ffffff;
    font-size: 19px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 14px 0;
    border-radius: 14px;
    border: none;
    box-shadow: 0 8px 24px rgba(255,106,136,0.4);
    transition: all 0.3s ease;
    animation: textFadeIn 1s ease;
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 12px 32px rgba(255,154,68,0.55);
    color: #ffffff;
}

/* Success result box text */
div[data-testid="stAlert"] p {
    font-size: 19px !important;
    font-weight: 700 !important;
    animation: textFadeIn 0.8s ease, glowPulse 4s ease-in-out infinite;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.25) !important;
}

/* ===== ANIMATED CREDIT / FOOTER ===== */
.credit-container {
    text-align: center;
    margin-top: 15px;
}

.credit-name {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    background: linear-gradient(90deg, #ff6a88 0%, #ff9a44 35%, #43e97b 65%, #38f9d7 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s linear infinite, textFadeIn 1s ease;
    display: inline-block;
    transition: transform 0.3s ease;
}

.credit-name:hover {
    transform: scale(1.06);
}

.credit-sub {
    color: rgba(255,255,255,0.6);
    font-size: 13px;
    margin-top: 6px;
    animation: textFadeIn 1.1s ease;
}

</style>
"""

if hasattr(st, "html"):
    st.html(CUSTOM_CSS)
else:
    # Fallback for older Streamlit versions that don't have st.html yet
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("🏠 House Price Prediction")
st.write("Estimate house prices using a Machine Learning model.")

st.header("🏠 Basic House Details")

col1, col2, col3 = st.columns(3)

with col1:
    area = st.number_input(
        "📐 Area (sq.ft)",
        min_value=200,
        max_value=16000,
        value=1000,
        step=50
    )

with col2:
    bedrooms = st.number_input(
        "🛏️ No. of Bedrooms",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )

with col3:
    resale = st.selectbox(
        "🔄 Resale Property",
        ["No", "Yes"]
    )

st.header("🏙️ Location Details")

city = st.selectbox(
    "Select City",
    ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]
)

st.header("✨ Property Features & Amenities")

feature_list = [
    ("MaintenanceStaff", "👨‍🔧 Maintenance Staff"),
    ("Gymnasium", "🏋️ Gymnasium"),
    ("SwimmingPool", "🏊 Swimming Pool"),
    ("LandscapedGardens", "🌳 Landscaped Gardens"),
    ("JoggingTrack", "🏃 Jogging Track"),
    ("RainWaterHarvesting", "💧 Rain Water Harvesting"),
    ("IndoorGames", "🎮 Indoor Games"),
    ("ShoppingMall", "🛍️ Shopping Mall"),
    ("Intercom", "📞 Intercom"),
    ("SportsFacility", "⚽ Sports Facility"),
    ("ATM", "🏧 ATM"),
    ("ClubHouse", "🏛️ Club House"),
    ("School", "🏫 School"),
    ("24X7Security", "🔐 24X7 Security"),
    ("PowerBackup", "🔋 Power Backup"),
    ("CarParking", "🚗 Car Parking"),
    ("StaffQuarter", "👨‍💼 Staff Quarter"),
    ("Cafeteria", "☕ Cafeteria"),
    ("MultipurposeRoom", "🏠 Multipurpose Room"),
    ("Hospital", "🏥 Hospital"),
    ("WashingMachine", "🧺 Washing Machine"),
    ("Gasconnection", "🔥 Gas Connection"),
    ("AC", "❄️ Air Conditioner"),
    ("Wifi", "📶 WiFi"),
    ("Children'splayarea", "🧒 Children's Play Area"),
    ("LiftAvailable", "🛗 Lift Available"),
    ("BED", "🛏️ BED"),
    ("VaastuCompliant", "🕉️ Vaastu Compliant"),
    ("Microwave", "📡 Microwave"),
    ("GolfCourse", "⛳ Golf Course"),
    ("TV", "📺 TV"),
    ("DiningTable", "🍽️ Dining Table"),
    ("Sofa", "🛋️ Sofa"),
    ("Wardrobe", "👔 Wardrobe"),
    ("Refrigerator", "🧊 Refrigerator")
]

feature_cols = st.columns(3)
feature_values = {}

for index, (feature_name, feature_label) in enumerate(feature_list):
    with feature_cols[index % 3]:
        feature_values[feature_name] = int(
            st.checkbox(feature_label, value=False)
        )

input_data = {
    "Area": area,
    "No. of Bedrooms": bedrooms,
    "Resale": 1 if resale == "Yes" else 0
}

for feature_name, _ in feature_list:
    input_data[feature_name] = feature_values[feature_name]

city_columns = [
    "City_Chennai",
    "City_Delhi",
    "City_Hyderabad",
    "City_Kolkata",
    "City_Mumbai"
]

for column in city_columns:
    input_data[column] = int(
        city == column.replace("City_", "")
    )

st.write("")

if st.button("🔮 Predict House Price", type="primary"):

    input_df = pd.DataFrame([input_data])

    input_df = input_df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    predicted_price = model.predict(input_df)[0]

    st.success(
        f"Estimated House Price: ₹{predicted_price:,.0f}"
    )

    st.write(
        f"📍 **City:** {city}  |  "
        f"📐 **Area:** {area:,.0f} sq.ft  |  "
        f"🛏️ **Bedrooms:** {bedrooms}"
    )

st.divider()

credit_html = """
<div class="credit-container">
    <div class="credit-name">Aryan Prajapati</div>
    <div class="credit-sub">House Price Prediction • Machine Learning Project</div>
</div>
"""

if hasattr(st, "html"):
    st.html(credit_html)
else:
    st.markdown(credit_html, unsafe_allow_html=True)
