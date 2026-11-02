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

/* ==========================================
   SMARTPROPERTY AI - PROFESSIONAL UI THEME
========================================== */

/* Main application background */
.stApp {
    background-color: #F4F7FB;
    color: #1E293B;
}

/* Main headings */
h1, h2, h3, h4, h5, h6 {
    color: #142B49 !important;
    font-weight: 700 !important;
}

/* Normal text */
p, label, span, li {
    color: #334155;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #142B49;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #FFFFFF;
    color: #142B49 !important;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border-radius: 8px;
}

[data-baseweb="select"] * {
    color: #142B49 !important;
}

/* Widget labels */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p {
    color: #142B49 !important;
    font-weight: 600;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
}

/* Metric labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #64748B !important;
    font-weight: 600;
}

/* Metric values */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #142B49 !important;
    font-weight: 800;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background-color: #E98235;
    color: #FFFFFF !important;
    border: none;
    border-radius: 9px;
    padding: 0.65rem 1rem;
    font-weight: 600;
    transition: 0.3s ease;
}

/* Button hover effect */
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #D96D20;
    color: #FFFFFF !important;
    border: none;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

/* Containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-radius: 14px;
    border-color: #E2E8F0;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    background-color: #FFFFFF;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Links */
a {
    color: #E98235 !important;
    font-weight: 600;
}

/* Horizontal divider */
hr {
    border-color: #E2E8F0;
}

/* Dashboard hero section */
.dashboard-hero {
    background: linear-gradient(
        120deg,
        #142B49,
        #234B75
    );
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0 5px 18px rgba(20, 43, 73, 0.15);
}

.dashboard-hero h1 {
    color: #FFFFFF !important;
    font-size: 36px;
    margin-bottom: 8px;
}

.dashboard-hero p {
    color: #E2E8F0 !important;
    font-size: 16px;
}

/* Property card price */
.property-price {
    color: #E98235;
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 12px;
}

