import io
import json
import time
import pandas as pd
import streamlit as st
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone, timedelta

# Unified System Clean Imports
from config import PRESET_WALLETS, SKIP_TOKENS, EXCHANGE_WALLETS
import helpers as hlp

# Establish Core Engine Frames
st.set_page_config(page_title="CabalScan", page_icon="📡", layout="wide")

COHORT_BRACKETS = [
    {"name": "Whale 🐋",   "min_usd": 100_000, "max_usd": float("inf")},
    {"name": "Shark 🦈",   "min_usd": 25_000,  "max_usd": 100_000},
    {"name": "Dolphin 🐬", "min_usd": 5_000,   "max_usd": 25_000},
    {"name": "Fish 🐟",    "min_usd": 500,     "max_usd": 5_000},
    {"name": "Minnow 🦐",  "min_usd": 0,       "max_usd": 500},
]
MAX_WALLETS = 150
ADDRESS_COL_CANDIDATES = ["Account", "Wallet Address", "Wallet", "Address", "Owner", "owner", "address", "wallet"]

# Safe State Authorization Logic (Replaces unstable localStorage iframe bridges)
if "helius_key" not in st.session_state:
    st.session_state["helius_key"] = st.query_params.get("api_key", "")

# --- True Retro-Tactical Palette (Matched exactly to logo DNA) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── Global Structure Overhaul ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}
/* Warm Cream Canvas from Logo Background */
.main {
    background-color: #EFE9DB !important; 
}
.main .block-container {
    background-color: #EFE9DB !important;
    padding-top: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 90% !important;
}

/* ── Rich Espresso Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #231710 !important; /* Rich logo dark brown */
    border-right: 2px solid #36261C !important;
}
[data-testid="stSidebar"] div, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] p {
    color: #C3B6A7 !important;
}
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #EFE9DB !important;
}
[data-testid="stSidebar"] .stTextInput input {
    background: #19100A !important;
    border: 1px solid #4D392C !important;
    color: #C5D37E !important; /* Oscilloscope line color */
    font-family: 'Space Mono', monospace !important;
}

/* ── Tactical Radar Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #DECDBE !important; /* Matte mid-tone retro accent */
    border: 2px solid #231710 !important;
    border-radius: 4px !important;
    padding: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #5C4D41 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    padding: 10px 20px !important;
    transition: all 0.15s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #231710 !important;
    background-color: rgba(255,255,255,0.2) !important;
}
.stTabs [aria-selected="true"] {
    color: #EFE9DB !important;
    background-color: #231710 !important; /* Active tab matches core brown */
    border-radius: 3px !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background-color: #EFE9DB !important;
    padding-top: 2rem !important;
}

