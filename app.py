import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# =========================================================
# LOAD MODEL
# =========================================================

APP_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(
    os.path.join(APP_DIR, "house_price_city_model.pkl")
)

feature_columns = joblib.load(
    os.path.join(APP_DIR, "city_feature_columns.pkl")
)

# =========================================================
# CUSTOM CSS
# =========================================================

CUSTOM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

<style>

/* =====================================================
   GLOBAL
===================================================== */

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* =====================================================
   ANIMATED BACKGROUND
===================================================== */

.stApp {
    background: linear-gradient(
        120deg,
        #1b1035,
        #2c1250,
        #4a1942,
        #7a2b4a,
        #a8455a,
        #d97b4f,
        #7a2b4a,
        #2c1250
    );

    background-size: 400% 400%;
    animation: gradientMove 22s ease infinite;
}

@keyframes gradientMove {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }

}

/* =====================================================
   HIDE DEFAULT STREAMLIT MENU
===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* =====================================================
   MAIN CONTAINER
===================================================== */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1150px;
}

/* =====================================================
   TEXT ANIMATION
===================================================== */

@keyframes textFadeIn {

    0% {
        opacity: 0;
        transform: translateY(12px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }

}

/* =====================================================
   GLOW ANIMATION
===================================================== */

@keyframes glowPulse {

    0%, 100% {
        text-shadow:
        0 0 6px rgba(255,255,255,0.15);
    }

    50% {
        text-shadow:
        0 0 18px rgba(255,255,255,0.45);
    }

}

/* =====================================================
   MAIN TITLE BOX
===================================================== */

.main-title-box {

    background: rgba(20, 10, 35, 0.72);

    border: 1px solid rgba(255,255,255,0.18);

    border-radius: 20px;

    padding: 22px 28px;

    margin-bottom: 12px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.08);

    backdrop-filter: blur(12px);

    animation: textFadeIn 0.9s ease;
}

.main-title {

    color: white;

    font-size: 42px;

    font-weight: 800;

    margin: 0;

    letter-spacing: 0.5px;

    animation:
        glowPulse 4s ease-in-out infinite;

}

.main-description {

    color: rgba(255,255,255,0.92);

    font-size: 16px;

    margin-top: 10px;

    margin-bottom: 0;

}

/* =====================================================
   SECTION HEADER BOX
===================================================== */

.section-title-box {

    background: rgba(20, 10, 35, 0.68);

    border: 1px solid rgba(255,255,255,0.18);

    border-radius: 15px;

    padding: 13px 20px;

    margin-top: 25px;

    margin-bottom: 18px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.22);

    backdrop-filter: blur(10px);

    animation: textFadeIn 0.8s ease;

}

.section-title {

    color: #ffffff;

    font-size: 25px;

    font-weight: 700;

    margin: 0;

}

/* =====================================================
   STREAMLIT LABELS
===================================================== */

.stNumberInput label,
.stSelectbox label,
.stCheckbox label {

    background: rgba(20, 10, 35, 0.62);

    border-radius: 8px;

    padding: 5px 10px;

    width: fit-content;

    box-shadow:
        0 4px 12px rgba(0,0,0,0.15);

}

.stNumberInput label p,
.stSelectbox label p,
.stCheckbox label p {

    color: #ffffff !important;

    font-weight: 600 !important;

    font-size: 14px !important;

    margin: 0 !important;

}

/* =====================================================
   INPUT BOX
===================================================== */

.stNumberInput input {

    background: rgba(255,255,255,0.93) !important;

    border-radius: 10px !important;

    border: 2px solid rgba(255,255,255,0.5) !important;

    color: #222222 !important;

    font-weight: 500 !important;

}

/* =====================================================
   SELECT BOX
===================================================== */

div[data-baseweb="select"] > div {

    background: rgba(255,255,255,0.93) !important;

    border-radius: 10px !important;

    border: 2px solid rgba(255,255,255,0.5) !important;

    color: #222222 !important;

}

/* =====================================================
   SELECT BOX TEXT
===================================================== */

div[data-baseweb="select"] span {

    color: #222222 !important;

    font-weight: 500 !important;

}

/* =====================================================
   CHECKBOX TEXT
===================================================== */

.stCheckbox {

    background: rgba(20, 10, 35, 0.55);

    border-radius: 9px;

    padding: 5px 9px;

    margin-bottom: 6px;

    transition: all 0.25s ease;

}

.stCheckbox:hover {

    background: rgba(20, 10, 35, 0.78);

    transform: translateY(-1px);

}

/* =====================================================
   PREDICT BUTTON
===================================================== */

div.stButton > button {

    width: 100%;

    background:
        linear-gradient(
            90deg,
            #ff6a88 0%,
            #ff9a44 100%
        );

    color: #ffffff;

    font-size: 19px;

    font-weight: 700;

    letter-spacing: 1px;

    padding: 14px 0;

    border-radius: 14px;

    border: none;

    box-shadow:
        0 8px 24px rgba(255,106,136,0.4);

    transition: all 0.3s ease;

    animation: textFadeIn 1s ease;

}

