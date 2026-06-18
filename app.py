"""
Solana Wallet Intelligence
===========================
Five-tab Streamlit app — deploy free on Streamlit Community Cloud.
"""

import io
import time
import requests
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from collections import defaultdict
from datetime import datetime, timezone, timedelta

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Solana Wallet Intel",
    page_icon="🔬",
    layout="centered",
)

# ── GLOBAL STYLES ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import font ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root variables ── */
:root {
    --green: #4ade80;
    --green-dim: #22c55e;
    --green-dark: #166534;
    --green-glow: rgba(74, 222, 128, 0.08);
    --bg: #0a0a0a;
    --bg-card: #111111;
    --bg-card-hover: #161616;
    --border: #1f1f1f;
    --border-lit: #2a2a2a;
    --text: #e5e5e5;
    --text-muted: #666666;
    --text-dim: #444444;
    --radius: 8px;
    --radius-lg: 12px;
}

/* ── Kill Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stStatusWidget"] { display: none; }

/* ── Page background ── */
.stApp {
    background-color: var(--bg);
    font-family: 'Outfit', sans-serif;
}
.main .block-container {
    padding: 2rem 1.5rem 4rem;
    max-width: 860px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0d0d0d !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stSidebarContent"] {
    padding: 1.5rem 1rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--border);
    gap: 0;
    padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.25rem !important;
    margin: 0 !important;
    transition: color 0.15s ease, border-color 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
    color: var(--green) !important;
    border-bottom: 2px solid var(--green) !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 2rem 0 0 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--green-dim) !important;
    color: var(--green) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.5rem !important;
    border-radius: var(--radius) !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: var(--green-glow) !important;
    border-color: var(--green) !important;
    color: var(--green) !important;
}
.stButton > button[kind="primary"] {
    background: var(--green-glow) !important;
    border: 1px solid var(--green) !important;
}
.stButton > button:disabled {
    opacity: 0.3 !important;
    cursor: not-allowed !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-lit) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--green-dim) !important;
    box-shadow: 0 0 0 1px rgba(74, 222, 128, 0.15) !important;
}
.stTextInput > label,
.stTextArea > label,
.stSlider > label,
.stFileUploader > label,
.stRadio > label {
    color: var(--text-muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Sliders ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: var(--green) !important;
}
.stSlider [data-testid="stThumbValue"] {
    color: var(--green) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background-color: var(--green) !important;
    border-radius: 2px !important;
}
.stProgress > div {
    background-color: var(--border) !important;
    border-radius: 2px !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem 1.25rem !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: var(--green) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 500 !important;
}

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden;
}
iframe[title="st_dataframe"] {
    background: var(--bg-card) !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stExpander"] summary:hover {
    color: var(--text) !important;
}
[data-testid="stExpander"] > div > div {
    padding: 0 1rem 1rem !important;
}

/* ── Alerts / Info ── */
[data-testid="stAlert"] {
    background: #0f1a0f !important;
    border: 1px solid #1a3a1a !important;
    border-radius: var(--radius) !important;
    color: #86efac !important;
    font-size: 0.85rem !important;
}
.stAlert [data-testid="stMarkdownContainer"] p {
    color: #86efac !important;
}

/* ── Code blocks ── */
code {
    background: #111 !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--green) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    padding: 0.1rem 0.4rem !important;
}

/* ── Radio ── */
.stRadio > div {
    gap: 0.5rem !important;
}
.stRadio [data-baseweb="radio"] {
    gap: 0.5rem !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-lit) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--green-dim) !important;
}

/* ── Checkbox ── */
.stCheckbox label {
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--border-lit) !important;
    color: var(--text-muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border-radius: var(--radius) !important;
}
.stDownloadButton > button:hover {
    border-color: var(--green-dim) !important;
    color: var(--green) !important;
    background: var(--green-glow) !important;
}

