import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from urllib.parse import quote
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# SmartProperty AI - upgraded student prototype
st.set_page_config(page_title="SmartProperty AI", page_icon="🏡", layout="wide")

st.markdown("""
<style>
.stApp {background:#f4f7fb; color:#17243a;}
[data-testid="stSidebar"] {background:#101d35;}
[data-testid="stSidebar"] * {color:#f5f7fb;}
.block-container {max-width:1440px; padding-top:1.8rem; padding-bottom:3rem;}
h1 {color:#142747; font-weight:800;}
h2,h3 {color:#203a60; font-weight:700;}
[data-testid="stMetric"] {background:white; border:1px solid #e3eaf3;
padding:18px; border-radius:14px; box-shadow:0 4px 16px rgba(24,45,75,.05);}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "properties.csv"
LOCALITY_FILE = BASE_DIR / "data" / "locality_data.csv"

st.title("🏡 SmartProperty AI")
st.subheader("Property Price, Locality & Investment Analyzer")
st.caption("Student prototype. Results depend on the quality of the supplied data; estimates are not professional valuation or financial advice.")

@st.cache_data
def load_properties():
    df = pd.read_csv(DATA_FILE)
    required = ["property_name", "location", "property_type", "price_lakh",
                "area_sqft", "monthly_rent", "building_age"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError("Missing columns in properties.csv: " + ", ".join(missing))
    df = df.dropna(subset=required).copy()
    for col in ["price_lakh", "area_sqft", "monthly_rent", "building_age"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["price_lakh", "area_sqft", "monthly_rent", "building_age"])
    return df[df["area_sqft"] > 0]

@st.cache_resource
def train_model(data):
    features = ["location", "property_type", "area_sqft", "building_age"]
    transformer = ColumnTransformer([
        ("category", OneHotEncoder(handle_unknown="ignore"), ["location", "property_type"]),
        ("numbers", "passthrough", ["area_sqft", "building_age"])
    ])
    model = Pipeline([
        ("preprocessor", transformer),
        ("model", RandomForestRegressor(n_estimators=150, random_state=42))
    ])
    model.fit(data[features], data["price_lakh"])
    return model

try:
    properties = load_properties()
except Exception as exc:
    st.error(f"Could not load {DATA_FILE}: {exc}")
    st.info("Keep the existing data/properties.csv file in the same project folder.")
    st.stop()

if len(properties) < 5:
    st.error("Please provide at least 5 valid property rows in data/properties.csv.")
    st.stop()

model = train_model(properties)

with st.sidebar:
    st.header("🏠 Property details")
    location = st.selectbox("Location", sorted(properties["location"].unique()))
    property_type = st.selectbox("Property type", sorted(properties["property_type"].unique()))
    price_lakh = st.number_input("Asking price (₹ lakh)", min_value=1.0, max_value=10000.0, value=60.0, step=1.0)
    area = st.number_input("Area (sq. ft.)", min_value=50, max_value=100000, value=600, step=10)
    age = st.number_input("Building age (years)", min_value=0, max_value=150, value=5, step=1)
    monthly_rent = st.number_input("Expected monthly rent (₹)", min_value=0, max_value=10000000, value=15000, step=1000)
    monthly_maintenance = st.number_input("Monthly maintenance (₹)", min_value=0, max_value=500000, value=3000, step=500)
    annual_other_costs = st.number_input("Other annual owner costs (₹)", min_value=0, max_value=10000000, value=12000, step=2000)

price_rupees = price_lakh * 100000
price_per_sqft = price_rupees / area
annual_rent = monthly_rent * 12
gross_yield = annual_rent / price_rupees * 100 if price_rupees else 0
annual_maintenance = monthly_maintenance * 12
net_annual_income = annual_rent - annual_maintenance - annual_other_costs
net_yield = net_annual_income / price_rupees * 100 if price_rupees else 0
input_data = pd.DataFrame([{"location": location, "property_type": property_type,
                            "area_sqft": area, "building_age": age}])
predicted_lakh = max(0, float(model.predict(input_data)[0]))
difference = price_lakh - predicted_lakh
difference_percent = difference / predicted_lakh * 100 if predicted_lakh > 0 else 0

tabs = st.tabs(["📊 Property Dashboard", "🏘️ Smart Locality Analysis", "📈 Investment Scenarios", "📥 Export Report"])

with tabs[0]:
    st.header("Property dashboard")
    a,b,c,d = st.columns(4)
    a.metric("Asking price", f"₹{price_lakh:,.1f} lakh")
    b.metric("Sample ML estimate", f"₹{predicted_lakh:,.1f} lakh")
    c.metric("Price per sq. ft.", f"₹{price_per_sqft:,.0f}")
    d.metric("Gross rental yield", f"{gross_yield:.2f}%")
    st.caption("The model is trained on the small sample CSV in this project. Its prediction is for demonstration only, not a verified market valuation.")
    left, right = st.columns(2)
    with left:
        st.subheader("Asking price vs model estimate")
        st.bar_chart(pd.DataFrame({"Price (₹ lakh)": [predicted_lakh, price_lakh]},
                                  index=["Model estimate", "Asking price"]))
    with right:
        st.subheader("Quick assessment")
        if abs(difference_percent) <= 10:
            st.info("Asking price is within 10% of this model estimate. Check real comparable listings and property documents.")
        elif difference > 0:
            st.warning(f"Asking price is {difference_percent:.1f}% above the sample model estimate. Investigate before deciding.")
        else:
            st.success(f"Asking price is {abs(difference_percent):.1f}% below the sample model estimate. Verify condition, title and hidden costs.")
        st.write(f"Estimated annual rent: ₹{annual_rent:,.0f}")
        st.write(f"Estimated net annual rent after entered costs: ₹{net_annual_income:,.0f}")
        st.metric("Net rental yield after entered costs", f"{net_yield:.2f}%")
    st.divider()
    st.subheader("Comparable sample properties")
    comparable = properties[properties["location"] == location].copy()
    comparable["price_per_sqft"] = comparable["price_lakh"] * 100000 / comparable["area_sqft"]
    st.dataframe(comparable.rename(columns={
        "property_name":"Property", "location":"Location", "property_type":"Type",
        "price_lakh":"Price (₹ lakh)", "area_sqft":"Area (sq. ft.)",
        "monthly_rent":"Monthly rent (₹)", "building_age":"Age (years)",
        "price_per_sqft":"Price / sq. ft. (₹)"
    }), use_container_width=True, hide_index=True)
    maps_url = "https://www.google.com/maps/search/?api=1&query=" + quote(f"{location}, India")
    st.link_button("🗺️ Open selected location in Google Maps", maps_url)
    st.caption("The map link opens Google Maps; it does not verify water supply, power cuts or internet reliability.")

with tabs[1]:
    st.header("Smart Locality Analysis")
    st.write("Use verified locality information where available. Do not treat example data as real-world facts.")
    st.info("If you have no verified data for a field, leave it as 'Unknown'. The score below only uses fields you enter.")
    if LOCALITY_FILE.exists():
        locality_df = pd.read_csv(LOCALITY_FILE)
        if "location" not in locality_df.columns:
            locality_df = pd.DataFrame()
    else:
        locality_df = pd.DataFrame()

    match = locality_df[locality_df["location"].astype(str).str.casefold() == str(location).casefold()] if not locality_df.empty else pd.DataFrame()
    existing = match.iloc[0].to_dict() if not match.empty else {}
    st.caption("Values loaded from data/locality_data.csv if you create it. Source/date columns are recommended.")
    with st.form("locality_form"):
        water = st.selectbox("Water supply", ["Unknown", "Good", "Average", "Poor"],
                             index=["Unknown","Good","Average","Poor"].index(str(existing.get("water_supply","Unknown"))))
        power_cuts = st.number_input("Reported power cuts per month (enter only if known)", min_value=0, max_value=100, value=int(existing.get("power_cuts_per_month", 0) or 0))
        internet = st.selectbox("Internet quality", ["Unknown", "Good", "Average", "Poor"],
                                index=["Unknown","Good","Average","Poor"].index(str(existing.get("internet_quality","Unknown"))))
        hospital_km = st.number_input("Distance to nearest hospital (km; unknown = 0)", min_value=0.0, max_value=500.0, value=float(existing.get("hospital_km", 0) or 0), step=0.5)
        school_km = st.number_input("Distance to nearest school (km; unknown = 0)", min_value=0.0, max_value=500.0, value=float(existing.get("school_km", 0) or 0), step=0.5)
        source = st.text_input("Data source / survey reference", value=str(existing.get("source","")))
        checked_date = st.date_input("Date checked")
        submitted = st.form_submit_button("Analyze locality")
    if submitted:
        scores = []
        if water != "Unknown":
            scores.append({"Good":100,"Average":60,"Poor":20}[water] * 0.35)
            water_status = f"{water} (entered data)"
        else:
            water_status = "Unavailable"
        if power_cuts > 0 or (not match.empty and pd.notna(existing.get("power_cuts_per_month"))):
            power_score = max(0, 100 - power_cuts * 5)
            scores.append(power_score * 0.30)
            power_status = f"{power_cuts} reported cuts/month"
        else:
            power_status = "Unavailable / not entered"
        if internet != "Unknown":
            scores.append({"Good":100,"Average":60,"Poor":20}[internet] * 0.25)
            internet_status = f"{internet} (entered data)"
        else:
            internet_status = "Unavailable"
        distance_scores = []
        if hospital_km > 0:
            distance_scores.append(max(0, 100 - hospital_km * 10))
        if school_km > 0:
            distance_scores.append(max(0, 100 - school_km * 10))
        if distance_scores:
            scores.append((sum(distance_scores)/len(distance_scores)) * 0.10)
        if scores:
            # Renormalize over known factors only; do not penalize missing values as if they were poor.
            weights_used = []
            if water != "Unknown": weights_used.append(0.35)
            if power_cuts > 0 or (not match.empty and pd.notna(existing.get("power_cuts_per_month"))): weights_used.append(0.30)
            if internet != "Unknown": weights_used.append(0.25)
            if distance_scores: weights_used.append(0.10)
            total_weight = sum(weights_used)
            locality_score = sum(scores) / total_weight if total_weight else None
            st.metric("Provisional Locality Score", f"{locality_score:.0f}/100" if locality_score is not None else "Unavailable")
            st.write("Water:", water_status)
            st.write("Electricity:", power_status)
            st.write("Internet:", internet_status)
            st.write("Hospital distance:", f"{hospital_km:g} km" if hospital_km > 0 else "Unavailable")
            st.write("School distance:", f"{school_km:g} km" if school_km > 0 else "Unavailable")
            st.write("Source:", source.strip() or "Not supplied")
            st.write("Checked on:", checked_date.isoformat())
            st.caption("This is a simple user-entered screening score, not an official area rating. Confirm information with local authorities/providers.")
        else:
            st.warning("Not enough information to calculate a score. Enter at least one known field.")
    st.markdown("#### Suggested locality CSV format")
    st.code("location,water_supply,power_cuts_per_month,internet_quality,hospital_km,school_km,source,checked_date\\nPanvel,Unknown,,,1.2,0.8,Add verified source,2026-10-29", language="csv")
    st.caption("Save verified rows as data/locality_data.csv. Keep unknown values blank; do not fill guesses as facts.")

with tabs[2]:
    st.header("Future Investment Scenarios")
    st.write("These are what-if scenarios based on assumptions chosen by you, not AI predictions or guarantees.")
    col1, col2, col3 = st.columns(3)
    with col1:
        years = st.slider("Projection period (years)", 1, 10, 5)
        conservative = st.number_input("Conservative annual price change (%)", min_value=-30.0, max_value=30.0, value=0.0, step=0.5)
    with col2:
        base = st.number_input("Base annual price change (%)", min_value=-30.0, max_value=30.0, value=4.0, step=0.5)
        vacancy = st.slider("Estimated vacant months per year", 0, 12, 1)
    with col3:
        optimistic = st.number_input("Optimistic annual price change (%)", min_value=-30.0, max_value=30.0, value=8.0, step=0.5)
        rent_growth = st.number_input("Annual rent change (%)", min_value=-20.0, max_value=30.0, value=3.0, step=0.5)
    scenario_rates = {"Conservative": conservative/100, "Base": base/100, "Optimistic": optimistic/100}
    scenario_rows = []
    for label, rate in scenario_rates.items():
        future_value = price_rupees * ((1 + rate) ** years)
        annual_rent_received = monthly_rent * max(0, 12-vacancy)
        total_net_rent = 0
        current_rent = monthly_rent
        current_maintenance = monthly_maintenance
        for _ in range(years):
            total_net_rent += current_rent * max(0, 12-vacancy) - current_maintenance * 12 - annual_other_costs
            current_rent *= (1 + rent_growth/100)
            current_maintenance *= 1.03
        total_change = future_value - price_rupees + total_net_rent
        scenario_rows.append({
            "Scenario": label,
            "Assumed yearly price change": f"{rate*100:.1f}%",
            "Estimated property value": round(future_value),
            "Cumulative net rent after entered costs": round(total_net_rent),
            "Value change + net rent (before transaction/sale costs)": round(total_change)
        })
    scenario_df = pd.DataFrame(scenario_rows)
    st.dataframe(scenario_df, use_container_width=True, hide_index=True)
    chart_df = pd.DataFrame({
        "Estimated value (₹)": [price_rupees * ((1+r)**years) for r in scenario_rates.values()]
    }, index=list(scenario_rates.keys()))
    st.bar_chart(chart_df)
    st.caption("Assumptions are illustrative. Calculations exclude loan interest, tax, transaction costs, major repairs, inflation and sale costs. Negative net rent is possible.")

with tabs[3]:
    st.header("Download your analysis")
    report = pd.DataFrame([{
        "location": location, "property_type": property_type,
        "asking_price_lakh": price_lakh, "sample_model_estimate_lakh": round(predicted_lakh, 2),
        "area_sqft": area, "building_age": age, "price_per_sqft_rupees": round(price_per_sqft, 2),
        "monthly_rent_rupees": monthly_rent, "monthly_maintenance_rupees": monthly_maintenance,
        "annual_other_costs_rupees": annual_other_costs, "gross_rental_yield_percent": round(gross_yield, 2),
        "net_rental_yield_after_entered_costs_percent": round(net_yield, 2)
    }])
    st.dataframe(report, use_container_width=True, hide_index=True)
    st.download_button("Download property report (CSV)", data=report.to_csv(index=False).encode("utf-8"),
                       file_name="smartproperty_ai_report.csv", mime="text/csv")
    st.download_button("Download current properties data (CSV)", data=properties.to_csv(index=False).encode("utf-8"),
                       file_name="properties.csv", mime="text/csv")

st.divider()
st.caption("Educational prototype only. Sample data and user-entered locality information may be incomplete or inaccurate. Verify property documents, locality conditions, and market data independently before making decisions.")
