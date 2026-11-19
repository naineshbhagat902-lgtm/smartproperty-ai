import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import textwrap
import asyncio
import json
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

/* =========================================
   SMARTPROPERTY AI — IPHONE LIQUID GLASS
========================================= */

:root {
    --glass-white: rgba(255, 255, 255, 0.20);
    --glass-border: rgba(255, 255, 255, 0.62);
    --glass-shadow: 0 12px 40px rgba(40, 70, 120, 0.10);
    --text-main: #17243a;
    --text-muted: #687991;
    --blue-glow: rgba(105, 180, 255, 0.28);
}

/* MAIN BACKGROUND */

.stApp {
    background:
        radial-gradient(
            circle at 12% 12%,
            rgba(105, 190, 255, 0.30),
            transparent 34%
        ),
        radial-gradient(
            circle at 88% 18%,
            rgba(174, 150, 255, 0.24),
            transparent 36%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(130, 220, 255, 0.22),
            transparent 40%
        ),
        linear-gradient(
            135deg,
            #eaf4ff,
            #f5f7ff 48%,
            #e9f1ff
        ) !important;

    color: var(--text-main);
    font-family: "Inter", -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif;
}

/* MAIN CONTENT WIDTH */

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* HEADINGS */

h1, h2, h3, h4 {
    color: var(--text-main) !important;
    font-weight: 750 !important;
    letter-spacing: -0.7px;
}

/* =========================================
   TRANSPARENT GLASS SIDEBAR
========================================= */

section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.22) !important;
    border-right: 1px solid rgba(255,255,255,0.65);
    backdrop-filter: blur(35px) saturate(180%);
    -webkit-backdrop-filter: blur(35px) saturate(180%);
    box-shadow: 8px 0 35px rgba(60, 100, 160, 0.08);
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
    padding: 2rem 1.2rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stCaption {
    color: #263b58 !important;
}

/* SIDEBAR SELECT BOXES */

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.38) !important;
    border: 1px solid rgba(255,255,255,0.85) !important;
    border-radius: 15px !important;
    backdrop-filter: blur(20px);
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.9);
}

/* SIDEBAR INPUTS */

section[data-testid="stSidebar"] input {
    background: rgba(255,255,255,0.38) !important;
    color: #17243a !important;
    border: 1px solid rgba(255,255,255,0.85) !important;
    border-radius: 15px !important;
}

/* SIDEBAR SPACING */

section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.9rem;
}

/* =========================================
   GLASS METRIC CARDS
========================================= */

[data-testid="stMetric"] {
    position: relative;
    overflow: hidden;

    background: rgba(255,255,255,0.30) !important;
    border: 1px solid rgba(255,255,255,0.82) !important;
    border-radius: 23px !important;

    padding: 20px 17px !important;

    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);

    box-shadow:
        0 12px 35px rgba(50,80,130,0.09),
        inset 0 1px 2px rgba(255,255,255,0.95);

    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow:
        0 18px 42px rgba(60,110,180,0.15),
        0 0 22px rgba(255,255,255,0.8),
        inset 0 1px 2px white;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-weight: 650 !important;
}

[data-testid="stMetricValue"] {
    color: #172b49 !important;
    font-weight: 780 !important;
    overflow-wrap: anywhere !important;
}

/* =========================================
   GLASS PROPERTY CARDS
========================================= */