/* ── Headings and text ── */
h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: -0.02em !important;
    color: var(--text) !important;
}
h1 { font-size: 1.4rem !important; }
h2 { font-size: 1.1rem !important; }
h3 { font-size: 0.95rem !important; }
p, li {
    color: #999 !important;
    font-size: 0.875rem !important;
    line-height: 1.7 !important;
}
.stMarkdown hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Caption ── */
.stCaption {
    color: var(--text-dim) !important;
    font-size: 0.75rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border-color: var(--border-lit) !important;
    border-radius: var(--radius) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Custom header component ────────────────────────────────────────────────────
def page_header(title: str, subtitle: str):
    st.markdown(f"""
<div style="margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid #1f1f1f;">
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
        <div style="width: 6px; height: 6px; border-radius: 50%; background: #4ade80; box-shadow: 0 0 8px rgba(74,222,128,0.6);"></div>
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #4ade80; letter-spacing: 0.15em; text-transform: uppercase;">{subtitle}</span>
    </div>
    <h1 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 600; color: #e5e5e5; letter-spacing: -0.02em;">{title}</h1>
</div>
""", unsafe_allow_html=True)


def stat_card(label: str, value: str, accent: bool = False):
    color = "#4ade80" if accent else "#e5e5e5"
    return f"""
<div style="background: #111; border: 1px solid #1f1f1f; border-radius: 10px; padding: 1rem 1.25rem;">
    <div style="font-family: 'Outfit', sans-serif; font-size: 0.65rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #555; margin-bottom: 6px;">{label}</div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 500; color: {color};">{value}</div>
</div>"""


def section_label(text: str):
    st.markdown(f"""
<div style="display: flex; align-items: center; gap: 10px; margin: 1.5rem 0 0.75rem;">
    <div style="width: 16px; height: 1px; background: #333;"></div>
    <span style="font-family: 'Outfit', sans-serif; font-size: 0.65rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: #555;">{text}</span>
    <div style="flex: 1; height: 1px; background: #1a1a1a;"></div>
</div>
""", unsafe_allow_html=True)


# ── constants ─────────────────────────────────────────────────────────────────
COHORT_BRACKETS = [
    {"name": "Whale",   "emoji": "🐋", "min_usd": 100_000, "max_usd": float("inf"), "color": "#4ade80"},
    {"name": "Shark",   "emoji": "🦈", "min_usd": 25_000,  "max_usd": 100_000,      "color": "#86efac"},
    {"name": "Dolphin", "emoji": "🐬", "min_usd": 5_000,   "max_usd": 25_000,       "color": "#bbf7d0"},
    {"name": "Fish",    "emoji": "🐟", "min_usd": 500,     "max_usd": 5_000,        "color": "#555"},
    {"name": "Minnow",  "emoji": "🦐", "min_usd": 0,       "max_usd": 500,          "color": "#333"},
]

SKIP_TOKENS = {
    "So11111111111111111111111111111111111111112",
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
}

MAX_WALLETS = 150

ADDRESS_COL_CANDIDATES = [
    "Account", "Wallet Address", "Wallet", "Address", "Owner", "owner", "address", "wallet",
]

PRESET_WALLETS = [
    "5N69dUvxdiQGFaRob32oPSwLuUYTqNgHz6GoEtnrRd8S",
    "AQ8t7FmGaDQ4AqmNtaX2d9NqfACCHb16yKo8BavExWkV",
    "2UGhBWG6K9UJq5iM96t1PebJfCBuNxYgYjwNsvE9nwBw",
    "8qRh4cJDH9bBAgUHHuoudBMoDsNHsrjDVHsAd3PXxZ5A",
    "8H86inoTa6PfeoCgRiuup2ZFkeR6WMQYTJWNtHcdSpQW",
]


# ── shared API helpers ─────────────────────────────────────────────────────────
def get_assets(wallet: str, helius_url: str) -> list:
    payload = {
        "jsonrpc": "2.0", "id": "wai",
        "method": "getAssetsByOwner",
        "params": {
            "ownerAddress": wallet,
            "page": 1, "limit": 1000,
            "displayOptions": {"showFungible": True},
        },
    }
    try:
        r = requests.post(helius_url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json().get("result", {}).get("items", [])
    except Exception:
        return []


def wallet_usd_value(assets: list) -> float:
    total = 0.0
    for item in assets:
        ti = item.get("token_info", {})
        pi = ti.get("price_info", {})
        if pi:
            price  = float(pi.get("price_per_token", 0))
            bal    = float(ti.get("balance", 0))
            dec    = int(ti.get("decimals", 0))
            actual = bal / (10 ** dec) if dec > 0 else bal
            total += actual * price
    return total


def assign_cohort(usd: float) -> dict:
    for b in COHORT_BRACKETS:
        if b["min_usd"] <= usd < b["max_usd"]:
            return b
    return COHORT_BRACKETS[-1]


def detect_address_col(df: pd.DataFrame):
    for col in df.columns:
        if df[col].astype(str).str.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$").any():
            return col
    return None


def parse_wallets_from_csv(uploaded) -> list:
    df = pd.read_csv(io.BytesIO(uploaded.read()))
    col = detect_address_col(df)
    if not col:
        return []
    return df[col].dropna().astype(str).str.strip().unique().tolist()


def detect_holder_address_col(df: pd.DataFrame):
    for cand in ADDRESS_COL_CANDIDATES:
        if cand in df.columns:
            return cand
    return detect_address_col(df)


# ── sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
        <div style="width: 5px; height: 5px; border-radius: 50%; background: #4ade80; box-shadow: 0 0 6px rgba(74,222,128,0.7);"></div>
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #4ade80; letter-spacing: 0.15em; text-transform: uppercase;">Solana</span>
    </div>
    <div style="font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 600; color: #e5e5e5; letter-spacing: -0.01em;">Wallet Intel</div>
</div>
<div style="height: 1px; background: #1f1f1f; margin-bottom: 1.25rem;"></div>
<div style="font-family: 'Outfit', sans-serif; font-size: 0.8rem; color: #666; line-height: 1.65; margin-bottom: 1.25rem;">
    On-chain data tells you what wallets actually hold and what they've actually bought — not what anyone is saying on social media. This tool surfaces those patterns across groups of wallets so you can make more informed decisions about a token before the crowd catches on.
</div>
<div style="height: 1px; background: #1f1f1f; margin-bottom: 1.25rem;"></div>
""", unsafe_allow_html=True)

    components.html("""
<script>
(function() {
    const saved = localStorage.getItem('helius_api_key');
    if (saved) {
        window.parent.postMessage({type: 'helius_key', key: saved}, '*');
    }
})();
window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'save_helius_key')
        localStorage.setItem('helius_api_key', e.data.key);
    if (e.data && e.data.type === 'clear_helius_key')
        localStorage.removeItem('helius_api_key');
});
</script>
""", height=0)

    if "helius_key_value" not in st.session_state:
        st.session_state["helius_key_value"] = ""

    helius_key = st.text_input(
        "Helius API Key",
        type="password",
        placeholder="Paste your key here",
        value=st.session_state["helius_key_value"],
        key="helius_key_input",
    )
    remember = st.checkbox("Remember in this browser", value=True)

    if helius_key:
        st.session_state["helius_key_value"] = helius_key
        if remember:
            components.html(f"""
<script>
window.parent.postMessage({{type: 'save_helius_key', key: '{helius_key}'}}, '*');
</script>
""", height=0)
        else:
            components.html("""
