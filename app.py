import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# SmartProperty AI
# Beginner-friendly property analysis demo
# -----------------------------
st.set_page_config(page_title="SmartProperty AI", page_icon="🏡", layout="wide")

DATA_FILE = Path(__file__).parent / "data" / "properties.csv"

st.title("🏡 SmartProperty AI")
st.subheader("Simple property price and rental analysis")
st.caption("Student project demo • Sample listings are illustrative, not verified market data.")

@st.cache_data
def load_properties():
    return pd.read_csv(DATA_FILE)

properties = load_properties()

with st.sidebar:
    st.header("Property details")
    location = st.selectbox(
        "Location",
        sorted(properties["location"].dropna().unique().tolist()),
        index=0
    )
    property_type = st.selectbox("Property type", ["Apartment", "House", "Shop", "Office"])
    price_lakh = st.number_input("Asking price (₹ lakh)", min_value=1.0, max_value=10000.0, value=60.0, step=1.0)
    area = st.number_input("Carpet area (sq. ft.)", min_value=50.0, max_value=100000.0, value=600.0, step=10.0)
    age = st.number_input("Building age (years)", min_value=0, max_value=150, value=5, step=1)
    monthly_rent = st.number_input("Expected monthly rent (₹)", min_value=0, max_value=10000000, value=15000, step=1000)
    compare_location_only = st.checkbox("Compare with selected location", value=True)

price_rupees = price_lakh * 100000
price_per_sqft = price_rupees / area if area > 0 else 0
annual_rent = monthly_rent * 12
gross_yield = (annual_rent / price_rupees * 100) if price_rupees > 0 else 0

# Compare against sample listing data using the same area basis (carpet area).
comparison = properties.copy()
if compare_location_only:
    comparison = comparison[comparison["location"] == location]

comparison = comparison[comparison["area_sqft"] > 0].copy()
comparison["price_per_sqft"] = comparison["price_lakh"] * 100000 / comparison["area_sqft"]
median_price = comparison["price_per_sqft"].median() if not comparison.empty else None

st.markdown("### Your property analysis")
c1, c2, c3 = st.columns(3)
c1.metric("Price per sq. ft.", f"₹{price_per_sqft:,.0f}")
c2.metric("Gross rental yield", f"{gross_yield:.2f}%")
c3.metric("Annual rent", f"₹{annual_rent:,.0f}")

st.markdown("### Explainable assessment")
if median_price is None or pd.isna(median_price):
    st.warning("There are no comparison listings for this selection. Add more sample data before comparing.")
else:
    difference = ((price_per_sqft - median_price) / median_price) * 100 if median_price else 0
    st.write(f"Selected area: **{location}**")
    st.write(f"Median price per sq. ft. in the sample: **₹{median_price:,.0f}**")
    st.write(f"Your entered property is **{abs(difference):.1f}% {'above' if difference > 0 else 'below' if difference < 0 else 'at'}** the sample median by price per sq. ft.")
    if difference > 10:
        st.info("Assessment: The asking price is noticeably above this sample's median. Check whether location, condition, floor, amenities, and building age explain the difference.")
    elif difference < -10:
        st.info("Assessment: The asking price is noticeably below this sample's median. Verify the listing details, condition, title, and other possible reasons before drawing conclusions.")
    else:
        st.info("Assessment: The asking price is within about 10% of this sample's median. Compare more similar properties before judging value.")

if monthly_rent > 0:
    st.write(f"At ₹{monthly_rent:,.0f} monthly rent, gross annual rent is **₹{annual_rent:,.0f}**.")
    st.caption("Gross rental yield excludes maintenance, repairs, taxes, vacancy, and buying costs. It is not net return.")

st.markdown("### Compare sample listings")
if not comparison.empty:
    display = comparison.copy()
    display["Asking price (₹ lakh)"] = display["price_lakh"].map(lambda x: f"₹{x:,.1f} lakh")
    display["Carpet area (sq. ft.)"] = display["area_sqft"].map(lambda x: f"{x:,.0f}")
    display["Price / sq. ft."] = display["price_per_sqft"].map(lambda x: f"₹{x:,.0f}")
    st.dataframe(
        display[["property_name", "location", "property_type", "Asking price (₹ lakh)", "Carpet area (sq. ft.)", "Price / sq. ft."]],
        use_container_width=True,
        hide_index=True
    )

    chart_data = comparison.sort_values("price_per_sqft")
    fig, ax = plt.subplots()
    ax.bar(chart_data["property_name"], chart_data["price_per_sqft"])
    ax.set_title("Sample listing price per sq. ft.")
    ax.set_ylabel("₹ per sq. ft.")
    ax.set_xlabel("Sample property")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.warning("No comparison data available for this location.")

st.markdown("### Download your analysis")
report = pd.DataFrame([{
    "location": location,
    "property_type": property_type,
    "asking_price_lakh": price_lakh,
    "carpet_area_sqft": area,
    "building_age_years": age,
    "monthly_rent_rupees": monthly_rent,
    "price_per_sqft_rupees": round(price_per_sqft, 2),
    "annual_rent_rupees": annual_rent,
    "gross_rental_yield_percent": round(gross_yield, 2),
    "sample_median_price_per_sqft": round(float(median_price), 2) if median_price is not None and not pd.isna(median_price) else None
}])
st.download_button(
    "Download analysis as CSV",
    data=report.to_csv(index=False).encode("utf-8"),
    file_name="smartproperty_analysis.csv",
    mime="text/csv"
)

st.divider()
st.caption("Limitations: This demo uses illustrative sample listings. It is not a valuation, investment recommendation, legal check, or guarantee of market price. Verify all property information independently.")