div[data-testid="stVerticalBlockBorderWrapper"]:has(
    [class*="st-key-property-card-"]
) {
    position: relative;
    overflow: hidden;

    background: rgba(255,255,255,0.25) !important;
    border: 1px solid rgba(255,255,255,0.82) !important;
    border-radius: 26px !important;

    backdrop-filter: blur(32px) saturate(190%);
    -webkit-backdrop-filter: blur(32px) saturate(190%);

    box-shadow:
        0 15px 45px rgba(45,75,125,0.10),
        inset 0 1px 2px rgba(255,255,255,0.95);

    transition: all 0.35s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(
    [class*="st-key-property-card-"]
):hover {
    transform: translateY(-7px);
    background: rgba(255,255,255,0.42) !important;
    box-shadow:
        0 22px 55px rgba(45,90,155,0.16),
        0 0 25px rgba(255,255,255,0.8);
}

/* PROPERTY CARD CONTENT */

div[data-testid="stVerticalBlockBorderWrapper"]:has(
    [class*="st-key-property-card-"]
) > div {
    background: transparent !important;
}

/* PROPERTY IMAGES */

div[data-testid="stVerticalBlockBorderWrapper"]:has(
    [class*="st-key-property-card-"]
) [data-testid="stImage"] img {
    border-radius: 19px !important;
    object-fit: cover;
}

/* PROPERTY PRICE */

.property-price {
    color: #347fc7 !important;
    font-size: 25px;
    font-weight: 800;
}

/* =========================================
   GLASS INPUTS
========================================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: rgba(255,255,255,0.40) !important;
    border: 1px solid rgba(255,255,255,0.90) !important;
    border-radius: 14px !important;
    color: #17243a !important;
    backdrop-filter: blur(18px);
}

/* =========================================
   GLASS BUTTONS
========================================= */

.stButton > button,
.stDownloadButton > button,
.stLinkButton > a {
    background: rgba(255,255,255,0.38) !important;
    color: #1b4775 !important;

    border: 1px solid rgba(255,255,255,0.90) !important;
    border-radius: 16px !important;

    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);

    box-shadow:
        0 7px 22px rgba(50,90,150,0.09),
        inset 0 1px 2px white;

    font-weight: 700;
    transition: all 0.3s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stLinkButton > a:hover {
    background: rgba(255,255,255,0.72) !important;
    border-color: white !important;
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(65,130,200,0.16);
}

/* =========================================
   GLASS TABLES AND EXPANDERS
========================================= */

[data-testid="stDataFrame"],
[data-testid="stExpander"],
[data-testid="stAlert"] {
    border: 1px solid rgba(255,255,255,0.75);
    border-radius: 19px !important;
    overflow: hidden;
}

/* GENERAL DIVIDERS */

hr {
    border-color: rgba(255,255,255,0.75) !important;
}

/* RESPONSIVE MOBILE DESIGN */

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    h1 {
        font-size: 28px !important;
    }

    [data-testid="stMetric"] {
        border-radius: 18px !important;
        padding: 14px !important;
    }
}

</style>
""", unsafe_allow_html=True)



BASE_DIR = Path(__file__).parent
# Support the normal project path and the CSV filename uploaded for this update.
DATA_CANDIDATES = [
    BASE_DIR / "data" / "properties.csv",
    BASE_DIR / "properties.csv",
    BASE_DIR / "properties-3.csv",
]
DATA_FILE = next((path for path in DATA_CANDIDATES if path.is_file()), DATA_CANDIDATES[0])

SQUAREYARDS_MCP_URL = "https://sy-mcp.squareyards.com/mcp/external"


async def _squareyards_call_async(tool_name, arguments):
    """Call Square Yards' public, read-only MCP endpoint (no API key required)."""
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    async with streamablehttp_client(SQUAREYARDS_MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)

            if getattr(result, "isError", False):
                messages = [getattr(item, "text", "") for item in (result.content or [])]
                raise RuntimeError("; ".join(message for message in messages if message) or "Square Yards returned an error.")

            structured = getattr(result, "structuredContent", None)
            if structured is not None:
                return structured

            for item in (result.content or []):
                item_text = getattr(item, "text", None)
                if item_text:
                    try:
                        return json.loads(item_text)
                    except json.JSONDecodeError:
                        return {"message": item_text}
            return {}


@st.cache_data(ttl=900, show_spinner=False)
def squareyards_search(tool_name, arguments_json):
    """Cache identical searches for 15 minutes to avoid unnecessary requests."""
    arguments = json.loads(arguments_json)
    return asyncio.run(_squareyards_call_async(tool_name, arguments))