<script>
window.parent.postMessage({type: 'clear_helius_key'}, '*');
</script>
""", height=0)

    if helius_key:
        st.markdown("""
<div style="display: flex; align-items: center; gap: 6px; margin-top: 0.5rem; margin-bottom: 1.25rem;">
    <div style="width: 4px; height: 4px; border-radius: 50%; background: #4ade80;"></div>
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #4ade80;">Connected</span>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div style="display: flex; align-items: center; gap: 6px; margin-top: 0.5rem; margin-bottom: 1.25rem;">
    <div style="width: 4px; height: 4px; border-radius: 50%; background: #555;"></div>
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #555;">No key entered</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="height: 1px; background: #1f1f1f; margin-bottom: 1.25rem;"></div>
<div style="font-family: 'Outfit', sans-serif; font-size: 0.7rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #444; margin-bottom: 0.75rem;">How to get a free API key</div>

<div style="display: flex; flex-direction: column; gap: 0.6rem;">

<div style="display: flex; gap: 10px; align-items: flex-start;">
    <div style="min-width: 18px; height: 18px; border-radius: 50%; background: #1a1a1a; border: 1px solid #2a2a2a; display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #4ade80; margin-top: 1px;">1</div>
    <div style="font-family: 'Outfit', sans-serif; font-size: 0.78rem; color: #555; line-height: 1.5;">Go to <a href="https://helius.dev" target="_blank" style="color: #4ade80; text-decoration: none;">helius.dev</a> and click <span style="color: #888;">Get started free</span></div>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start;">
    <div style="min-width: 18px; height: 18px; border-radius: 50%; background: #1a1a1a; border: 1px solid #2a2a2a; display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #4ade80; margin-top: 1px;">2</div>
    <div style="font-family: 'Outfit', sans-serif; font-size: 0.78rem; color: #555; line-height: 1.5;">Create a free account — no credit card needed</div>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start;">
    <div style="min-width: 18px; height: 18px; border-radius: 50%; background: #1a1a1a; border: 1px solid #2a2a2a; display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #4ade80; margin-top: 1px;">3</div>
    <div style="font-family: 'Outfit', sans-serif; font-size: 0.78rem; color: #555; line-height: 1.5;">From your dashboard, click <span style="color: #888;">Create new API key</span></div>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start;">
    <div style="min-width: 18px; height: 18px; border-radius: 50%; background: #1a1a1a; border: 1px solid #2a2a2a; display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #4ade80; margin-top: 1px;">4</div>
    <div style="font-family: 'Outfit', sans-serif; font-size: 0.78rem; color: #555; line-height: 1.5;">Copy the key and paste it into the field above — it saves automatically</div>
</div>

</div>

<div style="margin-top: 1rem; padding: 0.6rem 0.75rem; background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 6px;">
    <div style="font-family: 'Outfit', sans-serif; font-size: 0.72rem; color: #444; line-height: 1.5;">The free tier gives you 100k credits/month — more than enough for regular use. Your key is stored only in your browser and never sent to any server other than Helius.</div>
</div>
""", unsafe_allow_html=True)


HELIUS_URL = f"https://mainnet.helius-rpc.com/?api-key={helius_key.strip()}" if helius_key else ""


# ── tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Cohort Analyzer",
    "Whale Overlap",
    "Recent Buys",
    "Watchlist",
    "Common Holders",
])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — COHORT ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    page_header("Cohort Analyzer", "Holder Intelligence")
    st.markdown("""
<p style="font-family: 'Outfit', sans-serif; font-size: 0.9rem; color: #555; margin-bottom: 0.5rem; margin-top: -1rem; line-height: 1.65;">
Most tools show you who holds the most tokens. This shows you who holds the most <em style="color: #888;">money</em> — 
which is a different question. A wallet holding 1M tokens means more if it also holds $500k in other assets 
than if it's a fresh wallet with nothing else. Cohort analysis tells you the quality of your holder base, not just the size.
</p>
""", unsafe_allow_html=True)

    section_label("Load wallets to analyze")
    st.markdown("""
<div style="font-family: 'Outfit', sans-serif; font-size: 0.82rem; color: #555; line-height: 1.65; margin-bottom: 1rem;">
You have three ways to bring in wallet addresses:
</div>
<div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.25rem;">
    <div style="display: flex; gap: 10px; align-items: flex-start;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #4ade80; padding-top: 2px; min-width: 20px;">01</div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 0.82rem; color: #666; line-height: 1.5;"><span style="color: #999;">Paste a list</span> — copy any wallet addresses and paste them one per line into the text box below</div>
    </div>
    <div style="display: flex; gap: 10px; align-items: flex-start;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #4ade80; padding-top: 2px; min-width: 20px;">02</div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 0.82rem; color: #666; line-height: 1.5;"><span style="color: #999;">Type them in</span> — works the same way, just type or paste addresses directly</div>
    </div>
    <div style="display: flex; gap: 10px; align-items: flex-start;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #4ade80; padding-top: 2px; min-width: 20px;">03</div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 0.82rem; color: #666; line-height: 1.5;"><span style="color: #999;">Upload a CSV</span> — the most powerful option. Go to a token page on <a href="https://solscan.io" target="_blank" style="color: #4ade80; text-decoration: none;">Solscan</a>, click the <strong style="color: #888;">Holders</strong> tab, then <strong style="color: #888;">Export</strong>. That CSV drops straight in here — address column is detected automatically.</div>
    </div>
