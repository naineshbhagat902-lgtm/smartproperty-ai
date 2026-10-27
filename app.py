import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# -------------------------------
# SmartProperty AI - Advanced Demo
# -------------------------------
st.set_page_config(
    page_title="SmartProperty AI",
    page_icon="🏡",
    layout="wide"
)
st.markdown("""
<style>
    .stApp {
        background: #f4f7fb;
        color: #17243a;
    }

    [data-testid="stSidebar"] {
        background: #101d35;
    }

    [data-testid="stSidebar"] * {
        color: #f5f7fb;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #142747;
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #203a60;
        font-weight: 700;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e3eaf3;
        padding: 22px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(24, 45, 75, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #163b70;
        font-weight: 800;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        background: #2458a6;
        color: white;
        border: none;
        border-radius: 9px;
        padding: 0.65rem 1rem;
        font-weight: 600;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        background: #173e79;
        color: white;
        border: none;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #e3eaf3;
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: #dfe7f1;
    }
</style>
""", unsafe_allow_html=True)
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "properties.csv"

st.title("🏡 SmartProperty AI")
st.subheader("Real Estate Analytics & Price Prediction")
st.caption(
    "AI/ML student prototype | Predictions use illustrative sample data."
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    required = [
        "property_name", "location", "property_type",
        "price_lakh", "area_sqft", "monthly_rent",
        "building_age"
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing CSV columns: {', '.join(missing)}")

    df = df.dropna(subset=required).copy()
    df = df[df["area_sqft"] > 0]
    return df

@st.cache_resource
def train_model(data):
    features = [
        "location", "property_type",
        "area_sqft", "building_age"
    ]

    transformer = ColumnTransformer([
        (
            "category",
            OneHotEncoder(handle_unknown="ignore"),
            ["location", "property_type"]
        ),
        ("numbers", "passthrough", ["area_sqft", "building_age"])
    ])

    pipeline = Pipeline([
        ("preprocessor", transformer),
        ("model", RandomForestRegressor(
            n_estimators=100,
            random_state=42
        ))
    ])

    pipeline.fit(data[features], data["price_lakh"])
    return pipeline

try:
    properties = load_data()
except Exception as error:
    st.error(f"Could not load property data: {error}")
    st.stop()

if len(properties) < 5:
    st.error("Please add at least 5 valid sample properties.")
    st.stop()

model = train_model(properties)

# Sidebar inputs
with st.sidebar:
    st.header("🏠 Property details")

    location = st.selectbox(
        "Location",
        sorted(properties["location"].unique())
    )

    property_type = st.selectbox(
        "Property type",
        sorted(properties["property_type"].unique())
    )

    price_lakh = st.number_input(
        "Asking price (₹ lakh)",
        min_value=1.0,
        max_value=10000.0,
        value=60.0,
        step=1.0
    )

    area = st.number_input(
        "Area (sq. ft.)",
        min_value=50,
        max_value=100000,
        value=600,
        step=10
    )

    age = st.number_input(
        "Building age (years)",
        min_value=0,
        max_value=150,
        value=5,
        step=1
    )

    monthly_rent = st.number_input(
        "Expected monthly rent (₹)",
        min_value=0,
        max_value=10000000,
        value=15000,
        step=1000
    )

    compare_location = st.checkbox(
        "Compare with selected location",
        value=True
    )

# Calculations
price_rupees = price_lakh * 100000
price_per_sqft = price_rupees / area
annual_rent = monthly_rent * 12
gross_yield = annual_rent / price_rupees * 100

input_data = pd.DataFrame([{
    "location": location,
    "property_type": property_type,
    "area_sqft": area,
    "building_age": age
}])

predicted_lakh = max(0, float(model.predict(input_data)[0]))
difference = price_lakh - predicted_lakh
difference_percent = (
    difference / predicted_lakh * 100
    if predicted_lakh > 0 else 0
)

# Dashboard metrics
st.markdown("## 📊 Property dashboard")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Asking price", f"₹{price_lakh:,.1f} lakh")
m2.metric("ML price estimate", f"₹{predicted_lakh:,.1f} lakh")
m3.metric("Price per sq. ft.", f"₹{price_per_sqft:,.0f}")
m4.metric("Gross rental yield", f"{gross_yield:.2f}%")

st.divider()

# Prediction explanation
st.markdown("## 🤖 AI price analysis")

left, right = st.columns(2)

with left:
    st.markdown("### Estimated vs asking price")
    comparison_chart = pd.DataFrame({
        "Price type": ["ML estimate", "Asking price"],
        "Price (₹ lakh)": [predicted_lakh, price_lakh]
    }).set_index("Price type")

    st.bar_chart(comparison_chart)

with right:
    st.markdown("### Assessment")

    if abs(difference_percent) <= 10:
        st.info(
            "The asking price is within 10% of the model estimate. "
            "Check more comparable properties before deciding."
        )
    elif difference > 0:
        st.warning(
            f"The asking price is {difference_percent:.1f}% above "
            "the model estimate. Investigate the difference."
        )
    else:
        st.success(
            f"The asking price is {abs(difference_percent):.1f}% below "
            "the model estimate. Verify property condition and documents."
        )

    st.write(f"Estimated annual rent: ₹{annual_rent:,.0f}")
    st.write(f"Estimated monthly rent: ₹{monthly_rent:,.0f}")

    st.caption(
        "Gross yield excludes maintenance, vacancy, taxes and "
        "other ownership costs."
    )

# Comparable sample properties
st.markdown("## 🏘️ Comparable properties")

comparison = properties.copy()

if compare_location:
    comparison = comparison[comparison["location"] == location]

comparison["price_per_sqft"] = (
    comparison["price_lakh"] * 100000 / comparison["area_sqft"]
)

if not comparison.empty:
    median_price = comparison["price_per_sqft"].median()
    st.metric(
        "Sample median price per sq. ft.",
        f"₹{median_price:,.0f}"
    )

    st.dataframe(
        comparison[[
            "property_name", "location", "property_type",
            "price_lakh", "area_sqft", "monthly_rent",
            "building_age", "price_per_sqft"
        ]].rename(columns={
            "property_name": "Property",
            "price_lakh": "Price (₹ lakh)",
            "area_sqft": "Area (sq. ft.)",
            "monthly_rent": "Monthly rent (₹)",
            "building_age": "Age (years)",
            "price_per_sqft": "Price / sq. ft. (₹)"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Sample price distribution")
    fig, ax = plt.subplots()
    ax.bar(
        comparison["property_name"],
        comparison["price_lakh"]
    )
    ax.set_xlabel("Sample property")
    ax.set_ylabel("Price (₹ lakh)")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("No comparable properties found for this selection.")

# Download report
st.markdown("## 📥 Download your analysis")

report = pd.DataFrame([{
    "location": location,
    "property_type": property_type,
    "asking_price_lakh": price_lakh,
    "predicted_price_lakh": round(predicted_lakh, 2),
    "area_sqft": area,
    "building_age": age,
    "price_per_sqft_rupees": round(price_per_sqft, 2),
    "monthly_rent_rupees": monthly_rent,
    "annual_rent_rupees": annual_rent,
    "gross_rental_yield_percent": round(gross_yield, 2)
}])

st.download_button(
    "Download property report (CSV)",
    data=report.to_csv(index=False).encode("utf-8"),
    file_name="smartproperty_ai_report.csv",
    mime="text/csv"
)

st.divider()
st.caption(
    "Educational prototype only. The model trains on a very small "
    "illustrative dataset and may produce misleading estimates. "
    "It is not a verified market valuation or investment advice."
)
# Location map and neighbourhood insights
st.divider()
st.subheader("📍 Location & Neighbourhood Insights")

st.write(
    "Explore the selected property location on Google Maps. "
    "Location results depend on Google Maps search data."
)

import urllib.parse

maps_query = urllib.parse.quote(
    f"{location}, India"
)

st.link_button(
    "🗺️ View Neighbourhood on Google Maps",
    f"https://www.google.com/maps/search/?api=1&query={maps_query}",
    use_container_width=True
)

st.caption(
    "Note: This opens Google Maps in a new page. "
    "Nearby places and distances should be verified independently."
)
