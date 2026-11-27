import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import textwrap
import asyncio
import json
import re
import urllib.parse
import urllib.request
import urllib.error
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


/* LIQUID GLASS OVERRIDES — remove dark/black widget surfaces */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stHorizontalBlock"],
[data-testid="stExpander"],
[data-testid="stPopover"],
[data-testid="stDataFrame"],
[data-testid="stTable"],
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.22) !important;
    border: 1px solid rgba(255,255,255,0.72) !important;
    border-radius: 22px !important;
    backdrop-filter: blur(28px) saturate(175%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(175%) !important;
    box-shadow: 0 12px 38px rgba(48,82,130,0.08), inset 0 1px 2px rgba(255,255,255,0.8) !important;
}

/* All select/radio/slider surfaces use translucent glass, not Streamlit dark defaults. */
[data-baseweb="select"] > div,
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-testid="stNumberInput"] [data-baseweb="input"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.40) !important;
    color: #172b49 !important;
    border: 1px solid rgba(255,255,255,0.88) !important;
    border-radius: 15px !important;
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.85) !important;
    backdrop-filter: blur(22px) saturate(170%) !important;
}

[data-baseweb="select"] *,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea { color: #172b49 !important; }

[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background: rgba(255,255,255,0.16) !important;
    border: 1px solid rgba(255,255,255,0.62) !important;
    border-radius: 22px !important;
    overflow: hidden !important;
    backdrop-filter: blur(22px) saturate(170%) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div {
    background: rgba(255,255,255,0.42) !important;
    color: #172b49 !important;
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


def normalize_squareyards_location(value):
    """Normalize common city spellings before sending them to Square Yards."""
    raw = str(value or "").strip()
    aliases = {
        "benguluru": "Bengaluru",
        "bangalore": "Bengaluru",
        "bengaluru": "Bengaluru",
        "gurgaon": "Gurugram",
        "new delhi": "Delhi",
        "bombay": "Mumbai",
        "madras": "Chennai",
        "calcutta": "Kolkata",
    }
    return aliases.get(raw.casefold(), raw)


def _find_listing_image(value, depth=0, image_context=False):
    """Find an HTTP(S) URL only when it belongs to a photo/image field."""
    if depth > 8:
        return None
    image_keys = {
        "image", "images", "imageurl", "image_url", "thumbnail",
        "coverimage", "cover_image", "photourl", "photo_url",
        "photos", "gallery", "media", "propertyimages", "property_images",
    }
    if isinstance(value, str):
        if image_context and value.startswith(("https://", "http://")):
            return value
        return None
    if isinstance(value, list):
        for item in value:
            found = _find_listing_image(item, depth + 1, image_context)
            if found:
                return found
    elif isinstance(value, dict):
        for key, item in value.items():
            normalized_key = str(key).replace("-", "_").casefold()
            compact_key = normalized_key.replace("_", "")
            is_image_field = (
                normalized_key in image_keys
                or compact_key in {k.replace("_", "") for k in image_keys}
            )
            found = _find_listing_image(item, depth + 1, image_context or is_image_field)
            if found:
                return found
    return None


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


@st.cache_data(ttl=900, show_spinner=False)
def squareyards_listing_details(property_id):
    """Fetch one listing's full record so its genuine photo can be displayed if supplied."""
    return asyncio.run(_squareyards_call_async(
        "get_entity_details",
        {"entity": "listing", "id": str(property_id)}
    ))



UNTERA_API_BASE = "https://api.untera.io/api/v1"


def get_untera_api_key():
    """Read the API key from Streamlit Secrets; never hard-code it."""
    try:
        return st.secrets.get("UNTERA_API_KEY", "")
    except Exception:
        return ""


def untera_search(country_code, location_text, transaction, min_price, max_price,
                  min_beds, page_size, _cache_version="v1"):
    """Search Untera listings. The API key is read at request time from Secrets."""
    api_key = get_untera_api_key()
    if not api_key:
        raise RuntimeError(
            "Untera API key not found. Add UNTERA_API_KEY in Streamlit Cloud → "
            "App settings → Secrets, then redeploy."
        )

    params = {
        "country": country_code.upper(),
        "page": 1,
        "pageSize": min(50, max(1, int(page_size))),
    }
    if location_text:
        params["location"] = location_text
    if transaction:
        params["transaction"] = transaction
    if min_price is not None:
        params["minPrice"] = int(min_price)
    if max_price is not None:
        params["maxPrice"] = int(max_price)
    if min_beds is not None:
        params["minBeds"] = int(min_beds)

    url = f"{UNTERA_API_BASE}/listings/search?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={
            "X-API-Key": api_key,
            "Accept": "application/json",
            "User-Agent": "SmartPropertyAI/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        if error.code == 401:
            raise RuntimeError("Untera rejected the API key (401). Check UNTERA_API_KEY in Streamlit Secrets.") from error
        if error.code == 429:
            raise RuntimeError("Untera rate limit reached (429). Wait a little and try again.") from error
        raise RuntimeError(f"Untera API returned HTTP {error.code}: {detail}") from error
    except TimeoutError as error:
        raise RuntimeError("Untera took too long to respond. Please retry.") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Could not connect to Untera: {error.reason}") from error

    if not isinstance(payload, dict):
        raise RuntimeError("Untera returned an unexpected response format.")
    if payload.get("error"):
        err = payload["error"]
        if isinstance(err, dict):
            raise RuntimeError(str(err.get("message") or err.get("code") or err))
        raise RuntimeError(str(err))
    return payload


@st.cache_data(ttl=3600, show_spinner=False)
def untera_listing_details(listing_id):
    """Fetch a listing's detail record as a fallback when search has no photo URL."""
    api_key = get_untera_api_key()
    if not api_key or not listing_id:
        return {}

    safe_id = urllib.parse.quote(str(listing_id), safe="")
    url = f"{UNTERA_API_BASE}/listings/{safe_id}"
    request = urllib.request.Request(
        url,
        headers={
            "X-API-Key": api_key,
            "Accept": "application/json",
            "User-Agent": "SmartPropertyAI/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload if isinstance(payload, (dict, list)) else {}
    except Exception:
        # A detail lookup must never break the main property search.
        return {}


def _first_value(record, *keys):
    for key in keys:
        value = record.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def _listing_image_urls(record):
    """Return distinct real image URLs found in provider image/photo fields only."""
    image_keys = {
        "image", "images", "imageurl", "imageurls", "image_url", "photo", "photos",
        "photourl", "photourls", "photo_url", "picture", "pictures", "pictureurl",
        "picture_url", "thumbnail", "thumbnailurl", "thumbnail_url", "cover",
        "coverimage", "cover_image", "primaryimage", "primary_image", "mainimage",
        "main_image", "propertyimage", "propertyimages", "property_image",
        "listingimage", "listingimages", "listing_image", "media", "gallery",
        "galleryimages", "gallery_images",
    }
    url_keys = {"url", "src", "href", "secure_url", "original", "original_url",
                "large", "medium", "full", "image_url", "imageurl", "photo_url", "photourl"}
    image_keys = {re.sub(r"[^a-z0-9]", "", k.casefold()) for k in image_keys}
    url_keys = {re.sub(r"[^a-z0-9]", "", k.casefold()) for k in url_keys}
    found, seen = [], set()

    def add(candidate):
        if not isinstance(candidate, str):
            return
        candidate = candidate.strip()
        if not candidate.startswith(("https://", "http://")):
            return
        # The provider may use CDN URLs without a file extension; the enclosing
        # images/photos field is the signal that this URL represents a photo.
        if candidate not in seen:
            seen.add(candidate)
            found.append(candidate)

    def walk(value, image_context=False, depth=0):
        if depth > 14:
            return
        if isinstance(value, str):
            if image_context:
                add(value)
        elif isinstance(value, list):
            for child in value:
                walk(child, image_context, depth + 1)
        elif isinstance(value, dict):
            # URLs inside photo objects are valid only when nested below a photo field.
            for key, child in value.items():
                normalized = re.sub(r"[^a-z0-9]", "", str(key).casefold())
                if image_context and normalized in url_keys:
                    walk(child, True, depth + 1)
            for key, child in value.items():
                normalized = re.sub(r"[^a-z0-9]", "", str(key).casefold())
                walk(child, image_context or normalized in image_keys, depth + 1)

    walk(record)
    return found


def _untera_image(record):
    """Return the first genuine photo URL supplied in an Untera listing record."""
    urls = _listing_image_urls(record)
    return urls[0] if urls else None


def _country_code_from_label(country_label):
    """Country label to ISO-3166 alpha-2 code for Untera."""
    country_codes = {
        "United Arab Emirates": "AE", "UAE": "AE", "United States": "US",
        "USA": "US", "United Kingdom": "GB", "UK": "GB", "Canada": "CA",
        "Australia": "AU", "Singapore": "SG", "Portugal": "PT", "Spain": "ES",
        "Italy": "IT", "France": "FR", "Germany": "DE", "Netherlands": "NL",
        "Greece": "GR", "Turkey": "TR", "Türkiye": "TR", "Thailand": "TH",
        "Japan": "JP", "Indonesia": "ID", "Malaysia": "MY", "Mexico": "MX",
        "Brazil": "BR", "South Africa": "ZA", "New Zealand": "NZ",
        "Ireland": "IE", "Switzerland": "CH", "Austria": "AT", "Belgium": "BE",
        "Cyprus": "CY", "Croatia": "HR", "Poland": "PL", "Czechia": "CZ",
        "Czech Republic": "CZ", "Sweden": "SE", "Norway": "NO", "Denmark": "DK",
        "Finland": "FI", "Romania": "RO", "Bulgaria": "BG", "Hungary": "HU",
        "Philippines": "PH", "Vietnam": "VN", "Sri Lanka": "LK",
        "Saudi Arabia": "SA", "Qatar": "QA", "Oman": "OM", "Bahrain": "BH",
        "India": "IN",
    }
    return country_codes.get(country_label, "")


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
            <a href="#live-properties" target="_parent"
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

        <a href="#live-properties" target="_parent" style="
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

    # Detect common Indian cities from the locality/address text.
    # If no city is recognised, retain the supplied location instead of
    # incorrectly grouping every other Indian city under "Other".
    city_names = [
        "Mumbai", "Navi Mumbai", "Thane", "Panvel", "Pune", "Bengaluru",
        "Bangalore", "Hyderabad", "Chennai", "Delhi", "New Delhi", "Noida",
        "Greater Noida", "Gurugram", "Gurgaon", "Faridabad", "Ghaziabad",
        "Kolkata", "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Jaipur",
        "Jodhpur", "Udaipur", "Indore", "Bhopal", "Nagpur", "Nashik",
        "Aurangabad", "Chhatrapati Sambhajinagar", "Lucknow", "Kanpur",
        "Varanasi", "Prayagraj", "Agra", "Meerut", "Chandigarh", "Mohali",
        "Panchkula", "Ludhiana", "Amritsar", "Jalandhar", "Dehradun",
        "Haridwar", "Kochi", "Cochin", "Thiruvananthapuram", "Trivandrum",
        "Kozhikode", "Coimbatore", "Madurai", "Mysuru", "Mysore", "Mangaluru",
        "Mangalore", "Visakhapatnam", "Vizag", "Vijayawada", "Guntur",
        "Bhubaneswar", "Cuttack", "Patna", "Ranchi", "Jamshedpur", "Raipur",
        "Guwahati", "Shillong", "Imphal", "Siliguri", "Panaji", "Goa",
        "Vasai", "Virar", "Kalyan", "Dombivli", "Ulhasnagar", "Amravati",
        "Kolhapur", "Solapur", "Satara", "Nanded", "Jalgaon", "Akola"
    ]
    def detect_city(value):
        text = str(value).strip()
        lower = text.lower()
        # Prefer longer names first (e.g. Navi Mumbai before Mumbai).
        for city_name in sorted(city_names, key=len, reverse=True):
            if city_name.lower() in lower:
                if city_name == "Bangalore": return "Bengaluru"
                if city_name == "Gurgaon": return "Gurugram"
                if city_name == "Cochin": return "Kochi"
                if city_name == "Trivandrum": return "Thiruvananthapuram"
                if city_name == "Mysore": return "Mysuru"
                if city_name == "Mangalore": return "Mangaluru"
                if city_name == "Vizag": return "Visakhapatnam"
                return city_name
        return text if text else "Other"

    df["city"] = df["location"].apply(detect_city)
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
# SINGLE API-BASED PROPERTY EXPLORER
# The old CSV/manual Property Analysis sidebar has been removed.
# Existing dashboard analytics use a neutral sample record until a live API
# listing is selected from the Explore Properties results below.
# ==========================================

_default_property = properties.iloc[0]
location = str(_default_property.get("city", "Mumbai") or "Mumbai")
property_type = str(_default_property.get("property_type", "Apartment") or "Apartment")
price_lakh = float(_default_property.get("price_lakh", 120) or 120)
area = max(50, int(float(_default_property.get("area_sqft", 1000) or 1000)))
age = max(0, int(float(_default_property.get("building_age", 5) or 5)))
monthly_rent = max(0, int(float(_default_property.get("monthly_rent", 30000) or 30000)))
compare_location = True

# Selecting a live listing in the API results updates these dashboard values
# on the next Streamlit rerun.
_selected_live = st.session_state.get("selected_live_property", {})
_selected_is_international = (
    isinstance(_selected_live, dict) and bool(_selected_live.get("_is_international"))
)
_selected_listing_display = dict(_selected_live) if isinstance(_selected_live, dict) else {}
# Keep foreign-currency listings out of the INR-trained model inputs.
# Their listing details remain available for the dashboard selection notice.
if _selected_is_international:
    _selected_live = {}

if isinstance(_selected_live, dict) and _selected_live:
    _live_city = _selected_live.get("city") or _selected_live.get("locality") or _selected_live.get("location")
    if _live_city:
        location = str(_live_city)
    _live_type = _selected_live.get("propertyType") or _selected_live.get("property_type") or _selected_live.get("type")
    if _live_type:
        property_type = str(_live_type)
    _live_area = _selected_live.get("areaSqft") or _selected_live.get("area_sqft") or _selected_live.get("area")
    try:
        if _live_area:
            area = max(50, int(float(re.sub(r"[^0-9.]", "", str(_live_area)))))
    except (TypeError, ValueError):
        pass
    _live_age = _selected_live.get("buildingAge") or _selected_live.get("building_age") or _selected_live.get("age")
    try:
        if _live_age is not None:
            age = max(0, int(float(_live_age)))
    except (TypeError, ValueError):
        pass
    _live_price = None if _selected_is_international else (_selected_live.get("priceLakh") or _selected_live.get("price_lakh"))
    if _live_price is None:
        _price_raw = _selected_live.get("priceText") or _selected_live.get("price")
        if isinstance(_price_raw, (int, float)):
            _live_price = float(_price_raw) / 100000 if float(_price_raw) >= 100000 else float(_price_raw)
        elif _price_raw:
            _price_text = str(_price_raw).replace(",", "")
            _price_number = re.search(r"([0-9]+(?:\.[0-9]+)?)", _price_text)
            if _price_number:
                _price_value = float(_price_number.group(1))
                if "cr" in _price_text.lower() or "crore" in _price_text.lower():
                    _live_price = _price_value * 100
                elif "lakh" in _price_text.lower() or re.search(r"\bL\b", _price_text, re.I):
                    _live_price = _price_value
                elif "₹" in _price_text or "rs" in _price_text.lower():
                    _live_price = _price_value / 100000 if _price_value >= 100000 else _price_value
    try:
        if _live_price is not None:
            price_lakh = max(1.0, float(_live_price))
    except (TypeError, ValueError):
        pass
    _live_rent = _selected_live.get("monthlyRent") or _selected_live.get("monthly_rent")
    try:
        if _live_rent is not None:
            monthly_rent = max(0, int(float(_live_rent)))
        elif str(_selected_live.get("listingType", "")).lower() == "rent" and _live_price is not None:
            monthly_rent = max(0, int(float(_live_price) * 100000))
    except (TypeError, ValueError):
        pass

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


predicted_lakh = 0.0 if _selected_is_international else max(0, float(model.predict(input_data)[0]))
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

if _selected_is_international:
    st.warning(
        "An international listing is selected. Its original currency is preserved, "
        "but the current valuation, affordability and locality models are trained on "
        "Indian sample data in INR. They are intentionally not applied to this foreign listing; the existing dashboard below remains based on its Indian sample dataset."
    )
    st.info(
        "Selected international listing: "
        + str(_selected_listing_display.get("title") or "Property listing")
        + " · "
        + str(_selected_listing_display.get("_display_price") or "Price not supplied")
        + " · "
        + str(_selected_listing_display.get("_display_location") or _selected_listing_display.get("city") or "")
    )
else:
    st.caption("Choose ‘Use this listing for AI dashboard’ on any live API result to apply that property’s available details to the dashboard. Until then, dashboard estimates use a sample property from the model dataset.")

st.caption(
    "Your intelligent real estate dashboard powered by "
    "machine learning and property data analytics."
)

# ==========================================
# UNIFIED LIVE PROPERTY SEARCH — INDIA + GLOBAL
# ==========================================
st.divider()
st.markdown('<div id="live-properties"></div>', unsafe_allow_html=True)
st.markdown("## 🌐 Explore Properties — India & Worldwide")
st.caption(
    "Search Indian listings through Square Yards and international listings "
    "through Untera. Enter a city, locality, state or region in the location field."
)

country_options = [
    "India", "United Arab Emirates", "United States", "United Kingdom",
    "Canada", "Australia", "Singapore", "Portugal", "Spain", "Italy",
    "France", "Germany", "Netherlands", "Greece", "Turkey", "Thailand",
    "Japan", "Indonesia", "Malaysia", "Mexico", "Brazil", "South Africa",
    "New Zealand", "Ireland", "Switzerland", "Austria", "Belgium", "Cyprus",
    "Croatia", "Poland", "Czechia", "Sweden", "Norway", "Denmark", "Finland",
    "Romania", "Bulgaria", "Hungary", "Philippines", "Vietnam", "Sri Lanka",
    "Saudi Arabia", "Qatar", "Oman", "Bahrain", "Other (ISO-2 country code)"
]

with st.container(border=True):
    search_col1, search_col2, search_col3 = st.columns([1.1, 1.3, 1])
    with search_col1:
        live_country = st.selectbox(
            "Country / market",
            country_options,
            index=0,
            key="global_search_country",
            help="India uses Square Yards. Other countries use the Untera international listings API."
        )
    with search_col2:
        live_city = st.text_input(
            "City, locality, state or region",
            value="",
            placeholder="e.g. Mumbai, Dubai, New York, London",
            key="global_search_location"
        ).strip()
    with search_col3:
        live_search_type = st.selectbox(
            "Listing purpose",
            ["For sale", "For rent"],
            key="global_search_transaction"
        )

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    is_india_search = live_country == "India"
    currency_label = "₹ lakh" if is_india_search else "USD"
    default_max_budget = 200 if is_india_search else 500000

    with filter_col1:
        live_min_budget = st.number_input(
            f"Minimum budget ({currency_label})",
            min_value=0,
            value=0,
            step=5 if is_india_search else 10000,
            key="global_search_min_budget"
        )
    with filter_col2:
        live_max_budget = st.number_input(
            f"Maximum budget ({currency_label})",
            min_value=0,
            value=default_max_budget,
            step=5 if is_india_search else 25000,
            key="global_search_max_budget"
        )
    with filter_col3:
        live_bhk = st.selectbox(
            "Bedrooms",
            ["Any", "1", "2", "3", "4", "5"],
            key="global_search_bedrooms"
        )
    with filter_col4:
        live_result_count = st.selectbox(
            "Results to show", [5, 10, 20, 30, 50], index=1,
            key="global_search_result_count"
        )

    other_country_code = ""
    if live_country == "Other (ISO-2 country code)":
        other_country_code = st.text_input(
            "Country ISO-2 code",
            placeholder="e.g. AE, PT, JP",
            max_chars=2,
            key="global_search_other_country"
        ).strip().upper()
        st.caption("Use the two-letter country code, for example AE = UAE, PT = Portugal, JP = Japan.")

    run_live_search = st.button(
        "🔎 Search Properties",
        type="primary",
        use_container_width=True,
        key="run_unified_property_search"
    )

    if run_live_search:
        if not live_city:
            st.warning("Enter a city, locality, state or region before searching.")
        elif live_max_budget and live_min_budget > live_max_budget:
            st.warning("Minimum budget cannot be greater than maximum budget.")
        elif live_country == "Other (ISO-2 country code)" and not re.fullmatch(r"[A-Z]{2}", other_country_code):
            st.warning("Enter a valid two-letter ISO country code, such as AE or PT.")
        else:
            try:
                if is_india_search:
                    # Preserve the existing Square Yards India search flow.
                    normalized_city = normalize_squareyards_location(live_city)
                    min_price = int(live_min_budget * 100000) if live_min_budget else None
                    max_price = int(live_max_budget * 100000) if live_max_budget else None
                    bhk_value = live_bhk if live_bhk != "Any" else None
                    tool_name = "search_properties"
                    args = {
                        "listingType": "Sale" if live_search_type == "For sale" else "Rent",
                        "location": normalized_city,
                        "page": 1,
                        "size": int(live_result_count),
                    }
                    if bhk_value:
                        args["bedrooms"] = f"{bhk_value} BHK"
                    if min_price is not None:
                        args["minPrice"] = min_price
                    if max_price is not None:
                        args["maxPrice"] = max_price
                    args = {key: value for key, value in args.items() if value is not None}

                    with st.spinner(f"Searching Square Yards for properties in {normalized_city}..."):
                        live_payload = squareyards_search(tool_name, json.dumps(args, sort_keys=True))
                    live_rows = _extract_squareyards_rows(live_payload, ["listings", "results"])
                    provider_name = "Square Yards"
                    display_location = normalized_city
                    currency_code = "INR"
                else:
                    country_code = (
                        other_country_code
                        if live_country == "Other (ISO-2 country code)"
                        else _country_code_from_label(live_country)
                    )
                    if not country_code:
                        st.error("This country is not mapped yet. Choose Other and enter its ISO-2 code.")
                        st.stop()

                    min_price = int(live_min_budget) if live_min_budget else None
                    max_price = int(live_max_budget) if live_max_budget else None
                    beds = int(live_bhk) if live_bhk != "Any" else None

                    with st.spinner(f"Searching Untera listings in {live_country}..."):
                        live_payload = untera_search(
                            country_code,
                            live_city,
                            "sale" if live_search_type == "For sale" else "rent",
                            min_price,
                            max_price,
                            beds,
                            int(live_result_count),
                        )
                    live_rows = live_payload.get("results", [])
                    if not isinstance(live_rows, list):
                        live_rows = []
                    provider_name = "Untera"
                    display_location = live_city
                    currency_code = "USD"

                if live_rows:
                    # Remove duplicate listing records before rendering cards.
                    unique_rows = []
                    seen_listing_keys = set()
                    for candidate in live_rows:
                        if not isinstance(candidate, dict):
                            continue
                        candidate_id = _first_value(candidate, "id", "listing_id", "listingId", "propertyId", "propertyid")
                        candidate_title = str(_first_value(candidate, "title", "name") or "").strip().casefold()
                        candidate_place = str(_first_value(candidate, "address", "locality", "location", "city") or "").strip().casefold()
                        dedupe_key = (str(candidate_id).strip() if candidate_id else f"{candidate_title}|{candidate_place}")
                        if dedupe_key and dedupe_key not in seen_listing_keys:
                            seen_listing_keys.add(dedupe_key)
                            unique_rows.append(candidate)
                    live_rows = unique_rows
                    seen_photo_urls = set()
                    st.success(
                        f"Found {len(live_rows)} unique {live_search_type.lower()} result(s) "
                        f"for {display_location}. Showing up to {len(live_rows)}."
                    )
                    for row_start in range(0, len(live_rows), 2):
                        card_cols = st.columns(2)
                        for card_col, item in zip(card_cols, live_rows[row_start:row_start + 2]):
                            if not isinstance(item, dict):
                                continue
                            with card_col:
                                if is_india_search:
                                    title = _first_value(item, "title", "name") or "Property listing"
                                    place = ", ".join(str(x) for x in [
                                        item.get("locality"), item.get("city")
                                    ] if x)
                                    price_value = _first_value(item, "priceText", "price")
                                    if isinstance(price_value, (int, float)):
                                        price_display = f"₹{price_value:,.0f}"
                                    else:
                                        price_display = str(price_value) if price_value is not None else "Price not supplied"
                                    area_value = _first_value(item, "areaSqft", "areaText", "area")
                                    bedrooms_value = _first_value(item, "bhk", "bedrooms")
                                    image_candidates = _listing_image_urls(item)
                                    listing_id = _first_value(item, "id", "propertyId", "propertyid")
                                    if not image_candidates and listing_id:
                                        try:
                                            detail_payload = squareyards_listing_details(listing_id)
                                            image_candidates = _listing_image_urls(detail_payload)
                                        except Exception:
                                            image_candidates = []
                                    listing_url = _first_value(item, "url", "link", "propertyUrl", "detailUrl")
                                    map_location = _first_value(item, "address", "locality", "location") or place or display_location
                                    map_country = "India"
                                else:
                                    title = _first_value(item, "title", "name") or "International property listing"
                                    place = ", ".join(str(x) for x in [
                                        item.get("address"), item.get("city"), item.get("countryName") or item.get("country")
                                    ] if x)
                                    usd_price = _first_value(item, "price_usd", "priceUsd")
                                    original_price = _first_value(item, "original_price", "originalPrice")
                                    original_currency = _first_value(item, "original_currency", "originalCurrency")
                                    if original_price is not None and original_currency:
                                        price_display = f"{original_currency} {original_price:,.0f}" if isinstance(original_price, (int, float)) else f"{original_currency} {original_price}"
                                    elif usd_price is not None:
                                        price_display = f"US$ {float(usd_price):,.0f}"
                                    else:
                                        price_display = "Price not supplied"
                                    area_value = _first_value(item, "area_sqm", "areaSqm", "size_sqm", "area")
                                    bedrooms_value = _first_value(item, "bedrooms", "beds")
                                    listing_id = _first_value(item, "id", "listing_id", "listingId")
                                    image_candidates = _listing_image_urls(item)

                                    # Search results normally include images. If a result has
                                    # no photo URL, try the listing detail endpoint once.
                                    if not image_candidates and listing_id:
                                        detail_payload = untera_listing_details(listing_id)
                                        image_candidates = _listing_image_urls(detail_payload)

                                    listing_url = _first_value(item, "url", "listing_url", "source_url", "sourceUrl", "listingUrl")
                                    map_location = _first_value(item, "address", "location", "city") or display_location
                                    map_country = live_country
                                    if area_value is not None:
                                        try:
                                            area_value = f"{float(area_value):,.0f} m²"
                                        except (TypeError, ValueError):
                                            area_value = str(area_value)

                                # Never reuse one property's photo for another listing.
                                # If the provider has no unique actual photo, show an honest placeholder.
                                image_url = next(
                                    (candidate for candidate in image_candidates if candidate not in seen_photo_urls),
                                    None
                                )
                                if image_url:
                                    seen_photo_urls.add(image_url)
                                    st.image(image_url, use_container_width=True)
                                    st.caption(f"Actual listing photo supplied by {provider_name}")
                                else:
                                    st.markdown(
                                        "<div style='height:210px;display:flex;align-items:center;justify-content:center;"
                                        "border:1px dashed rgba(90,120,160,.45);border-radius:18px;"
                                        "background:rgba(255,255,255,.30);color:#60748d;text-align:center;padding:18px;'>"
                                        "<div><div style='font-size:34px;'>🏡</div>"
                                        "<b>Actual photo not provided</b><br><small>We won't substitute a random property image.</small></div></div>",
                                        unsafe_allow_html=True
                                    )

                                st.markdown(f"**{title}**")
                                if place:
                                    st.caption(f"📍 {place}")
                                st.markdown(f"### {price_display}")

                                detail_parts = []
                                if bedrooms_value:
                                    detail_parts.append(f"{bedrooms_value} bedrooms")
                                if area_value:
                                    detail_parts.append(str(area_value))
                                prop_type = _first_value(item, "type", "property_type", "propertyType")
                                if prop_type:
                                    detail_parts.append(str(prop_type))
                                if detail_parts:
                                    st.write(" · ".join(detail_parts))

                                if is_india_search and item.get("isVerified") is True:
                                    st.caption("✓ Square Yards verified listing")

                                map_query = urllib.parse.quote(f"{title}, {map_location}, {map_country}")
                                st.link_button(
                                    "🗺️ View this property on Google Maps",
                                    f"https://www.google.com/maps/search/?api=1&query={map_query}",
                                    use_container_width=True
                                )
                                if listing_url and str(listing_url).startswith(("https://", "http://")):
                                    st.link_button("View original listing", str(listing_url), use_container_width=True)

                                if st.button(
                                    "Use this listing for AI dashboard",
                                    key=f"use_global_listing_{provider_name}_{listing_id or row_start}_{str(title)[:30]}",
                                    use_container_width=True
                                ):
                                    selected_live = dict(item)
                                    selected_live["_provider"] = provider_name
                                    selected_live["_country_code"] = currency_code
                                    selected_live["_country_name"] = live_country
                                    selected_live["_is_international"] = not is_india_search
                                    selected_live.setdefault("city", item.get("city") or display_location)
                                    selected_live.setdefault(
                                        "listingType",
                                        "Rent" if live_search_type == "For rent" else "Sale"
                                    )
                                    if not is_india_search:
                                        selected_live["_display_price"] = price_display
                                        selected_live["_display_location"] = display_location
                                    st.session_state["selected_live_property"] = selected_live
                                    st.rerun()
                                st.divider()
                else:
                    api_message = (
                        live_payload.get("message") or live_payload.get("note")
                        if isinstance(live_payload, dict) else None
                    )
                    st.info(api_message or "No listings matched. Try a nearby city, a broader location or a wider budget.")
            except ImportError:
                st.error(
                    "The Square Yards MCP package is missing. Install the project's "
                    "requirements.txt dependencies and redeploy."
                )
            except Exception as error:
                st.error(f"Property search could not be completed: {error}")
                st.caption("Check the country, location and API key settings, then try again.")

    if not is_india_search:
        st.markdown(
            '<div style="font-size:12px;color:#60748d;margin-top:8px;">'
            'Powered by '
            '<a href="https://untera.io" target="_blank">Untera</a>'
            '</div>',
            unsafe_allow_html=True
        )

st.caption(
    "Data note: Square Yards listings are informational and may not reflect "
    "current availability or final transaction prices. Verify details with the listing provider. "
    "The AI estimate uses a sample-data model and is not a live market valuation. "
    "Only unique photo URLs supplied by the listing provider are displayed. Missing or repeated photos are shown as unavailable, never replaced with stock images."
)

# ==========================================
# 1. MAIN PROPERTY KPI CARDS
# ==========================================

st.markdown("### 📊 Property Overview")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "🏠 Asking Price",
    _selected_listing_display.get("_display_price", "N/A") if _selected_is_international else f"₹{price_lakh:,.1f} L"
)

m2.metric(
    "🤖 AI Estimated Value",
    "Not available for international listings" if _selected_is_international else f"₹{predicted_lakh:,.1f} L"
)

m3.metric(
    "📐 Price / Sq. Ft.",
    "N/A" if _selected_is_international else f"₹{price_per_sqft:,.0f}"
)

m4.metric(
    "💰 Rental Yield",
    "N/A" if _selected_is_international else f"{gross_yield:.2f}%"
)

st.divider()


# CSV-backed featured-property cards removed. The single Explore Properties
# feature above is the live Square Yards search and is the source for property discovery.

# ==========================================
# 3. AI PROPERTY ANALYTICS
# ==========================================

st.markdown('<div id="ai-insights"></div>', unsafe_allow_html=True)

ai_col1, ai_col2 = st.columns(2)

# AI valuation insight
with ai_col1:

    st.markdown("#### 📈 AI Price Analysis")

    if _selected_is_international:
        st.info("AI valuation is unavailable for this international listing because the current model is trained on Indian INR-denominated sample data.")
    else:
        st.metric(
            "AI Estimated Property Value",
            f"₹{predicted_lakh:,.2f} L"
        )

        st.write(
            f"Your asking price is ₹{price_lakh:,.2f} lakh."
        )

    if _selected_is_international:
        pass
    elif difference > 0:

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

    if _selected_is_international:
        st.info("Rental yield and INR price-per-square-foot metrics are not calculated for this foreign-currency listing.")
    else:
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
import urllib.request
import urllib.error

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

if _selected_is_international:
    st.warning("This calculator currently uses INR and Indian home-loan assumptions. It is not applied to the selected international listing; enter an Indian property selection before relying on these figures.")

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