</div>
""", unsafe_allow_html=True)

    input_method = st.radio(
        "Input method",
        ["Paste / type addresses", "Upload CSV"],
        key="c1_input_method",
        horizontal=True,
    )

    c1_wallets_raw = []
    c1_file = None

    if input_method == "Paste / type addresses":
        raw_c1 = st.text_area(
            "Wallet addresses (one per line)",
            height=140,
            placeholder="7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU\nAQ8t7FmGaDQ4AqmNtaX2d9NqfACCHb16yKo8BavExWkV\n...",
            key="c1_paste",
        )
        if raw_c1.strip():
            c1_wallets_raw = [w.strip() for w in raw_c1.strip().splitlines() if len(w.strip()) >= 32]
            st.caption(f"{len(c1_wallets_raw)} addresses detected.")
    else:
        c1_file = st.file_uploader("Holder CSV (from Solscan, Birdeye, or Dexscreener)", type=["csv"], key="c1_file")

    c1_max = st.slider("Max wallets to analyze", 10, MAX_WALLETS, 50, 10, key="c1_max")

    has_input = bool(c1_wallets_raw) or bool(c1_file)
    c1_btn = st.button("Run Cohort Analysis →", type="primary",
                       disabled=not (helius_key and has_input), key="c1_btn")

    if c1_btn:
        if c1_file:
            wallets = parse_wallets_from_csv(c1_file)
        else:
            wallets = c1_wallets_raw

        if not wallets:
            st.error("No valid Solana addresses found.")
            st.stop()
        if len(wallets) > c1_max:
            st.info(f"Found {len(wallets)} addresses — analyzing top {c1_max}.")
            wallets = wallets[:c1_max]

        section_label("Scanning wallets")
        prog = st.progress(0)
        status = st.empty()

        cohort_buckets = defaultdict(list)
        rows = []

        for i, wallet in enumerate(wallets):
            status.markdown(f"""
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #555;">
[{i+1}/{len(wallets)}] &nbsp;{wallet[:20]}...
</span>""", unsafe_allow_html=True)
            assets    = get_assets(wallet, HELIUS_URL)
            net_worth = wallet_usd_value(assets)
            cohort    = assign_cohort(net_worth)
            label     = cohort["name"]
            cohort_buckets[label].append({"wallet": wallet, "net_worth": net_worth, "cohort": cohort})
            rows.append({"wallet": wallet, "net_worth_usd": round(net_worth, 2), "cohort": label})
            prog.progress((i + 1) / len(wallets))
            time.sleep(0.2)

        status.empty()
        prog.empty()

        big_wallets = [r["wallet"] for r in rows if r["cohort"] in ("Whale", "Shark", "Dolphin")]
        st.session_state["whale_wallets"] = big_wallets
        if big_wallets:
            st.markdown(f"""
<div style="background: #0f1a0f; border: 1px solid #1a3a1a; border-radius: 8px; padding: 0.75rem 1rem; margin: 1rem 0; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #86efac;">
✓ &nbsp;{len(big_wallets)} smart-money wallets saved → available in Whale Overlap and Recent Buys
</div>""", unsafe_allow_html=True)

        section_label("Distribution")
        total = len(wallets)
        cols = st.columns(len(COHORT_BRACKETS))
        for col, bracket in zip(cols, COHORT_BRACKETS):
            count = len(cohort_buckets[bracket["name"]])
            col.markdown(stat_card(
                f"{bracket['emoji']} {bracket['name']}",
                str(count),
                accent=(bracket["name"] in ("Whale", "Shark"))
            ), unsafe_allow_html=True)

        section_label("Holders by cohort")
        for bracket in COHORT_BRACKETS:
            members = cohort_buckets[bracket["name"]]
            if not members:
                continue
            with st.expander(f"{bracket['emoji']} {bracket['name']}  ·  {len(members)} wallets"):
                df_out = pd.DataFrame([
                    {"Wallet": m["wallet"], "Net Worth (USD)": f"${m['net_worth']:,.2f}"}
                    for m in sorted(members, key=lambda x: -x["net_worth"])
                ])
                st.dataframe(df_out, use_container_width=True, hide_index=True)

        section_label("Export")
        csv_bytes = pd.DataFrame(rows).sort_values("net_worth_usd", ascending=False).to_csv(index=False).encode()
        st.download_button("Download results CSV", csv_bytes, "holder_cohorts.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — WHALE OVERLAP
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    page_header("Whale Overlap", "Portfolio Intelligence")
    st.markdown("""
<p style="font-family: 'Outfit', sans-serif; font-size: 0.9rem; color: #555; margin-bottom: 1.25rem; margin-top: -1rem; line-height: 1.65;">
If multiple large wallets are independently holding the same token, that's a signal worth paying attention to. 
This tool surfaces those overlaps — tokens that appear across several wallets simultaneously — 
so you can distinguish broad conviction from a single whale's position.
</p>
""", unsafe_allow_html=True)

    source = st.radio(
        "Wallet source",
        ["From Cohort Analyzer", "Paste addresses", "Upload CSV"],
        key="t2_source",
        horizontal=True,
    )

    t2_wallets = []

    if source == "From Cohort Analyzer":
        saved = st.session_state.get("whale_wallets", [])
        if saved:
            st.markdown(f"""
<div style="background: #0f1a0f; border: 1px solid #1a3a1a; border-radius: 8px; padding: 0.75rem 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #86efac;">
✓ &nbsp;{len(saved)} wallets loaded from Cohort Analysis
</div>""", unsafe_allow_html=True)
            t2_wallets = saved
            with st.expander("View wallets"):
                for w in saved:
                    st.code(w)
        else:
            st.info("Run the Cohort Analyzer first to populate this automatically.")

    elif source == "Paste addresses":
        raw = st.text_area(
            "Wallet addresses (one per line)",
            height=140,
            placeholder="7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU\n...",
            key="t2_paste",
        )
        if raw.strip():
            t2_wallets = [w.strip() for w in raw.strip().splitlines() if len(w.strip()) >= 32]
            st.caption(f"{len(t2_wallets)} addresses detected.")

    else:
        st.markdown("""