div.stButton > button:hover {

    transform:
        translateY(-3px)
        scale(1.01);

    box-shadow:
        0 12px 32px rgba(255,154,68,0.55);

    color: #ffffff;

}

/* =====================================================
   RESULT BOX
===================================================== */

div[data-testid="stAlert"] {

    background: rgba(20, 10, 35, 0.82) !important;

    border: 2px solid rgba(255,255,255,0.25) !important;

    border-radius: 16px !important;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.3);

}

div[data-testid="stAlert"] p {

    color: #ffffff !important;

    font-size: 20px !important;

    font-weight: 700 !important;

    animation:
        textFadeIn 0.8s ease,
        glowPulse 4s ease-in-out infinite;

}

/* =====================================================
   PREDICTION DETAILS BOX
===================================================== */

.prediction-details {

    background: rgba(20, 10, 35, 0.68);

    border: 1px solid rgba(255,255,255,0.18);

    border-radius: 12px;

    padding: 12px 18px;

    margin-top: 10px;

    color: #ffffff;

    font-size: 15px;

    font-weight: 500;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.2);

}

/* =====================================================
   DIVIDER
===================================================== */

hr {

    border-color:
        rgba(255,255,255,0.25) !important;

}

/* =====================================================
   FOOTER
===================================================== */

.credit-container {

    text-align: center;

    margin-top: 15px;

    background: rgba(20,10,35,0.65);

    border: 1px solid rgba(255,255,255,0.15);

    border-radius: 14px;

    padding: 15px;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.2);

}

.credit-name {

    font-size: 24px;

    font-weight: 800;

    letter-spacing: 3px;

    text-transform: uppercase;

    background:
        linear-gradient(
            90deg,
            #ff6a88 0%,
            #ff9a44 35%,
            #43e97b 65%,
            #38f9d7 100%
        );

    background-size: 200% auto;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    background-clip: text;

    display: inline-block;

}

.credit-sub {

    color: rgba(255,255,255,0.78);

    font-size: 13px;

    margin-top: 6px;

}

</style>
"""

if hasattr(st, "html"):
    st.html(CUSTOM_CSS)
else:
    st.markdown(
        CUSTOM_CSS,
        unsafe_allow_html=True
    )

# =========================================================
# TITLE
# =========================================================

st.html("""
<div class="main-title-box">

    <div class="main-title">
        🏠 House Price Prediction
    </div>

    <div class="main-description">
        Estimate house prices using a Machine Learning model.
    </div>

</div>
""")

# =========================================================
# BASIC HOUSE DETAILS
# =========================================================

st.html("""
<div class="section-title-box">
    <div class="section-title">
        🏠 Basic House Details
    </div>
</div>
""")

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

# =========================================================
# LOCATION
# =========================================================

st.html("""
<div class="section-title-box">
    <div class="section-title">
        🏙️ Location Details
    </div>
</div>
""")

city = st.selectbox(
    "🌆 Select City",
    [
        "Bangalore",
        "Chennai",
        "Delhi",
        "Hyderabad",
        "Kolkata",
        "Mumbai"
    ]
)

# =========================================================
# FEATURES
# =========================================================

st.html("""
<div class="section-title-box">
    <div class="section-title">
        ✨ Property Features & Amenities
    </div>
</div>
""")

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
            st.checkbox(
                feature_label,
                value=False
            )
        )

# =========================================================
# INPUT DATA
# =========================================================

input_data = {

    "Area": area,

    "No. of Bedrooms": bedrooms,

    "Resale": 1 if resale == "Yes" else 0
}

for feature_name, _ in feature_list:

    input_data[feature_name] = feature_values[
        feature_name
    ]

# =========================================================
# CITY ONE-HOT ENCODING
# =========================================================

city_columns = [

    "City_Chennai",

    "City_Delhi",

    "City_Hyderabad",

    "City_Kolkata",

    "City_Mumbai"
]

for column in city_columns:

    input_data[column] = int(
        city == column.replace(
            "City_",
            ""
        )
    )

# =========================================================
# PREDICTION
# =========================================================

st.write("")

if st.button(
    "🔮 Predict House Price",
    type="primary"
):

    input_df = pd.DataFrame(
        [input_data]
    )

    input_df = input_df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    predicted_price = model.predict(
        input_df
    )[0]

    st.success(
        f"Estimated House Price: ₹{predicted_price:,.0f}"
    )

    st.html(f"""
    <div class="prediction-details">

        📍 <b>City:</b> {city}
        &nbsp;&nbsp; | &nbsp;&nbsp;

        📐 <b>Area:</b> {area:,.0f} sq.ft
        &nbsp;&nbsp; | &nbsp;&nbsp;

        🛏️ <b>Bedrooms:</b> {bedrooms}

    </div>
    """)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.html("""
<div class="credit-container">

    <div class="credit-name">
        ARYAN PRAJAPATI
    </div>

    <div class="credit-sub">
        🏠 House Price Prediction • Machine Learning Project
    </div>

</div>
""")