/* Smooth page appearance */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Responsive headings */
@media (max-width: 768px) {
    .dashboard-hero {
        padding: 22px;
    }

    .dashboard-hero h1 {
        font-size: 27px;
    }
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
    df = df[df["area_sqft"] > 0].copy()

    # Group individual localities into their main cities
    location_text = df["location"].astype(str).str.strip().str.lower()

    df["city"] = "Other"
    df.loc[location_text.str.contains("panvel", na=False), "city"] = "Panvel"
    df.loc[location_text.str.contains("navi mumbai", na=False), "city"] = "Navi Mumbai"

    mumbai_mask = (
        location_text.str.contains("mumbai", na=False)
        & ~location_text.str.contains("navi mumbai", na=False)
    )
    df.loc[mumbai_mask, "city"] = "Mumbai"

    return df



@st.cache_resource
def train_model(data):
    features = [
        "city", "property_type",
        "area_sqft", "building_age"
    ]

    transformer = ColumnTransformer([
        (
            "category",
            OneHotEncoder(handle_unknown="ignore"),
            ["city", "property_type"]
        ),
        (
            "numbers",
            "passthrough",
            ["area_sqft", "building_age"]
        )
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

selected_city = properties.loc[
    properties["location"] == location, "city"
].iloc[0]

input_data = pd.DataFrame([{
    "city": selected_city,
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

# ==========================================
# PROFESSIONAL SMARTPROPERTY AI DASHBOARD
# ==========================================

# Dashboard heading
st.markdown("## 🏡 SmartProperty Dashboard")

st.caption(
    "Your intelligent real estate dashboard powered by "
    "machine learning and property data analytics."
)

# ==========================================
# 1. MAIN PROPERTY KPI CARDS
# ==========================================

st.markdown("### 📊 Property Overview")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "🏠 Asking Price",
    f"₹{price_lakh:,.1f} L"
)

m2.metric(
    "🤖 AI Estimated Value",
    f"₹{predicted_lakh:,.1f} L"
)

m3.metric(
    "📐 Price / Sq. Ft.",
    f"₹{price_per_sqft:,.0f}"
)

m4.metric(
    "💰 Rental Yield",
    f"{gross_yield:.2f}%"
)

st.divider()

# ==========================================
# 2. FEATURED PROPERTY CARDS
# ==========================================

st.markdown("### 🏘️ Featured Properties")

st.caption(
    "Explore properties available in your existing CSV dataset."
)

featured_properties = properties[
    properties["location"].astype(str).str.strip()
    == str(location).strip()
].head(6)

property_columns = st.columns(3)

for index, (_, prop) in enumerate(
    featured_properties.iterrows()
):

    with property_columns[index % 3]:

        with st.container(border=True):
            image_path = prop.get("image_path", "")

            if pd.notna(image_path) and Path(str(image_path)).is_file():
                st.image(image_path, use_container_width=True)
            st.markdown(
                f"#### 🏠 {prop['property_name']}"
            )

            st.markdown(
                f"""
                <div class="property-price">
                    ₹{float(prop['price_lakh']):,.2f} L
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                "📍 **Location:**",
                prop["location"]
            )

            st.write(
                "🏢 **Type:**",
                prop["property_type"]
            )

            st.write(
                "📐 **Area:**",
                f"{float(prop['area_sqft']):,.0f} sq. ft."
            )

            st.write(
                "💵 **Monthly Rent:**",
                f"₹{float(prop['monthly_rent']):,.0f}"
            )

            st.write(
                "🏗️ **Building Age:**",
                f"{float(prop['building_age']):.0f} years"
            )

st.divider()

# ==========================================
# 3. AI PROPERTY ANALYTICS
# ==========================================

st.markdown("### 🤖 AI Property Analytics")

ai_col1, ai_col2 = st.columns(2)

# AI valuation insight
with ai_col1:

    st.markdown("#### 📈 AI Price Analysis")

    st.metric(
        "AI Estimated Property Value",
        f"₹{predicted_lakh:,.2f} L"
    )

    st.write(
        f"Your asking price is ₹{price_lakh:,.2f} lakh."
    )

    if difference > 0:

        st.warning(
            f"Your asking price is "
            f"{difference_percent:.1f}% above the "
            "AI estimated value."
        )

    elif difference < 0:

        st.success(
            f"Your asking price is "
            f"{abs(difference_percent):.1f}% below the "
            "AI estimated value."
        )

    else:

        st.info(
            "Your asking price matches the AI estimated value."
        )

# Investment insights
with ai_col2:

    st.markdown("#### 💡 Investment Snapshot")

    st.metric(
        "Annual Rental Income",
        f"₹{annual_rent:,.0f}"
    )

    st.metric(
        "Monthly Rental Income",
        f"₹{monthly_rent:,.0f}"
    )

    st.metric(
        "Gross Rental Yield",
        f"{gross_yield:.2f}%"
    )

    st.metric(
        "Price per Sq. Ft.",
        f"₹{price_per_sqft:,.0f}"
    )

st.divider()

# ==========================================
# 4. AI RECOMMENDATION
# ==========================================

st.markdown("### 🧠 Smart AI Recommendation")

if predicted_lakh > 0:

    if abs(difference_percent) <= 10:

        st.success(
            "The asking price is within 10% of the "
            "machine learning estimate. Compare similar "
            "properties before making a decision."
        )

    elif difference > 0:

        st.warning(
            "The asking price is higher than the AI estimate. "
            "Consider checking comparable properties and "
            "negotiating the price."
        )

    else:

        st.success(
            "The asking price is below the AI estimate. "
            "Check the property's condition, documents and "
            "location before making a decision."
        )

else:

    st.info(
        "The AI valuation is unavailable for this property."
    )

st.caption(
    "AI insights are based on your sample CSV dataset and "
    "Random Forest model. They are estimates, not verified "
    "market valuations or investment advice."
)

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

# =====================================================
# HOME AFFORDABILITY & TRUE COST CALCULATOR
# PROFESSIONAL DASHBOARD VERSION
# =====================================================

st.divider()
st.header("🏡 Home Affordability & Loan Calculator")

st.write(
    "Plan your home purchase by understanding your income, "
    "savings, loan EMI and additional property expenses."
)

st.info(
    "Educational estimates only. Actual home-loan eligibility, "
    "interest rates and purchase charges depend on the lender "
    "and applicable local rules."
)

# =====================================================
# 1. SELECTED PROPERTY INFORMATION FROM YOUR PROJECT
# =====================================================

st.subheader("🏠 1. Selected Property Overview")

property_data = properties[
    (properties["location"].astype(str).str.strip() == str(location).strip()) &
    (properties["property_type"].astype(str).str.strip() == str(property_type).strip())
].copy()

p1, p2, p3, p4 = st.columns(4)

p1.metric("Selected Location", location)
p2.metric("Property Type", property_type)
p3.metric("Asking Price", f"₹{price_lakh:,.2f} L")
p4.metric("Property Area", f"{area:,.0f} sq. ft.")

# Compare with actual CSV records
if not property_data.empty:

    average_price = property_data["price_lakh"].median()
    average_rent = property_data["monthly_rent"].median()
    average_area = property_data["area_sqft"].median()

    st.markdown("#### 📊 Dataset Comparison")

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Sample Median Property Price",
        f"₹{average_price:,.2f} L"
    )

    d2.metric(
        "Sample Median Monthly Rent",
        f"₹{average_rent:,.0f}"
    )

    d3.metric(
        "Sample Median Property Area",
        f"{average_area:,.0f} sq. ft."
    )

    st.caption(
        f"Comparison uses {len(property_data)} matching records "
        f"from your CSV for {location} and {property_type}."
    )

else:
    average_price = None
    average_rent = None

    st.warning(
        "No matching property records are available "
        "for this location and property type."
    )

# =====================================================
# 2. YOUR FINANCIAL PROFILE
# =====================================================

st.divider()
st.subheader("💰 2. Your Financial Profile")

st.caption(
    "Enter your household income, current loan payments "
    "and savings to estimate your home-buying capacity."
)

col1, col2 = st.columns(2)

with col1:

    monthly_income = st.number_input(
        "Monthly Household Income (₹)",
        min_value=0,
        value=80000,
        step=5000,
        key="aff_income",
        help="Total monthly income earned by all household members."
    )

    existing_emi = st.number_input(
        "Existing Monthly Loan EMIs (₹)",
        min_value=0,
        value=5000,
        step=1000,
        key="aff_existing_emi",
        help="Monthly payments for your existing loans."
    )

with col2:

    savings = st.number_input(
        "Available Home-Buying Savings (₹)",
        min_value=0,
        value=1000000,
        step=50000,
        key="aff_savings",
        help="Savings available for your down payment and purchase costs."
    )

    monthly_maintenance = st.number_input(
        "Estimated Monthly Property Maintenance (₹)",
        min_value=0,
        value=3000,
        step=500,
        key="aff_maintenance",
        help="Estimated monthly society maintenance and property upkeep."
    )

# =====================================================
# 3. HOME LOAN CONFIGURATION
# =====================================================

st.divider()
st.subheader("🏦 3. Home Loan Configuration")

st.caption(
    "Choose your down payment, annual interest rate "
    "and repayment period."
)

col3, col4, col5 = st.columns(3)

with col3:

    down_payment_percent = st.slider(
        "Down Payment (%)",
        min_value=10,
        max_value=50,
        value=20,
        key="aff_down_payment",
        help="Percentage of property price paid using your own money."
    )

with col4:

    interest_rate = st.number_input(
        "Annual Home Loan Interest Rate (%)",
        min_value=1.0,
        max_value=20.0,
        value=8.5,
        step=0.25,
        key="aff_interest",
        help="Assumed yearly interest rate on your home loan."
    )

with col5:

    loan_years = st.slider(
        "Loan Tenure (Years)",
        min_value=5,
        max_value=30,
        value=20,
        key="aff_tenure",
        help="Number of years taken to repay the loan."
    )

# =====================================================
# 4. ADDITIONAL PROPERTY PURCHASE COSTS
# =====================================================

st.divider()
st.subheader("🧾 4. Additional Property Purchase Costs")

st.caption(
    "Estimate additional expenses such as stamp duty, "
    "registration and other purchase-related charges."
)

purchase_cost_percent = st.number_input(
    "Estimated Additional Buying Costs (% of Property Price)",
    min_value=0.0,
    max_value=20.0,
    value=7.0,
    step=0.5,
    key="aff_purchase_costs",
    help="Estimated percentage for registration, stamp duty and other expenses."
)

st.caption(
    "This is an assumption. Actual government charges and "
    "other expenses may vary by location and property."
)

# =====================================================
# 5. FINANCIAL CALCULATIONS
# =====================================================

monthly_rate = interest_rate / 1200
number_of_payments = loan_years * 12

if monthly_rate > 0:

    emi_factor = (
        monthly_rate * (1 + monthly_rate) ** number_of_payments
        / ((1 + monthly_rate) ** number_of_payments - 1)
    )

else:

    emi_factor = 1 / number_of_payments

# Assumed 35% monthly income limit
assumed_income_limit = monthly_income * 0.35

available_monthly_emi = max(
    0,
    assumed_income_limit - existing_emi - monthly_maintenance
)

affordable_loan = (
    available_monthly_emi / emi_factor
    if emi_factor > 0 else 0
)

down_fraction = down_payment_percent / 100
cost_fraction = purchase_cost_percent / 100

# Income-based property budget
income_budget = (
    affordable_loan / (1 - down_fraction)
    if down_fraction < 1 else 0
)

# Savings-based property budget
cash_budget = (
    savings / (down_fraction + cost_fraction)
    if down_fraction + cost_fraction > 0 else 0
)

# Final estimated maximum budget
estimated_home_budget = min(income_budget, cash_budget)

estimated_down_payment = estimated_home_budget * down_fraction
estimated_extra_costs = estimated_home_budget * cost_fraction

estimated_loan = max(
    0,
    estimated_home_budget - estimated_down_payment
)

estimated_emi = estimated_loan * emi_factor

estimated_monthly_total = (
    estimated_emi + monthly_maintenance + existing_emi
)

total_interest = (
    estimated_emi * number_of_payments - estimated_loan
)

total_loan_repayment = estimated_emi * number_of_payments

initial_cash_required = (
    estimated_down_payment + estimated_extra_costs
)

remaining_savings = savings - initial_cash_required

# =====================================================
# 6. AFFORDABILITY RESULTS
# =====================================================

st.divider()
st.subheader("📊 5. Your Home Affordability Results")

st.caption(
    "These results estimate the home price you may afford "
    "based on your financial inputs and selected loan settings."
)

r1, r2, r3 = st.columns(3)

r1.metric(
    "Maximum Estimated Home Budget",
    f"₹{estimated_home_budget / 100000:.2f} L"
)

r2.metric(
    "Estimated Home Loan Amount",
    f"₹{estimated_loan / 100000:.2f} L"
)

r3.metric(
    "Estimated Monthly EMI",
    f"₹{estimated_emi:,.0f}"
)

r4, r5, r6 = st.columns(3)

r4.metric(
    "Required Down Payment",
    f"₹{estimated_down_payment:,.0f}"
)

r5.metric(
    "Estimated Buying Expenses",
    f"₹{estimated_extra_costs:,.0f}"
)

r6.metric(
    "Total Initial Cash Required",
    f"₹{initial_cash_required:,.0f}"
)

# =====================================================
# 7. SELECTED PROPERTY AFFORDABILITY CHECK
# =====================================================

st.divider()
st.subheader("🔍 6. Can You Afford This Selected Property?")

selected_price = price_lakh * 100000

selected_down_payment = selected_price * down_fraction
selected_extra_cost = selected_price * cost_fraction

selected_loan = selected_price - selected_down_payment

selected_emi = selected_loan * emi_factor

selected_initial_cash = (
    selected_down_payment + selected_extra_cost
)

selected_monthly_outgo = (
    selected_emi + monthly_maintenance + existing_emi
)

selected_income_ratio = (
    selected_monthly_outgo / monthly_income * 100
    if monthly_income > 0 else 0
)

cash_shortfall = max(0, selected_initial_cash - savings)

budget_difference = estimated_home_budget - selected_price

a1, a2, a3 = st.columns(3)

a1.metric(
    "Selected Property Price",
    f"₹{selected_price / 100000:.2f} L"
)

a2.metric(
    "Estimated EMI for This Property",
    f"₹{selected_emi:,.0f}"
)

a3.metric(
    "Initial Cash Required",
    f"₹{selected_initial_cash:,.0f}"
)

if selected_price <= estimated_home_budget and cash_shortfall == 0:

    st.success(
        "The selected property is within your estimated "
        "income-based budget and available savings."
    )

elif selected_price > estimated_home_budget:

    st.warning(
        f"The selected property is approximately "
        f"₹{abs(budget_difference) / 100000:.2f} lakh "
        "above your estimated affordable budget."
    )

else:

    st.warning(
        f"You need approximately ₹{cash_shortfall:,.0f} "
        "more savings for the estimated initial payment."
    )

st.metric(
    "Monthly Housing Outgo as % of Income",
    f"{selected_income_ratio:.1f}%"
)

# =====================================================
# 8. LOAN REPAYMENT SUMMARY
# =====================================================

st.divider()
st.subheader("📈 7. Loan Repayment Summary")

loan1, loan2, loan3 = st.columns(3)

loan1.metric(
    "Total Loan Repayment",
    f"₹{total_loan_repayment:,.0f}"
)

loan2.metric(
    "Total Estimated Interest",
    f"₹{total_interest:,.0f}"
)

loan3.metric(
    "Loan Duration",
    f"{loan_years} Years"
)

st.caption(
    "Total repayment includes the estimated principal "
    "and interest across the selected loan tenure."
)

# =====================================================
# 9. VISUAL FINANCIAL ANALYSIS
# =====================================================

st.divider()
st.subheader("📊 8. Visual Financial Analysis")

chart1, chart2 = st.columns(2)

with chart1:

    st.markdown("#### Loan Principal vs Interest")

    fig1, ax1 = plt.subplots()

    ax1.pie(
        [estimated_loan, max(0, total_interest)],
        labels=["Loan Principal", "Interest"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax1.axis("equal")
    st.pyplot(fig1)
    plt.close(fig1)

with chart2:

    st.markdown("#### Monthly Expense Breakdown")

    expense_data = pd.Series({
        "New Home EMI": estimated_emi,
        "Existing EMIs": existing_emi,
        "Maintenance": monthly_maintenance
    })

    fig2, ax2 = plt.subplots()

    expense_data.plot(
        kind="bar",
        ax=ax2
    )

    ax2.set_ylabel("Amount (₹)")
    ax2.set_xlabel("Monthly Expenses")
    ax2.tick_params(axis="x", rotation=15)

    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

# =====================================================
# 10. FINANCIAL RECOMMENDATION
# =====================================================

st.divider()
st.subheader("💡 9. Financial Recommendation")

if monthly_income == 0:

    st.warning(
        "Enter your monthly household income "
        "to calculate your affordability."
    )

elif estimated_home_budget <= 0:

    st.warning(
        "Your current income or savings may not be "
        "sufficient for the selected loan assumptions. "
        "Review your financial inputs."
    )

else:

    if selected_price <= estimated_home_budget and cash_shortfall == 0:

        st.success(
            "Your selected property fits within the "
            "calculator's estimated budget and savings limit."
        )

    else:

        st.info(
            "Consider a lower-priced property, a larger "
            "down payment or additional savings."
        )

st.write("### Understanding Your Results")

st.markdown(
    """
    - **Home Budget:** Estimated maximum property price.
    - **Down Payment:** Your contribution towards the property.
    - **Loan Amount:** Estimated amount borrowed from a lender.
    - **EMI:** Monthly principal and interest repayment.
    - **Buying Expenses:** Estimated additional purchase costs.
    - **Total Monthly Outgo:** New EMI, existing EMIs and maintenance.
    """
)

# =====================================================
# 11. DOWNLOAD FINANCIAL REPORT
# =====================================================

st.divider()
st.subheader("📥 10. Download Your Financial Report")

financial_report = pd.DataFrame([{
    "Location": location,
    "Property Type": property_type,
    "Property Price (₹)": selected_price,
    "Monthly Income (₹)": monthly_income,
    "Existing EMIs (₹)": existing_emi,
    "Available Savings (₹)": savings,
    "Down Payment (%)": down_payment_percent,
    "Interest Rate (%)": interest_rate,
    "Loan Tenure (Years)": loan_years,
    "Estimated Home Budget (₹)": estimated_home_budget,
    "Estimated Loan (₹)": estimated_loan,
    "Estimated Monthly EMI (₹)": estimated_emi,
    "Estimated Buying Costs (₹)": estimated_extra_costs,
    "Initial Cash Required (₹)": selected_initial_cash,
    "Total Monthly Outgo (₹)": selected_monthly_outgo,
    "Estimated Total Interest (₹)": total_interest
}])

st.download_button(
    "📄 Download Home Affordability Report (CSV)",
    data=financial_report.to_csv(index=False).encode("utf-8"),
    file_name="home_affordability_report.csv",
    mime="text/csv",
    use_container_width=True
)

st.caption(
    "All figures are estimates based on user inputs and "
    "illustrative assumptions. This tool is not a bank approval, "
    "loan offer, property valuation or financial advice."
)

# ==========================================
# SMART PROPERTY ANALYZER - NEW FEATURES
# ==========================================

import streamlit as st

st.divider()
st.header("🏡 Smart Property Risk & Opportunity Analyzer")

st.write(
    "Analyze the locality and estimate possible "
    "property investment returns."
)


# ==========================================
# FEATURE 1: AUTOMATIC SMART LOCALITY ANALYSIS
# ==========================================

st.subheader("📍 1. Smart Locality Analysis")

st.caption(
    f"Locality information is automatically calculated "
    f"from your CSV dataset for {location}."
)

# Get only properties from the selected location
locality_data = properties[
    properties["location"].astype(str).str.strip() == location
].copy()

if locality_data.empty:

    st.warning(
        f"No locality data is available for {location}. "
        "Please add records for this location in your CSV."
    )

else:

    # --------------------------------------
    # Clean and process CSV values
    # --------------------------------------

    # Fix spelling variations
    locality_data["water_supply"] = (
        locality_data["water_supply"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "avarage": "Average",
            "average": "Average",
            "good": "Good",
            "poor": "Poor",
            "unknown": "Unknown"
        })
    )

    # Extract number from values like 3/month
    power_values = pd.to_numeric(
        locality_data["power_cuts_per_month"]
        .astype(str)
        .str.extract(r"(\d+(?:\.\d+)?)")[0],
        errors="coerce"
    )

    # Convert internet quality into numerical scores
    internet_mapping = {
        "poor": 3,
        "average": 6,
        "good": 8,
        "excellent": 10,
        "exelent": 10
    }

    internet_values = (
        locality_data["internet_quality"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(internet_mapping)
    )

    # --------------------------------------
    # Calculate locality statistics
    # --------------------------------------

    water_mode = locality_data["water_supply"].mode()

    water = (
        water_mode.iloc[0]
        if not water_mode.empty else "Unknown"
    )

    avg_power_cuts = power_values.mean()

    avg_internet = internet_values.mean()

    avg_hospital_distance = (
        pd.to_numeric(
            locality_data["hospital_distance_km"],
            errors="coerce"
        ).mean()
    )

    # --------------------------------------
    # Calculate locality score
    # --------------------------------------

    water_scores = {
        "Good": 100,
        "Average": 60,
        "Poor": 20,
        "Unknown": None
    }

    water_score = water_scores.get(water)

    electricity_score = (
        max(0, 100 - avg_power_cuts * 5)
        if pd.notna(avg_power_cuts) else None
    )

    internet_score = (
        avg_internet * 10
        if pd.notna(avg_internet) else None
    )

    available_scores = [
        (water_score, 0.40),
        (electricity_score, 0.30),
        (internet_score, 0.30)
    ]

    available_scores = [
        (score, weight)
        for score, weight in available_scores
        if score is not None
    ]

    total_weight = sum(
        weight for score, weight in available_scores
    )

    locality_score = (
        sum(
            score * weight
            for score, weight in available_scores
        ) / total_weight
        if total_weight > 0 else 0
    )

    # --------------------------------------
    # Display automatic locality dashboard
    # --------------------------------------

    st.markdown(f"### 📊 {location} Locality Dashboard")

    st.caption(
        f"Based on {len(locality_data)} property records "
        "in your dataset."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Locality Score",
        f"{locality_score:.1f}/100"
    )

    c2.metric(
        "Water Supply",
        water
    )

    c3.metric(
        "Power Cuts / Month",
        f"{avg_power_cuts:.1f}"
        if pd.notna(avg_power_cuts) else "N/A"
    )

    c4.metric(
        "Internet Quality",
        f"{avg_internet:.1f}/10"
        if pd.notna(avg_internet) else "N/A"
    )

    st.divider()

    c5, c6 = st.columns(2)

    c5.metric(
        "Average Hospital Distance",
        f"{avg_hospital_distance:.2f} km"
        if pd.notna(avg_hospital_distance) else "N/A"
    )

    c6.metric(
        "Properties Analysed",
        len(locality_data)
    )

    # --------------------------------------
    # Locality recommendation
    # --------------------------------------

    if locality_score >= 80:
        st.success(
            f"{location} has a good estimated locality score."
        )

    elif locality_score >= 50:
        st.warning(
            f"{location} has a moderate estimated locality score."
        )

    else:
        st.error(
            f"{location} has a low estimated locality score."
        )

    # --------------------------------------
    # Show selected location records
    # --------------------------------------

    with st.expander("View locality data from CSV"):

        st.dataframe(
            locality_data[
                [
                    "property_name",
                    "location",
                    "water_supply",
                    "power_cuts_per_month",
                    "internet_quality",
                    "hospital_distance_km"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Scores are illustrative calculations based on your "
        "CSV records, not verified live locality information. "
        "Hospital distance is displayed separately and is not "
        "included in the locality score."
    )


# ==========================================
# FEATURE 2: FUTURE INVESTMENT ANALYSIS
# ==========================================

st.divider()
st.subheader("📈 2. Future Investment Analysis")

st.write(
    "Estimate possible future property values "
    "using different annual growth assumptions."
)

col3, col4 = st.columns(2)

with col3:
    property_price = st.number_input(
        "Current Property Price (₹ lakh)",
        min_value=1.0,
        value=50.0,
        step=1.0,
        key="new_property_price"
    )

    monthly_rent = st.number_input(
        "Expected Monthly Rent (₹)",
        min_value=0,
        value=20000,
        step=1000,
        key="new_monthly_rent"
    )

with col4:
    annual_expenses = st.number_input(
        "Annual Maintenance and Other Costs (₹)",
        min_value=0,
        value=30000,
        step=5000,
        key="new_annual_expenses"
    )

    years = st.slider(
        "Investment Period (Years)",
        min_value=1,
        max_value=10,
        value=5,
        key="new_investment_years"
    )

st.caption(
    "Growth rates below are assumptions, not predictions "
    "based on verified market data."
)

col5, col6, col7 = st.columns(3)

with col5:
    conservative_growth = st.number_input(
        "Conservative Growth (%)",
        min_value=-20.0,
        max_value=30.0,
        value=2.0,
        step=1.0,
        key="new_conservative_growth"
    )

with col6:
    base_growth = st.number_input(
        "Base Growth (%)",
        min_value=-20.0,
        max_value=30.0,
        value=5.0,
        step=1.0,
        key="new_base_growth"
    )

with col7:
    optimistic_growth = st.number_input(
        "Optimistic Growth (%)",
        min_value=-20.0,
        max_value=30.0,
        value=8.0,
        step=1.0,
        key="new_optimistic_growth"
    )

# Estimate future prices using compound growth.
current_price_rupees = property_price * 100000

scenarios = {
    "Conservative": conservative_growth,
    "Base": base_growth,
    "Optimistic": optimistic_growth
}

results = []

for scenario, growth in scenarios.items():
    future_value = current_price_rupees * (
        1 + growth / 100
    ) ** years

    results.append({
        "Scenario": scenario,
        "Annual Growth (%)": growth,
        "Future Property Value (₹ lakh)": round(
            future_value / 100000, 2
        ),
        "Price Change (₹ lakh)": round(
            (future_value - current_price_rupees) / 100000,
            2
        )
    })

st.write(f"### Estimated Value After {years} Years")

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)

# Calculate estimated net rental yield.
annual_rent = monthly_rent * 12
net_annual_rent = annual_rent - annual_expenses

net_rental_yield = (
    net_annual_rent / current_price_rupees
) * 100

st.metric(
    "Estimated Net Rental Yield",
    f"{net_rental_yield:.2f}%"
)

st.metric(
    "Estimated Annual Rent After Expenses",
    f"₹{net_annual_rent:,.0f}"
)

st.caption(
    "Net rental yield here deducts only the expenses entered. "
    "It excludes loan interest, taxes, vacancy and other "
    "costs unless included above. Future values are estimates, "
    "not guaranteed returns."
)