<div style="font-family: 'Outfit', sans-serif; font-size: 0.8rem; color: #555; line-height: 1.55; margin-bottom: 0.75rem;">
Export a holder list from <a href="https://solscan.io" target="_blank" style="color: #4ade80; text-decoration: none;">Solscan</a> (token page → Holders tab → Export) or Birdeye / Dexscreener and upload it below.
</div>
""", unsafe_allow_html=True)
        t2_file = st.file_uploader("Holder CSV", type=["csv"], key="t2_file")
        if t2_file:
            t2_wallets = parse_wallets_from_csv(t2_file)
            if t2_wallets:
                st.caption(f"{len(t2_wallets)} addresses found.")
            else:
                st.error("No valid Solana addresses detected.")

    t2_max = st.slider("Max wallets to scan", 5, MAX_WALLETS, 30, 5, key="t2_max")
    min_shared = st.slider("Min wallets sharing a token", 2, 10, 2, 1, key="t2_min")

    t2_btn = st.button("Run Overlap Analysis →", type="primary",
                       disabled=not (helius_key and t2_wallets), key="t2_btn")

    if t2_btn:
        wallets = t2_wallets[:t2_max]

        section_label("Scanning portfolios")
        prog2   = st.progress(0)
        status2 = st.empty()

        token_counts   = defaultdict(int)
        token_metadata = {}
        token_holders  = defaultdict(list)

        for i, wallet in enumerate(wallets):
            status2.markdown(f"""
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #555;">
[{i+1}/{len(wallets)}] &nbsp;{wallet[:20]}...
</span>""", unsafe_allow_html=True)
            assets = get_assets(wallet, HELIUS_URL)
            seen_this_wallet = set()

            for asset in assets:
                mint      = asset.get("id", "")
                interface = asset.get("interface", "")
                if interface != "FungibleToken" or mint in SKIP_TOKENS:
                    continue
                ti  = asset.get("token_info", {})
                bal = float(ti.get("balance", 0))
                if bal <= 0 or mint in seen_this_wallet:
                    continue

                seen_this_wallet.add(mint)
                token_counts[mint] += 1
                token_holders[mint].append(wallet)

                if mint not in token_metadata:
                    meta = asset.get("content", {}).get("metadata", {})
                    pi   = ti.get("price_info", {})
                    token_metadata[mint] = {
                        "symbol":    meta.get("symbol", "???"),
                        "name":      meta.get("name", "Unknown"),
                        "price_usd": float(pi.get("price_per_token", 0)),
                    }

            prog2.progress((i + 1) / len(wallets))
            time.sleep(0.2)

        status2.empty()
        prog2.empty()

        shared = {m: c for m, c in token_counts.items() if c >= min_shared}
        sorted_tokens = sorted(shared.items(), key=lambda x: -x[1])

        if not sorted_tokens:
            st.warning(f"No tokens shared by {min_shared}+ wallets.")
        else:
            section_label(f"{len(sorted_tokens)} shared tokens")

            summary_rows = []
            for mint, count in sorted_tokens[:50]:
                meta = token_metadata[mint]
                summary_rows.append({
                    "Symbol":        meta["symbol"],
                    "Name":          meta["name"],
                    "Wallets":       count,
                    "% of Group":    f"{count/len(wallets)*100:.1f}%",
                    "Price (USD)":   f"${meta['price_usd']:,.6f}" if meta["price_usd"] > 0 else "—",
                    "Mint":          mint,
                })
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

            section_label("Token detail")
            for mint, count in sorted_tokens[:30]:
                meta    = token_metadata[mint]
                holders = token_holders[mint]
                pct     = count / len(wallets) * 100
                with st.expander(f"{meta['symbol']}  ·  {count} wallets  ·  {pct:.1f}%"):
                    st.caption(f"Mint: {mint}")
                    if meta["price_usd"] > 0:
                        st.caption(f"Price: ${meta['price_usd']:,.6f}")
                    for h in holders:
                        st.code(h)

            section_label("Export")
            dl_rows = []
            for mint, count in sorted_tokens:
                meta = token_metadata[mint]
                for h in token_holders[mint]:
                    dl_rows.append({"mint": mint, "symbol": meta["symbol"],
                                    "name": meta["name"], "wallets_holding": count, "wallet": h})
            csv2 = pd.DataFrame(dl_rows).to_csv(index=False).encode()
            st.download_button("Download overlap CSV", csv2, "whale_overlap.csv", "text/csv")


# ── acquisition helpers ────────────────────────────────────────────────────────
def fetch_signatures(wallet: str, helius_url: str, limit: int = 100) -> list:
    payload = {"jsonrpc": "2.0", "id": "sigs", "method": "getSignaturesForAddress",
               "params": [wallet, {"limit": limit}]}
    try:
        r = requests.post(helius_url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json().get("result", [])
    except Exception:
        return []


def fetch_transaction(sig: str, helius_url: str):
    payload = {"jsonrpc": "2.0", "id": "tx", "method": "getTransaction",
               "params": [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]}
    try:
        r = requests.post(helius_url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json().get("result")
    except Exception:
        return None


def parse_token_inflows(tx, wallet: str, sig: str) -> list:
    inflows = []
    if not tx:
        return inflows
    meta       = tx.get("meta", {})
    block_time = tx.get("blockTime", 0)
    pre  = {e["accountIndex"]: e for e in meta.get("preTokenBalances", [])}
    post = {e["accountIndex"]: e for e in meta.get("postTokenBalances", [])}
    wallet_indices = set()
    for i, key_info in enumerate(tx.get("transaction", {}).get("message", {}).get("accountKeys", [])):
        pubkey = key_info if isinstance(key_info, str) else key_info.get("pubkey", "")
        if pubkey == wallet:
            wallet_indices.add(i)
    for idx in set(pre) | set(post):
        entry = post.get(idx) or pre.get(idx, {})
        if entry.get("owner") == wallet:
            wallet_indices.add(idx)
    for idx in wallet_indices:
        pre_entry  = pre.get(idx, {})
        post_entry = post.get(idx, {})
        pre_amt    = float((pre_entry.get("uiTokenAmount") or {}).get("uiAmount") or 0)
        post_amt   = float((post_entry.get("uiTokenAmount") or {}).get("uiAmount") or 0)
        if post_amt > pre_amt:
            mint = post_entry.get("mint") or pre_entry.get("mint", "unknown")
            if mint in SKIP_TOKENS:
                continue
            inflows.append({
                "mint":            mint,
                "amount_received": round(post_amt - pre_amt, 6),
                "timestamp":       block_time,
                "date":            datetime.fromtimestamp(block_time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                "tx_sig":          sig,
            })
    return inflows


def scan_wallet_acquisitions(wallet: str, helius_url: str, cutoff_ts: int) -> list:
    acquisitions = []
    sigs = fetch_signatures(wallet, helius_url, limit=100)
    for sig_info in sigs:
        if sig_info.get("blockTime", 0) < cutoff_ts:
            break
        tx    = fetch_transaction(sig_info["signature"], helius_url)
        found = parse_token_inflows(tx, wallet, sig_info["signature"])
        acquisitions.extend(found)
        time.sleep(0.1)
    return acquisitions


def enrich_token_metadata(mints: list, helius_url: str) -> dict:
    meta = {}
    for i in range(0, len(mints), 100):
        batch = mints[i:i+100]
        try:
            r = requests.post(helius_url, json={
                "jsonrpc": "2.0", "id": "batch-meta",
                "method": "getAssetBatch",
                "params": {"ids": batch},
            }, timeout=30)
            for asset in r.json().get("result", []):
                mint = asset.get("id", "")
                if mint:
                    m = asset.get("content", {}).get("metadata", {})
                    meta[mint] = {"symbol": m.get("symbol", mint[:8]), "name": m.get("name", "Unknown")}
        except Exception:
            pass
    return meta


def render_acquisition_results(all_acq, token_wallets, token_meta, total_wallets, min_shared, days, filename):
    summary = []
    for mint, buying_wallets in token_wallets.items():
        meta   = token_meta.get(mint, {"symbol": mint[:8], "name": ""})
        events = [a for a in all_acq if a["mint"] == mint]
        summary.append({
            "mint": mint, "symbol": meta["symbol"], "name": meta["name"],
            "wallets_bought": len(buying_wallets),
            "total_received": round(sum(e["amount_received"] for e in events), 4),
            "last_seen": max(e["date"] for e in events),
            "coordinated": len(buying_wallets) >= min_shared,
        })
    summary.sort(key=lambda x: (-x["wallets_bought"], x["last_seen"]))

    coordinated = [s for s in summary if s["coordinated"]]
    if coordinated:
        section_label(f"Coordination signals — {min_shared}+ wallets buying")
        st.markdown("""