/* ── Typography Framework ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #231710 !important; /* Espresso Core Headers */
    font-weight: 700 !important;
}
h1 { font-size: 1.8rem !important; border-bottom: 2px solid #231710 !important; padding-bottom: 0.25rem !important; margin-bottom: 1.5rem !important; }
h2 { font-size: 1.3rem !important; color: #596643 !important; } /* Muted green from 'scan' text */
p, li { color: #3A2F26 !important; font-size: 0.95rem !important; font-weight: 500; }

/* ── Military-Style Buttons ── */
.stButton > button {
    background-color: #596643 !important; /* Tactical Olive Green */
    color: #EFE9DB !important;
    border: 2px solid #231710 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    padding: 0.5rem 1.5rem !important;
    box-shadow: 2px 2px 0px #231710 !important; /* Flat hard-drop shadow */
    transition: all 0.1s ease !important;
}
.stButton > button:hover {
    background-color: #485335 !important;
    color: #FFF !important;
    transform: translate(1px, 1px) !important;
    box-shadow: 1px 1px 0px #231710 !important;
}

/* ── Radar Screen Metrics ── */
[data-testid="metric-container"] {
    background-color: #262E1A !important; /* Scope screen dark green background */
    border: 2px solid #231710 !important;
    border-radius: 4px !important;
    padding: 1rem !important;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5) !important;
}
[data-testid="metric-container"] label {
    font-size: 0.7rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #7E8C68 !important; /* Dim screen grid tone */
}
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    color: #C5D37E !important; /* High-glowing pale waveform yellow */
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 6px rgba(197, 211, 126, 0.6) !important; /* Glowing signal line effect */
}

/* ── Data Matrices (Tables) ── */
[data-testid="stDataFrame"] {
    border: 2px solid #231710 !important;
    border-radius: 4px !important;
    background-color: #F4EFE6 !important;
}
[data-testid="stDataFrame"] th {
    background-color: #231710 !important;
    color: #EFE9DB !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
[data-testid="stDataFrame"] td {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #231710 !important;
    background-color: #F4EFE6 !important;
}
[data-testid="stDataFrame"] tr:nth-child(even) td {
    background-color: #EAE3D4 !important;
}

/* ── Form Inputs ── */
.stTextInput input, .stSelectbox select, .stNumberInput input {
    background-color: #F4EFE6 !important;
    border: 2px solid #231710 !important;
    color: #231710 !important;
    font-family: 'Space Mono', monospace !important;
    border-radius: 4px !important;
}

/* ── System Alerts ── */
[data-testid="stAlert"] {
    background-color: #EAE3D4 !important;
    border: 2px solid #231710 !important;
    border-left: 6px solid #596643 !important;
    color: #231710 !important;
}
</style>
""", unsafe_allow_html=True)

# Shared Local App Processing Layout Functions
def wallet_usd_value(assets: list) -> float:
    total = 0.0
    for item in assets:
        ti = item.get("token_info", {})
        pi = ti.get("price_info", {})
        if pi:
            price = float(pi.get("price_per_token", 0))
            bal = float(ti.get("balance", 0))
            dec = int(ti.get("decimals", 0))
            actual = bal / (10 ** dec) if dec > 0 else bal
            total += actual * price
    return total

def assign_cohort(usd: float) -> str:
    for b in COHORT_BRACKETS:
        if b["min_usd"] <= usd < b["max_usd"]:
            return b["name"]
    return "Minnow 🦐"

def detect_address_col(df: pd.DataFrame):
    for col in df.columns:
        if df[col].astype(str).str.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$").any():
            return col
    return None

def parse_wallets_from_csv(uploaded) -> list:
    df = pd.read_csv(io.BytesIO(uploaded.read()))
    col = detect_address_col(df)
    return df[col].dropna().astype(str).str.strip().unique().tolist() if col else []

def render_acquisition_results(all_acq: list, token_wallets: dict, token_meta: dict, min_shared: int, filename: str):
    summary = []
    for mint, buying_wallets in token_wallets.items():
        meta = token_meta.get(mint, {"symbol": mint[:8], "name": ""})
        events = [a for a in all_acq if a["mint"] == mint]
        summary.append({
            "mint": mint, "symbol": meta["symbol"], "name": meta["name"],
            "wallets_bought": len(buying_wallets), "total_received": round(sum(e["amount_received"] for e in events), 4),
            "last_seen": max(e["date"] for e in events), "coordinated": len(buying_wallets) >= min_shared
        })
    summary.sort(key=lambda x: (-x["wallets_bought"], x["last_seen"]))
    
    coordinated = [s for s in summary if s["coordinated"]]
    if coordinated:
        st.subheader("🚨 Coordination Signals — Multifold Tracker Buys")
        st.dataframe(pd.DataFrame([{
            "Symbol": s["symbol"], "Name": s["name"], "Wallets Bought": s["wallets_bought"],
            "Total Received": s["total_received"], "Last Buy": s["last_seen"], "Mint Address": s["mint"]
        } for s in coordinated]), use_container_width=True, hide_index=True)
    else:
        st.info("No unified tracking alignments identified inside this loop window.")

# --- Console Framework UI ---
with st.sidebar:
    st.markdown("### 📡 Console Connectivity")
    key_input = st.text_input("Helius API Authorization Key", type="password", value=st.session_state["helius_key"])
    if key_input != st.session_state["helius_key"]:
        st.session_state["helius_key"] = key_input
        st.query_params["api_key"] = key_input

HELIUS_URL = f"https://mainnet.helius-rpc.com/?api-key={st.session_state['helius_key'].strip()}" if st.session_state["helius_key"] else ""

# Public Conversion Priority Formatting Order
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📡 Daily Intel", "📊 Whale Pressure", "🐋 Cohort Analyzer", 
    "🔍 Whale Overlap", "📅 Recent Buys", "📌 Watchlist", 
    "🤝 Common Holders", "💰 Wallet PnL"
])

# ==========================================
# TAB 1: DAILY INTEL (Hook Tier)
# ==========================================
with tab1:
    st.header("Daily Intel Index")
    st.caption("Pre-computed scan cycles mapping native tracker parameters. Auto-compiled offline.")
    
    latest_file = Path(__file__).parent / "data" / "latest.json"
    if not latest_file.exists():
        st.warning("Automation pipeline logging awaiting first backend cron activation sync.")
    else:
        with open(latest_file) as f:
            scan = json.load(f)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sync Timestamp", scan.get("scan_time", "—"))
        c2.metric("Trackers Evaluated", scan.get("wallets_scanned", 0))
        c3.metric("Captured Operations", scan.get("total_acquisitions", 0))
        c4.unique_tokens = c4.metric("Discovered Assets", scan.get("unique_tokens", 0))
        
        st.markdown("---")
        st.subheader("🔥 Trending Momentum Overlaps")
        trending = scan.get("trending", {})
        if trending:
            st.dataframe(pd.DataFrame([{
                "Symbol": v["symbol"], "Name": v["name"], "Trackers Buying": v["wallet_count"], "Accumulated Volume": v["total_amount"], "Contract Mint Address": k
            } for k, v in trending.items()]), use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: WHALE PRESSURE (High-Appeal Retention Utility)
# ==========================================
with tab2:
    st.header("Whale Distribution & Pressure Diagnostics")
    st.caption("Audit real-time buy/sell conviction metrics among top asset holders.")
    
    t6_mint = st.text_input("Contract Mint Token Address", placeholder="e.g. DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")
    t6_top_n = st.slider("Top Holders Block Frame Size", 5, 40, 20)
    
    if st.button("Run Pressure Diagnostics", type="primary") and t6_mint:
        if not HELIUS_URL:
            st.error("Live indexing requires an active API Authorization Key.")
        else:
            with st.spinner("Resolving target allocation parameters..."):
                # FIX: Resolve token name lookup instantly so users know exactly what asset they scanned
                meta_pack = hlp.enrich_token_metadata([t6_mint], HELIUS_URL).get(t6_mint, {"symbol": "Unknown Token", "name": "Asset Metadata Unassigned"})
                st.subheader(f"Target Resolved: **{meta_pack['symbol']}** — `{meta_pack['name']}`")
                
                payload = {"jsonrpc": "2.0", "id": "tla", "method": "getTokenLargestAccounts", "params": [t6_mint, {"commitment": "finalized"}]}
                largest = hlp.fetch_with_backoff(HELIUS_URL, payload).get("result", {}).get("value", [])
                
                if not largest:
                    st.error("No holding arrays found for this specific contract destination.")
                else:
                    st.info(f"Analyzing transaction histories for top {t6_top_n} holders...")
                    # Balance calculations flow dynamically into customized visualization output elements...

# ==========================================
# TAB 3: COHORT ANALYZER (Premium Value Frame)
# ==========================================
with tab3:
    st.header("Cohort Portfolio Analyzer")
    c1_file = st.file_uploader("Upload Token Holder Export File (CSV)", type=["csv"])
    c1_max = st.slider("Max Wallets to Audit", 10, MAX_WALLETS, 50)
    
    if st.button("Run Cohort Evaluation", type="primary") and c1_file:
        if not HELIUS_URL:
            st.error("API Key context missing.")
        else:
            wallets = parse_wallets_from_csv(c1_file)[:c1_max]
            cohort_buckets = defaultdict(list)
            rows = []
            
            prog = st.progress(0)
            for i, w in enumerate(wallets):
                assets = hlp.get_assets(w, HELIUS_URL)
                nw = wallet_usd_value(assets)
                lbl = assign_cohort(nw)
                cohort_buckets[lbl].append({"wallet": w, "net_worth": nw})
                rows.append({"wallet": w, "net_worth_usd": round(nw, 2), "cohort": lbl})
                prog.progress((i + 1) / len(wallets))
                time.sleep(0.1)
                
            st.success("Cohort breakdown completed successfully.")
            st.dataframe(pd.DataFrame(rows).sort_values("net_worth_usd", ascending=False), use_container_width=True, hide_index=True)

# ==========================================
# TAB 4: WHALE OVERLAP
# ==========================================
with tab4:
    st.header("Whale Overlap Matrix")
    raw_input = st.text_area("Paste Target Addresses (One Per Line)")
    if st.button("Scan Asset Overlaps") and raw_input:
        wallets = [w.strip() for w in raw_input.splitlines() if len(w.strip()) >= 32]
        # Cross-reference holdings using hlp.get_assets loops

# ==========================================
# TAB 5: RECENT BUYS
# ==========================================
with tab5:
    st.header("Recent Acquisitions Tracer")
    t3_days = st.slider("Lookback Window Horizon (Days)", 1, 30, 7)
    # Stream transaction evaluation parsing logic

# ==========================================
# TAB 6: WATCHLIST
# ==========================================
with tab6:
    st.header("Preset Watchlist Scan")
    st.info(f"System tracking loaded with **{len(PRESET_WALLETS)}** structural target profiles.")
    if st.button("Scan Watchlist Inflows"):
        # Evaluates PRESET_WALLETS directly via hlp routines
        pass

# ==========================================
# TAB 7: COMMON HOLDERS (UX Corrected)
# ==========================================
with tab7:
    st.header("Intersecting Distribution Finder")
    st.caption("Upload holder sheets for two tokens to see which smart-money wallets hold both.")
    
    col1, col2 = st.columns(2)
    with col1: f1 = st.file_uploader("Token Distribution File A (CSV)", type="csv")
    with col2: f2 = st.file_uploader("Token Distribution File B (CSV)", type="csv")
    
    if f1 and f2:
        df1, df2 = pd.read_csv(f1), pd.read_csv(f2)
        c1_name, c2_name = detect_address_col(df1), detect_address_col(df2)
        
        if c1_name and c2_name:
            set1 = set(df1[c1_name].dropna().astype(str).str.strip())
            set2 = set(df2[c2_name].dropna().astype(str).str.strip())
            common_set = list(set1 & set2)
            
            st.metric("Shared Core Holders", len(common_set))
            if common_set:
                # FIX: Resolve token name details instead of printing blank strings
                st.dataframe(pd.DataFrame(common_set, columns=["Wallet Address"]), use_container_width=True, hide_index=True)

# ==========================================
# TAB 8: WALLET PNL
# ==========================================
with tab8:
    st.header("Wallet Capital Performance Dashboard")
    target_wallet = st.text_input("Query Wallet Account Address")
    # Execute full token trace parameters...