def _extract_squareyards_rows(payload, preferred_keys):
    """Handle MCP structured output and JSON/text-wrapped output safely."""
    if not isinstance(payload, dict):
        return []
    for key in preferred_keys:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    # Some MCP servers wrap the useful response in a result/data property.
    for key in ("data", "result", "structuredContent"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            rows = _extract_squareyards_rows(nested, preferred_keys)
            if rows:
                return rows
    return []




st.components.v1.html("""
<div style="
    width:100%;
    min-height:470px;
    border-radius:30px;
    overflow:hidden;
    position:relative;
    background-image:
        linear-gradient(
            100deg,
            rgba(8,25,48,0.78),
            rgba(8,25,48,0.20)
        ),
        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=2000&q=85');
    background-size:cover;
    background-position:center;
    margin-bottom:35px;
    box-shadow:0 25px 70px rgba(30,65,110,0.20);
">

    <!-- FLOATING GLASS NAVIGATION -->

    <div style="
        margin:20px;
        padding:18px 25px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        flex-wrap:wrap;
        gap:15px;
        border:1px solid rgba(255,255,255,0.48);
        border-radius:22px;
        background:rgba(255,255,255,0.16);
        backdrop-filter:blur(25px);
        -webkit-backdrop-filter:blur(25px);
        box-shadow:inset 0 1px 2px rgba(255,255,255,0.7);
    ">

        <div style="
            color:white;
            font-size:21px;
            font-weight:800;
            letter-spacing:-0.5px;
        ">
            SMARTPROPERTY AI
            <div style="
                font-size:9px;
                letter-spacing:3px;
                color:rgba(255,255,255,0.82);
                margin-top:5px;
            ">
                REAL ESTATE INTELLIGENCE
            </div>
        </div>

        <div style="
            display:flex;
            gap:20px;
            flex-wrap:wrap;
            font-size:13px;
        ">
            <a href="#featured-properties" target="_parent"
               style="color:white;text-decoration:none;">Properties</a>

            <a href="#ai-insights" target="_parent"
               style="color:white;text-decoration:none;">AI Insights</a>

            <a href="#affordability" target="_parent"
               style="color:white;text-decoration:none;">Affordability</a>

            <a href="#investment-analysis" target="_parent"
               style="color:white;text-decoration:none;">Investment</a>
        </div>
    </div>

    <!-- HERO TEXT -->

    <div style="
        padding:65px 40px 85px;
        max-width:760px;
    ">

        <div style="
            display:inline-block;
            padding:9px 16px;
            border:1px solid rgba(255,255,255,0.45);
            border-radius:30px;
            background:rgba(255,255,255,0.15);
            backdrop-filter:blur(15px);
            color:white;
            font-size:11px;
            letter-spacing:2px;
            margin-bottom:22px;
        ">
            ✦ SMART PROPERTY INTELLIGENCE
        </div>

        <div style="
            color:white;
            font-size:clamp(35px,5vw,62px);
            font-weight:800;
            line-height:1.12;
            letter-spacing:-2px;
            margin-bottom:20px;
            text-shadow:0 3px 20px rgba(0,0,0,0.2);
        ">
            Find Your Dream Home.<br>
            Invest With Intelligence.
        </div>

        <div style="
            color:rgba(255,255,255,0.90);
            font-size:16px;
            line-height:1.8;
            max-width:570px;
            margin-bottom:30px;
        ">
            Discover properties, understand market value and
            make smarter real estate decisions with AI-powered insights.
        </div>

        <a href="#featured-properties" target="_parent" style="
            display:inline-block;
            padding:15px 26px;
            border:1px solid rgba(255,255,255,0.85);
            border-radius:17px;
            background:rgba(255,255,255,0.27);
            backdrop-filter:blur(22px);
            -webkit-backdrop-filter:blur(22px);
            color:white;
            text-decoration:none;
            font-size:13px;
            font-weight:750;
            box-shadow:inset 0 1px 2px rgba(255,255,255,0.8);
        ">
            EXPLORE PROPERTIES →
        </a>

    </div>
</div>
""", height=550, scrolling=False)


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


# ==========================================
# PREMIUM PROPERTY DETAILS SIDEBAR
# ==========================================

with st.sidebar:

    
    st.markdown(
        """
<div style="
    background: rgba(255,255,255,0.30);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 22px;
    padding: 22px 16px;
    margin-bottom: 18px;
    box-shadow: 0 8px 30px rgba(50,100,160,0.12);
">
    <div style="color:#377fc1;font-size:12px;
                font-weight:800;letter-spacing:3px;">
        SMARTPROPERTY AI
    </div>
    <div style="color:#172b49;font-size:23px;
                font-weight:800;margin-top:12px;">
        Property Details
    </div>
    <div style="color:#63758c;font-size:12px;margin-top:8px;">
        Configure your property to explore AI insights.
    </div>
</div>
        """,
        unsafe_allow_html=True
    )




    st.markdown("##### 📍 PROPERTY LOCATION")

    location = st.selectbox(
        "City",
        sorted(properties["city"].unique())
    )

    property_type = st.selectbox(
        "Property type",
        sorted(properties["property_type"].unique())
    )

    st.divider()

    st.markdown("##### 🏡 PROPERTY SPECIFICATIONS")

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

    st.divider()

    st.markdown("##### 💰 RENTAL INFORMATION")

    monthly_rent = st.number_input(
        "Expected monthly rent (₹)",
        min_value=0,
        max_value=10000000,
        value=15000,
        step=1000
    )

    st.divider()

    compare_location = st.checkbox(
        "Compare with selected location",
        value=True
    )

    st.caption(
        "Your selections automatically update the property analysis."
    )

# Calculations
price_rupees = price_lakh * 100000
price_per_sqft = price_rupees / area
annual_rent = monthly_rent * 12
gross_yield = annual_rent / price_rupees * 100

selected_city = location

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
st.markdown("## Property Dashboard")

st.caption(
    "Your intelligent real estate dashboard powered by "
    "machine learning and property data analytics."
)

# ==========================================
# SQUARE YARDS LIVE PROPERTY SEARCH (INDIA)
# ==========================================
st.divider()
st.markdown("## 🌐 Explore Properties Across India")
st.caption(
    "Search Square Yards' property database for sale listings, rentals, "
    "and new projects in Indian cities. No API key is required."
)

with st.container(border=True):
    live_col1, live_col2, live_col3 = st.columns([1.25, 1, 1])
    with live_col1:
        live_city = st.text_input(
            "City or locality in India",
            value="Mumbai",
            placeholder="e.g. Pune, Bengaluru, Thane, Jaipur"
        ).strip()
    with live_col2:
        live_search_type = st.selectbox(
            "What are you looking for?",
            ["Properties for sale", "Properties for rent", "New projects"]
        )
    with live_col3:
        live_bhk = st.selectbox(
            "Configuration",
            ["Any", "1 BHK", "2 BHK", "3 BHK", "4 BHK", "5 BHK"]
        )

    budget_col1, budget_col2, budget_col3 = st.columns(3)
    with budget_col1:
        live_min_budget_lakh = st.number_input(
            "Minimum budget (₹ lakh)", min_value=0, max_value=100000,
            value=0, step=5
        )
    with budget_col2:
        live_max_budget_lakh = st.number_input(
            "Maximum budget (₹ lakh)", min_value=0, max_value=100000,
            value=200, step=5
        )
    with budget_col3:
        live_result_count = st.selectbox("Results", [5, 10, 20, 30], index=1)

    run_live_search = st.button(
        "🔎 Search Square Yards", type="primary", use_container_width=True
    )

    if run_live_search:
        if not live_city:
            st.warning("Enter an Indian city or locality to search.")
        elif live_max_budget_lakh and live_min_budget_lakh > live_max_budget_lakh:
            st.warning("Minimum budget cannot be greater than maximum budget.")
        else:
            # Square Yards accepts absolute INR values, not lakh values.
            min_price = int(live_min_budget_lakh * 100000) if live_min_budget_lakh else None
            max_price = int(live_max_budget_lakh * 100000) if live_max_budget_lakh else None
            bhk_value = live_bhk if live_bhk != "Any" else None

            if live_search_type == "New projects":
                tool_name = "search_projects"
                args = {"location": live_city, "page": 1, "paging": int(live_result_count)}
                if bhk_value:
                    args["bhk"] = bhk_value.replace(" BHK", "")
                if min_price is not None:
                    args["minPrice"] = min_price
                if max_price is not None:
                    args["maxPrice"] = max_price
                preferred_keys = ["projects"]
            else:
                tool_name = "search_properties"
                args = {
                    "listingType": "Sale" if live_search_type == "Properties for sale" else "Rent",
                    "location": live_city,
                    "page": 1,
                    "size": int(live_result_count),
                }
                if bhk_value:
                    args["bedrooms"] = bhk_value
                if min_price is not None:
                    args["minPrice" if tool_name == "search_properties" else "minPrice"] = min_price
                if max_price is not None:
                    args["maxPrice"] = max_price
                preferred_keys = ["listings"]

            # A budget of zero is treated as an omitted lower bound.
            args = {key: value for key, value in args.items() if value is not None}
            try:
                with st.spinner("Searching Square Yards property data..."):
                    live_payload = squareyards_search(tool_name, json.dumps(args, sort_keys=True))
                live_rows = _extract_squareyards_rows(live_payload, preferred_keys)

                if live_rows:
                    total_count = live_payload.get("total", len(live_rows)) if isinstance(live_payload, dict) else len(live_rows)
                    st.success(f"Found {total_count} result(s). Showing up to {len(live_rows)}.")
                    for row_start in range(0, len(live_rows), 2):
                        card_cols = st.columns(2)
                        for card_col, item in zip(card_cols, live_rows[row_start:row_start + 2]):
                            with card_col:
                                title = item.get("title") or item.get("name") or "Property listing"
                                place = ", ".join(str(x) for x in [item.get("locality"), item.get("city")] if x)
                                price = item.get("priceText") or item.get("price")
                                if isinstance(price, (int, float)):
                                    price = f"₹{price:,.0f}"
                                area_value = item.get("areaSqft") or item.get("areaText")
                                details = []
                                if item.get("bhk"):
                                    details.append(f"{item.get('bhk')} BHK")
                                if area_value:
                                    details.append(f"{area_value} sq.ft." if isinstance(area_value, (int, float)) else str(area_value))
                                if item.get("pricePerSqft") is not None:
                                    try:
                                        details.append(f"₹{float(item.get('pricePerSqft')):,.0f}/sq.ft.")
                                    except (TypeError, ValueError):
                                        details.append(f"{item.get('pricePerSqft')}/sq.ft.")
                                st.markdown(f"**{title}**")
                                if place:
                                    st.caption(f"📍 {place}")
                                if price is not None:
                                    st.markdown(f"### {price}")
                                if details:
                                    st.write(" · ".join(details))
                                if item.get("isVerified") is True:
                                    st.caption("✓ Square Yards verified listing")
                                listing_url = item.get("url") or item.get("link") or item.get("propertyUrl") or item.get("detailUrl")
                                if listing_url and str(listing_url).startswith("https://"):
                                    st.link_button("View listing", listing_url, use_container_width=True)
                                st.divider()
                else:
                    message = live_payload.get("message") or live_payload.get("note") if isinstance(live_payload, dict) else None
                    st.info(message or "No matching results were returned. Try a broader city/locality or remove the budget limit.")
            except ImportError:
                st.error("Square Yards connection package is missing. Install the updated requirements.txt and redeploy the app.")
            except Exception as error:
                st.error(f"Square Yards search could not be completed: {error}")
                st.caption("Your existing CSV dashboard is still available. Please retry in a moment.")

st.caption(
    "Data note: Square Yards listings are informational and may not reflect "
    "current availability or final transaction prices. Verify details with the listing provider. "
    "Your CSV-based AI estimate is a separate sample-data model, not a live market valuation."
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


st.markdown('<div id="featured-properties"></div>', unsafe_allow_html=True)

st.markdown("## Featured Properties")

st.caption(
    "Discover selected properties from your property database."
)

featured_properties = properties[
    properties["city"] == location
].head(6)

if featured_properties.empty:
    st.info("No properties available for this location.")

else:
    property_columns = st.columns(3)

    for index, (_, prop) in enumerate(
        featured_properties.iterrows()
    ):
        with property_columns[index % 3]:

            with st.container(
    border=True,
    key=f"property-card-{index}"
):

                image_path = prop.get("image_path", "")

                if (
                    pd.notna(image_path)
                    and Path(str(image_path)).is_file()
                ):
                    st.image(
                        str(image_path),
                        use_container_width=True
                    )
                else:
                    st.markdown(
                        """
                        <div style="
                            height:190px;
                            background:#E9E6DF;
                            border-radius:8px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            color:#7C8490;
                            font-size:15px;
                        ">
                            Property Image Unavailable
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"""
                    <div style="
                        color:#B08D57;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:1.5px;
                        margin-top:12px;
                        text-transform:uppercase;
                    ">
                        {prop['property_type']}
                    </div>
                    <div style="
                        color:#101827;
                        font-size:20px;
                        font-weight:750;
                        margin-top:5px;
                        line-height:1.4;
                    ">
                        {prop['property_name']}
                    </div>
                    <div style="
                        color:#78818D;
                        font-size:13px;
                        margin-top:5px;
                    ">
                        📍 {prop['location']}
                    </div>
                    <div style="
                        color:#B08D57;
                        font-size:25px;
                        font-weight:800;
                        margin-top:15px;
                        margin-bottom:12px;
                    ">
                        ₹{float(prop['price_lakh']):,.2f} L
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.divider()

                detail1, detail2 = st.columns(2)

                with detail1:
                    st.markdown("**📐 Area**")
                    st.write(f"{float(prop['area_sqft']):,.0f} sq.ft.")

                with detail2:
                    st.markdown("**💰 Monthly Rent**")
                    st.write(f"₹{float(prop['monthly_rent']):,.0f}")                  
            

st.caption(
    f"🏗️ Building age: "
    f"{float(prop['building_age']):.0f} years"
)
st.divider()


# ==========================================
# 3. AI PROPERTY ANALYTICS
# ==========================================

st.markdown('<div id="ai-insights"></div>', unsafe_allow_html=True)

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
    st.markdown("### Estimated vs Asking Price")

    comparison_chart = pd.DataFrame({
        "Price Type": ["AI Estimate", "Asking Price"],
        "Price (₹ lakh)": [predicted_lakh, price_lakh]
    })

    fig = px.bar(
        comparison_chart,
        x="Price Type",
        y="Price (₹ lakh)",
        color="Price Type",
        text="Price (₹ lakh)",
        color_discrete_sequence=["#60A5FA", "#A78BFA"]
    )

    fig.update_traces(
        marker_line_width=0,
        texttemplate="₹%{y:.2f} L",
        textposition="outside",
        marker_cornerradius=12
    )

    fig.update_layout(
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#243B53", size=14),
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(100,140,200,0.15)",
            zeroline=False
        ),
        xaxis=dict(showgrid=False),
        bargap=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

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
    comparison = comparison[comparison["city"] == location]
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

    st.markdown("### 🏙️ Property Price Distribution")

    fig = px.bar(
        comparison,
        x="property_name",
        y="price_lakh",
        color="price_lakh",
        color_continuous_scale=["#60A5FA", "#A78BFA", "#6366F1"],
        labels={
            "property_name": "Property",
            "price_lakh": "Price (₹ lakh)"
        },
        text="price_lakh"
    )

    fig.update_traces(
        marker_line_width=0,
        texttemplate="₹%{y:.1f} L",
        textposition="outside",
        marker_cornerradius=10
    )

    fig.update_layout(
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#243B53", size=13),
        height=450,
        margin=dict(l=20, r=20, t=40, b=30),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(100,140,200,0.15)"
        ),
        bargap=0.35
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
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
st.markdown('<div id="affordability"></div>', unsafe_allow_html=True)
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
    (properties["city"] == location) &
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


    st.markdown("#### 🏦 Loan Principal vs Interest")

    loan_data = pd.DataFrame({
        "Category": ["Loan Principal", "Total Interest"],
        "Amount": [
            estimated_loan,
            max(0, total_interest)
        ]
    })

    fig1 = px.pie(
        loan_data,
        names="Category",
        values="Amount",
        hole=0.65,
        color="Category",
        color_discrete_sequence=["#60A5FA", "#A78BFA"]
    )

    fig1.update_traces(
        textinfo="percent",
        textfont_size=15,
        marker=dict(
            line=dict(
                color="rgba(255,255,255,0.8)",
                width=3
            )
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Amount: ₹%{value:,.0f}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    fig1.update_layout(
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#243B53", size=13),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.08,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(l=15, r=15, t=30, b=30)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={"displayModeBar": False}
    )
  

with chart2:

    st.markdown("#### 💳 Monthly Expense Breakdown")

    expense_data = pd.DataFrame({
        "Expense": [
            "New Home EMI",
            "Existing EMIs",
            "Maintenance"
        ],
        "Amount": [
            estimated_emi,
            existing_emi,
            monthly_maintenance
        ]
    })

    fig2 = px.bar(
        expense_data,
        x="Amount",
        y="Expense",
        orientation="h",
        color="Expense",
        text="Amount",
        color_discrete_sequence=[
            "#60A5FA",
            "#A78BFA",
            "#34D399"
        ]
    )

    fig2.update_traces(
        texttemplate="₹%{x:,.0f}",
        textposition="outside",
        marker_line_width=0
    )

    fig2.update_layout(
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#243B53", size=13),
        showlegend=False,
        height=400,
        margin=dict(l=20, r=50, t=30, b=20),
        xaxis=dict(
            title="Monthly Amount (₹)",
            showgrid=True,
            gridcolor="rgba(100,140,200,0.15)"
        ),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={"displayModeBar": False}
    )
    

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
    properties["city"] == location
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
st.markdown('<div id="investment-analysis"></div>', unsafe_allow_html=True)
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