<div style="background: #0f1a0f; border: 1px solid #1a3a1a; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #86efac;">
These tokens were independently acquired by multiple wallets in your window — potential coordination signal.
</div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([{
            "Symbol": s["symbol"], "Name": s["name"],
            "Wallets": s["wallets_bought"], "Total Received": s["total_received"],
            "Last Buy": s["last_seen"], "Mint": s["mint"],
        } for s in coordinated]), use_container_width=True, hide_index=True)

        for s in coordinated:
            with st.expander(f"{s['symbol']}  ·  {s['wallets_bought']} wallets  ·  {s['name']}"):
                st.caption(f"Mint: {s['mint']}")
                events = sorted([a for a in all_acq if a["mint"] == s["mint"]],
                                key=lambda x: x["timestamp"], reverse=True)
                for ev in events:
                    st.markdown(f"`{ev['wallet'][:16]}...`  +{ev['amount_received']:,.2f}  ·  {ev['date']}")
    else:
        st.info(f"No tokens bought by {min_shared}+ wallets. Try lowering the threshold or extending the lookback.")

    section_label(f"All buys — {len(all_acq)} acquisitions")
    buys_rows = []
    for acq in sorted(all_acq, key=lambda x: x["timestamp"], reverse=True):
        meta = token_meta.get(acq["mint"], {"symbol": acq["mint"][:8], "name": ""})
        buys_rows.append({
            "Date": acq["date"], "Wallet": acq["wallet"],
            "Symbol": meta["symbol"], "Amount": acq["amount_received"],
            "Wallets (total)": len(token_wallets[acq["mint"]]),
            "Signal": "✓" if len(token_wallets[acq["mint"]]) >= min_shared else "",
            "Mint": acq["mint"],
        })
    st.dataframe(pd.DataFrame(buys_rows), use_container_width=True, hide_index=True)

    section_label("Export")
    dl_rows = []
    for acq in all_acq:
        meta = token_meta.get(acq["mint"], {"symbol": "", "name": ""})
        dl_rows.append({
            "wallet": acq["wallet"], "mint": acq["mint"],
            "symbol": meta["symbol"], "amount_received": acq["amount_received"],
            "date": acq["date"], "tx_sig": acq["tx_sig"],
            "wallets_bought": len(token_wallets[acq["mint"]]),
            "coordinated": len(token_wallets[acq["mint"]]) >= min_shared,
        })
    csv_out = pd.DataFrame(dl_rows).sort_values(
        ["coordinated", "wallets_bought"], ascending=[False, False]
    ).to_csv(index=False).encode()
    st.download_button("Download CSV", csv_out, filename, "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — RECENT BUYS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    page_header("Recent Buys", "Acquisition Scanner")
    st.markdown("""
<p style="font-family: 'Outfit', sans-serif; font-size: 0.9rem; color: #555; margin-bottom: 1.25rem; margin-top: -1rem; line-height: 1.65;">
Holdings tell you where wallets are — transaction history tells you where they're going. 
This tab scans recent buys so you can see what tokens smart-money wallets have actually been 
accumulating, and flag any tokens that multiple wallets bought independently in the same window.
</p>
""", unsafe_allow_html=True)

    t3_source = st.radio(
        "Wallet source",
        ["From Cohort Analyzer", "Paste addresses", "Upload CSV"],
        key="t3_source",
        horizontal=True,
    )

    t3_wallets = []

    if t3_source == "From Cohort Analyzer":
        saved3 = st.session_state.get("whale_wallets", [])
        if saved3:
            st.markdown(f"""
<div style="background: #0f1a0f; border: 1px solid #1a3a1a; border-radius: 8px; padding: 0.75rem 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #86efac;">
✓ &nbsp;{len(saved3)} wallets loaded from Cohort Analysis
</div>""", unsafe_allow_html=True)
            t3_wallets = saved3
        else:
            st.info("Run the Cohort Analyzer first to populate this automatically.")
    elif t3_source == "Paste addresses":
        raw3 = st.text_area(
            "Wallet addresses (one per line)",
            height=140,
            placeholder="7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU\n...",
            key="t3_paste",
        )
        if raw3.strip():
            t3_wallets = [w.strip() for w in raw3.strip().splitlines() if len(w.strip()) >= 32]
            st.caption(f"{len(t3_wallets)} addresses detected.")
    else:
        st.markdown("""
<div style="font-family: 'Outfit', sans-serif; font-size: 0.8rem; color: #555; line-height: 1.55; margin-bottom: 0.75rem;">
Export a holder list from <a href="https://solscan.io" target="_blank" style="color: #4ade80; text-decoration: none;">Solscan</a> (token page → Holders tab → Export) or Birdeye / Dexscreener and upload it below.
</div>
""", unsafe_allow_html=True)
        t3_file = st.file_uploader("Holder CSV", type=["csv"], key="t3_file")
        if t3_file:
            t3_wallets = parse_wallets_from_csv(t3_file)
            if t3_wallets:
                st.caption(f"{len(t3_wallets)} addresses found.")
            else:
                st.error("No valid Solana addresses detected.")

    col_a, col_b = st.columns(2)
    with col_a:
        t3_days = st.slider("Lookback (days)", 1, 30, 7, 1, key="t3_days")
    with col_b:
        t3_max = st.slider("Max wallets", 5, 50, 20, 5, key="t3_max")

    t3_min_shared = st.slider("Flag when bought by N+ wallets", 2, 10, 2, 1, key="t3_min_shared")

    t3_btn = st.button("Run Acquisition Scan →", type="primary",
                       disabled=not (helius_key and t3_wallets), key="t3_btn")

    if t3_btn:
        wallets3  = t3_wallets[:t3_max]
        cutoff_ts = int((datetime.now(timezone.utc) - timedelta(days=t3_days)).timestamp())
        cutoff_str = datetime.fromtimestamp(cutoff_ts, tz=timezone.utc).strftime("%Y-%m-%d")

        section_label(f"Scanning {len(wallets3)} wallets since {cutoff_str}")
        st.caption("Reads raw transactions — approximately 2–5s per wallet.")

        prog3   = st.progress(0)
        status3 = st.empty()
        all_acq3       = []
        token_wallets3 = defaultdict(set)
        token_meta3    = {}

        for i, wallet in enumerate(wallets3):
            status3.markdown(f"""
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #555;">
[{i+1}/{len(wallets3)}] &nbsp;{wallet[:20]}...
</span>""", unsafe_allow_html=True)
            acqs = scan_wallet_acquisitions(wallet, HELIUS_URL, cutoff_ts)
            for acq in acqs:
                mint = acq["mint"]
                token_wallets3[mint].add(wallet)
                acq["wallet"] = wallet
                all_acq3.append(acq)
                if mint not in token_meta3:
                    token_meta3[mint] = {"symbol": mint[:8], "name": ""}
            prog3.progress((i + 1) / len(wallets3))

        status3.empty()
        prog3.empty()

        if not all_acq3:
            st.warning(f"No token inflows found in the last {t3_days} days.")
        else:
            unknown3 = [m for m in token_meta3 if token_meta3[m]["name"] == ""]
            token_meta3.update(enrich_token_metadata(unknown3, HELIUS_URL))
            render_acquisition_results(all_acq3, token_wallets3, token_meta3,
                                       len(wallets3), t3_min_shared, t3_days,
                                       f"whale_acquisitions_{t3_days}d.csv")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — WATCHLIST
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    page_header("Watchlist", "Preset Wallet Scanner")
    st.markdown("""
<p style="font-family: 'Outfit', sans-serif; font-size: 0.9rem; color: #555; margin-bottom: 1.25rem; margin-top: -1rem; line-height: 1.65;">
Your curated list of wallets worth tracking — known traders, influencers, or wallets you've identified 
as consistently early. This runs the same acquisition scan as Recent Buys but against your preset list, 
so you can check in on what they've been accumulating without rebuilding the list each time.
</p>
""", unsafe_allow_html=True)

    if PRESET_WALLETS:
        st.markdown(f"""
<div style="background: #0f1a0f; border: 1px solid #1a3a1a; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #86efac;">
{len(PRESET_WALLETS)} wallets in watchlist &nbsp;·&nbsp; edit PRESET_WALLETS in app.py to modify
</div>""", unsafe_allow_html=True)
        with st.expander("View preset wallets"):
            for w in PRESET_WALLETS:
                st.code(w)
    else:
        st.warning("Watchlist is empty. Add addresses to PRESET_WALLETS in app.py.")
        st.stop()

    col_a4, col_b4 = st.columns(2)
    with col_a4:
        t4_days = st.slider("Lookback (days)", 1, 30, 7, 1, key="t4_days")
    with col_b4:
        t4_min_shared = st.slider("Flag when bought by N+ wallets", 2, 10, 2, 1, key="t4_min_shared")

    t4_btn = st.button("Scan Watchlist →", type="primary", disabled=not helius_key, key="t4_btn")

    if t4_btn:
        cutoff_ts  = int((datetime.now(timezone.utc) - timedelta(days=t4_days)).timestamp())
        cutoff_str = datetime.fromtimestamp(cutoff_ts, tz=timezone.utc).strftime("%Y-%m-%d")

        section_label(f"Scanning {len(PRESET_WALLETS)} wallets since {cutoff_str}")
        st.caption("Reads raw transactions — approximately 2–5s per wallet.")

        prog4   = st.progress(0)
        status4 = st.empty()
        all_acq4       = []
        token_wallets4 = defaultdict(set)
        token_meta4    = {}

        for i, wallet in enumerate(PRESET_WALLETS):
            status4.markdown(f"""
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #555;">
[{i+1}/{len(PRESET_WALLETS)}] &nbsp;{wallet[:20]}...
</span>""", unsafe_allow_html=True)
            acqs = scan_wallet_acquisitions(wallet, HELIUS_URL, cutoff_ts)
            for acq in acqs:
                mint = acq["mint"]
                token_wallets4[mint].add(wallet)
                acq["wallet"] = wallet
                all_acq4.append(acq)
                if mint not in token_meta4:
                    token_meta4[mint] = {"symbol": mint[:8], "name": ""}
            prog4.progress((i + 1) / len(PRESET_WALLETS))

        status4.empty()
        prog4.empty()

        if not all_acq4:
            st.warning(f"No token inflows found in the last {t4_days} days.")
        else:
            unknown4 = [m for m in token_meta4 if token_meta4[m]["name"] == ""]
            token_meta4.update(enrich_token_metadata(unknown4, HELIUS_URL))
            render_acquisition_results(all_acq4, token_wallets4, token_meta4,
                                       len(PRESET_WALLETS), t4_min_shared, t4_days,
                                       f"watchlist_acquisitions_{t4_days}d.csv")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — COMMON HOLDERS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    page_header("Common Holders", "Cross-Token Analysis")
    st.markdown("""
<p style="font-family: 'Outfit', sans-serif; font-size: 0.9rem; color: #555; margin-bottom: 1.25rem; margin-top: -1rem; line-height: 1.65;">
Which wallets are positioned in both Token A and Token B? Community overlap is useful for finding 
migration patterns, coordinated plays, or just understanding how much your holder base overlaps with 
another project's community. Upload holder exports for two tokens and see exactly who's in both.
</p>
<div style="font-family: 'Outfit', sans-serif; font-size: 0.8rem; color: #555; line-height: 1.6; margin-bottom: 1rem; padding: 0.75rem 1rem; background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 8px;">
    To get a holder CSV: go to any token page on <a href="https://solscan.io" target="_blank" style="color: #4ade80; text-decoration: none;">Solscan</a> → click the <strong style="color: #888;">Holders</strong> tab → click <strong style="color: #888;">Export</strong>. Do this for both tokens, then upload each file below. The address column is detected automatically.
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("Token A holders", type="csv", key="ch_file1")
    with col2:
        file2 = st.file_uploader("Token B holders", type="csv", key="ch_file2")

    if file1 and file2:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        col1_name = detect_holder_address_col(df1)
        col2_name = detect_holder_address_col(df2)

        if not col1_name or not col2_name:
            st.error("Could not detect a wallet address column in one or both files.")
        else:
            st.caption(f"Token A column: {col1_name}  ·  Token B column: {col2_name}")

            addrs1 = set(df1[col1_name].dropna().astype(str).str.strip())
            addrs2 = set(df2[col2_name].dropna().astype(str).str.strip())
            common = addrs1 & addrs2

            section_label("Results")
            cols = st.columns(3)
            cols[0].markdown(stat_card("Token A holders", f"{len(addrs1):,}"), unsafe_allow_html=True)
            cols[1].markdown(stat_card("Token B holders", f"{len(addrs2):,}"), unsafe_allow_html=True)
            cols[2].markdown(stat_card("Common holders", f"{len(common):,}", accent=True), unsafe_allow_html=True)

            st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
            common_df = pd.DataFrame(sorted(common), columns=["Wallet Address"])
            st.dataframe(common_df, use_container_width=True, hide_index=True)

            section_label("Export")
            st.download_button(
                "Download common holders CSV",
                common_df.to_csv(index=False).encode(),
                "common_holders.csv",
                "text/csv",
            )
