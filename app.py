import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load("house_price_real_model_small.pkl")
feature_columns = joblib.load("real_feature_columns.pkl")

# -----------------------------
    
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom CSS / Design
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(116, 82, 255, 0.20), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(0, 210, 255, 0.18), transparent 30%),
        linear-gradient(135deg, #eef5ff 0%, #f8f1ff 50%, #eefaff 100%);
}

/* Cartoon city/building background */
.stApp::before {
    content: "🏠  🏢  🏙️  🏠  🏢  🏙️  🏠  🏢  🏙️";
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    height: 130px;
    font-size: 65px;
    letter-spacing: 15px;
    opacity: 0.10;
    white-space: nowrap;
    overflow: hidden;
    text-align: center;
    pointer-events: none;
    z-index: 0;
}

/* Main content above background */
.main .block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Main title */
.hero-title {
    text-align: center;
    padding: 35px 20px;
    margin-bottom: 25px;
    border-radius: 30px;
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.8);
    box-shadow:
        0 15px 45px rgba(60, 50, 150, 0.15),
        inset 0 0 30px rgba(255,255,255,0.5);
    transition: all 0.35s ease;
}

.hero-title:hover {
    transform: translateY(-5px);
    box-shadow:
        0 20px 55px rgba(85, 60, 200, 0.25),
        0 0 35px rgba(125, 85, 255, 0.15);
}

.hero-title h1 {
    font-size: 3.3rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(90deg, #182b8c, #6538e8, #b329e8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-title p {
    font-size: 1.1rem;
    color: #445070;
    margin-top: 10px;
}

/* Section cards */
.section-card {
    background: rgba(255,255,255,0.76);
    backdrop-filter: blur(18px);
    border-radius: 25px;
    padding: 25px 30px 30px 30px;
    margin: 25px 0;
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 12px 40px rgba(54, 44, 120, 0.13);
    transition: all 0.35s ease;
}

.section-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 18px 50px rgba(70, 50, 180, 0.20),
        0 0 25px rgba(130, 80, 255, 0.10);
}

/* Section heading */
.section-heading {
    font-size: 1.65rem;
    font-weight: 700;
    color: #17236e;
    margin-bottom: 20px;
    border-bottom: 3px solid #8b5cf6;
    padding-bottom: 10px;
}

/* Input labels */
label {
    font-weight: 600 !important;
    color: #202b63 !important;
}

/* Number input and selectbox */
div[data-baseweb="input"],
div[data-baseweb="select"] {
    border-radius: 14px !important;
}

/* Input hover */
div[data-baseweb="input"]:hover,
div[data-baseweb="select"]:hover {
    box-shadow: 0 0 15px rgba(105, 75, 230, 0.25);
    transition: 0.25s ease;
}

/* Checkbox hover */
div[data-testid="stCheckbox"] {
    padding: 6px 10px;
    border-radius: 12px;
    transition: all 0.25s ease;
}

div[data-testid="stCheckbox"]:hover {
    background: rgba(130, 90, 255, 0.08);
    transform: translateX(4px);
}

/* Predict button */
.stButton > button {
    width: 100%;
    min-height: 65px;
    border: none;
    border-radius: 18px;
    color: white;
    font-size: 1.25rem;
    font-weight: 700;
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #c026d3
    );
    box-shadow:
        0 8px 25px rgba(91, 60, 220, 0.35),
        0 0 18px rgba(130, 70, 255, 0.25);
    transition: all 0.30s ease;
}

.stButton > button:hover {
    transform: translateY(-5px) scale(1.015);
    box-shadow:
        0 14px 35px rgba(91, 60, 220, 0.45),
        0 0 35px rgba(170, 80, 255, 0.50);
}

.stButton > button:active {
    transform: scale(0.97);
}

/* Prediction result */
.result-card {
    margin-top: 25px;
    padding: 30px;
    border-radius: 25px;
    background: linear-gradient(
        135deg,
        rgba(220,255,235,0.95),
        rgba(240,255,248,0.95)
    );
    border: 2px solid rgba(40, 200, 100, 0.35);
    box-shadow:
        0 12px 40px rgba(30, 150, 80, 0.15),
        0 0 25px rgba(50, 220, 120, 0.12);
    text-align: center;
    animation: resultAppear 0.6s ease;
}

.result-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #176b3a;
}

.result-price {
    font-size: 2.8rem;
    font-weight: 800;
    color: #087a3e;
    margin-top: 8px;
}

.result-note {
    color: #4b6655;
    font-size: 0.9rem;
    margin-top: 8px;
}

@keyframes resultAppear {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.97);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 45px;
    padding: 18px;
    color: #5b6380;
    font-size: 0.95rem;
}

.footer strong {
    color: #6638d9;
}

/* Mobile */
@media (max-width: 768px) {

    .hero-title h1 {
        font-size: 2.2rem;
    }

    .hero-title {
        padding: 25px 15px;
    }

    .section-card {
        padding: 20px 15px;
    }

    .result-price {
        font-size: 2rem;
    }
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Hero Header
# -----------------------------
st.markdown("""
<div class="hero-title">
    <h1>🏠 House Price Prediction</h1>
    <p>✨ Predict the estimated price of your dream home using Machine Learning</p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Basic House Details
# -----------------------------
st.markdown("""
<div class="section-card">
<div class="section-heading">🏡 Basic House Details</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    area = st.number_input(
        "Area (sq.ft)",
        min_value=200,
        max_value=16000,
        value=1000
    )

with col2:
    bedrooms = st.number_input(
        "No. of Bedrooms",
        min_value=1,
        max_value=10,
        value=2
    )

with col3:
    resale = st.selectbox(
        "Resale",
        ["No", "Yes"]
    )

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Property Features
# -----------------------------
st.markdown("""
<div class="section-card">
<div class="section-heading">🏢 Property Features</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    maintenance = st.checkbox("👨‍🔧 Maintenance Staff")
    gym = st.checkbox("🏋️ Gymnasium")
    swimming = st.checkbox("🏊 Swimming Pool")
    gardens = st.checkbox("🌳 Landscaped Gardens")
    jogging = st.checkbox("🏃 Jogging Track")
    rainwater = st.checkbox("💧 Rain Water Harvesting")
    indoor_games = st.checkbox("🎮 Indoor Games")
    shopping_mall = st.checkbox("🛍️ Shopping Mall")
    intercom = st.checkbox("📞 Intercom")
    sports = st.checkbox("⚽ Sports Facility")
    atm = st.checkbox("🏧 ATM")
    clubhouse = st.checkbox("🏠 Club House")
    school = st.checkbox("🎓 School")

with col2:
    security = st.checkbox("🔐 24X7 Security")
    power_backup = st.checkbox("⚡ Power Backup")
    car_parking = st.checkbox("🚗 Car Parking")
    staff_quarter = st.checkbox("🛏️ Staff Quarter")
    cafeteria = st.checkbox("☕ Cafeteria")
    multipurpose = st.checkbox("🏢 Multipurpose Room")
    hospital = st.checkbox("🏥 Hospital")
    washing_machine = st.checkbox("🧺 Washing Machine")
    gasconnection = st.checkbox("🔥 Gas Connection")
    ac = st.checkbox("❄️ AC")
    wifi = st.checkbox("📶 WiFi")
    children_play = st.checkbox("🧒 Children's Play Area")
    lift = st.checkbox("🛗 Lift Available")

with col3:
    bed = st.checkbox("🛏️ BED")
    vaastu = st.checkbox("🕉️ Vaastu Compliant")
    microwave = st.checkbox("📺 Microwave")
    golf = st.checkbox("⛳ Golf Course")
    tv = st.checkbox("📺 TV")
    dining_table = st.checkbox("🍽️ Dining Table")
    sofa = st.checkbox("🛋️ Sofa")
    wardrobe = st.checkbox("🚪 Wardrobe")
    refrigerator = st.checkbox("🧊 Refrigerator")

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Prediction
# -----------------------------
if st.button("🚀  Predict House Price", type="primary", use_container_width=True):

    input_data = {
        "Area": area,
        "No. of Bedrooms": bedrooms,
        "Resale": 1 if resale == "Yes" else 0,
        "MaintenanceStaff": int(maintenance),
        "Gymnasium": int(gym),
        "SwimmingPool": int(swimming),
        "LandscapedGardens": int(gardens),
        "JoggingTrack": int(jogging),
        "RainWaterHarvesting": int(rainwater),
        "IndoorGames": int(indoor_games),
        "ShoppingMall": int(shopping_mall),
        "Intercom": int(intercom),
        "SportsFacility": int(sports),
        "ATM": int(atm),
        "ClubHouse": int(clubhouse),
        "School": int(school),
        "24X7Security": int(security),
        "PowerBackup": int(power_backup),
        "CarParking": int(car_parking),
        "StaffQuarter": int(staff_quarter),
        "Cafeteria": int(cafeteria),
        "MultipurposeRoom": int(multipurpose),
        "Hospital": int(hospital),
        "WashingMachine": int(washing_machine),
        "Gasconnection": int(gasconnection),
        "AC": int(ac),
        "Wifi": int(wifi),
        "Children'splayarea": int(children_play),
        "LiftAvailable": int(lift),
        "BED": int(bed),
        "VaastuCompliant": int(vaastu),
        "Microwave": int(microwave),
        "GolfCourse": int(golf),
        "TV": int(tv),
        "DiningTable": int(dining_table),
        "Sofa": int(sofa),
        "Wardrobe": int(wardrobe),
        "Refrigerator": int(refrigerator)
    }

    # Convert input into DataFrame
    input_df = pd.DataFrame([input_data])

    # Same column order as training
    input_df = input_df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # Prediction
    predicted_price = model.predict(input_df)[0]

    # -----------------------------
    # Stylish Result
    # -----------------------------
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">🏠 Estimated House Price</div>
        <div class="result-price">₹{predicted_price:,.0f}</div>
        <div class="result-note">
            ✅ Prediction generated successfully using the Machine Learning model.
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div class="footer">
    🏠 House Price Prediction Project<br>
    <strong>Design By Aryan Prajapati</strong>
</div>
""", unsafe_allow_html=True)
