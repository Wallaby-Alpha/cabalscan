import io
import json
import time
import pandas as pd
import streamlit as st
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone, timedelta

# ── 1. GLOBAL SYSTEM CONFIGURATION CONSTANTS (Declared first for Scoping) ──
MAX_WALLETS = 150
ADDRESS_COL_CANDIDATES = ["Account", "Wallet Address", "Wallet", "Address", "Owner", "owner", "address", "wallet"]

COHORT_BRACKETS = [
    {"name": "Whale 🐋",   "min_usd": 100_000, "max_usd": float("inf")},
    {"name": "Shark 🦈",   "min_usd": 25_000,  "max_usd": 100_000},
    {"name": "Dolphin 🐬", "min_usd": 5_000,   "max_usd": 25_000},
    {"name": "Fish 🐟",    "min_usd": 500,     "max_usd": 5_000},
    {"name": "Minnow 🦐",  "min_usd": 0,       "max_usd": 500},
]

# ── 2. SHARED UNIFIED FILE IMPORTS ──
from config import PRESET_WALLETS, SKIP_TOKENS, EXCHANGE_WALLETS
import helpers as hlp

# Establish Streamlit Canvas Window Frame
st.set_page_config(page_title="CabalScan", page_icon="📡", layout="wide")

# ── 3. CUSTOM RETRO-TACTICAL CSS THEME SHEET ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* Core Dark Architecture */
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; }
.main { background-color: #0F0E0C !important; }
.main .block-container {
    background-color: #0F0E0C !important;
    padding-top: 1.5rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    max-width: 95% !important;
}

/* Sidebar Custom Radio Upgrades */
[data-testid="stSidebar"] { background-color: #161411 !important; border-right: 1px solid #2A2520 !important; }
[data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p { color: #A39689 !important; }

[data-testid="stSidebar"] .stRadio label {
    background-color: #1F1C18 !important;
    border: 1px solid #2A2520 !important;
    color: #C3B6A7 !important;
    padding: 10px 14px !important;
    border-radius: 4px !important;
    margin-bottom: 6px !important;
    display: block;
    cursor: pointer;
    transition: all 0.2s ease;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    border-color: #7E8C68 !important;
    color: #EFE9DB !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] [data-checked="true"] label {
    background-color: #2D3322 !important;
    border-color: #7E8C68 !important;
    color: #C5D37E !important;
    font-weight: 600;
}

/* Hero Panel Typography */
.hero-title { font-size: 2.85rem !important; font-weight: 700 !important; line-height: 1.1; letter-spacing: -0.03em !important; color: #EFE9DB !important; margin-bottom: 0.5rem; }
.hero-highlight { color: #C5D37E !important; text-shadow: 0 0 12px rgba(197, 211, 126, 0.2); }
.hero-subtitle { font-size: 1.05rem; color: #8C8073; margin-bottom: 2rem; }

/* Dashboard Component Enclosures */
[data-testid="metric-container"] { background-color: #161411 !important; border: 1px solid #2A2520 !important; border-radius: 6px !important; padding: 1.25rem !important; }
[data-testid="metric-container"] label { font-size: 0.72rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; color: #8C8073 !important; }
[data-testid="stMetricValue"] { font-family: 'Space Mono', monospace !important; color: #C5D37E !important; font-size: 1.85rem !important; }

[data-testid="stDataFrame"] { border: 1px solid #2A2520 !important; border-radius: 6px !important; background-color: #161411 !important; }
[data-testid="stDataFrame"] th { background-color: #1F1C18 !important; color: #EFE9DB !important; font-size: 0.75rem !important; }
[data-testid="stDataFrame"] td { font-family: 'Space Mono', monospace !important; color: #C3B6A7 !important; background-color: #161411 !important; }
[data-testid="stDataFrame"] tr:nth-child(even) td { background-color: #110F0D !important; }

.stButton > button {
    background-color: #596643 !important;
    color: #EFE9DB !important;
    border: 1px solid #2A2520 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em;
    border-radius: 4px !important;
    padding: 0.6rem 1.75rem !important;
    transition: all 0.2s;
}
.stButton > button:hover { background-color: #6C7C52 !important; color: #FFF !important; box-shadow: 0 0 15px rgba(197, 211, 126, 0.2) !important; }
</style>
""", unsafe_allow_html=True)

# ── 4. BACKEND CONTEXT PROCESSING HELPERS ──
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

# Safe State Authorization Logic
if "helius_key" not in st.session_state:
    st.session_state["helius_key"] = st.query_params.get("api_key", "")

# ── 5. UNIFIED TERMINAL SIDEBAR ──
with st.sidebar:
    st.image("logo for cabal scan.png", use_container_width=True)
    st.markdown("<hr style='border-color: #2A2520; margin: 1rem 0;'>", unsafe_allow_html=True)
    
    st.markdown("### 🖥️ Operation Terminal")
    nav_select = st.radio(
        "Select Operation Unit",
        ["📡 Daily Intel", "📊 Whale Pressure", "🐋 Cohort Analyzer", "🔍 Whale Overlap", "📅 Recent Buys", "📌 Watchlist", "🤝 Common Holders", "💰 Wallet PnL"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='border-color: #2A2520; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    key_input = st.text_input("Helius Connection Key", type="password", value=st.session_state["helius_key"])
    if key_input != st.session_state["helius_key"]:
        st.session_state["helius_key"] = key_input
        st.query_params["api_key"] = key_input

HELIUS_URL = f"https://mainnet.helius-rpc.com/?api-key={st.session_state['helius_key'].strip()}" if st.session_state["helius_key"] else ""

# ── 6. PRIMARY MAIN-STAGE CONTROL ROUTING ──
if nav_select == "📡 Daily Intel":
    st.markdown("""
        <p style="font-size: 0.75rem; letter-spacing: 0.15em; color: #7E8C68; font-weight: 700; text-transform: uppercase; margin-bottom: 0px;">BUILT IN DAEMON</p>
        <h1 class="hero-title">Trace the wallets<br>behind the <span class="hero-highlight">cabal</span></h1>
        <p class="hero-subtitle">Automated background network scans monitoring on-chain movements. Real-time alpha compiled without frontend friction.</p>
    """, unsafe_allow_html=True)
    
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
        c4.metric("Discovered Assets", scan.get("unique_tokens", 0))
        
        st.markdown("<br><h3 style='color: #EFE9DB;'>🔥 Trending Momentum Overlaps</h3>", unsafe_allow_html=True)
        trending = scan.get("trending", {})
        if trending:
            st.dataframe(pd.DataFrame([{
                "Symbol": v["symbol"], "Name": v["name"], "Trackers Buying": v["wallet_count"], "Accumulated Volume": v["total_amount"], "Contract Mint Address": k
            } for k, v in trending.items()]), use_container_width=True, hide_index=True)

elif nav_select == "📊 Whale Pressure":
    st.markdown('<h1 style="color: #EFE9DB; font-size: 2rem; margin-bottom:0.5rem;">Whale Distribution & Pressure Diagnostics</h1>', unsafe_allow_html=True)
    st.caption("Audit real-time buy/sell conviction metrics among top asset holders.")
    
    t6_mint = st.text_input("Contract Mint Token Address", placeholder="e.g. DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")
    t6_top_n = st.slider("Top Holders Block Frame Size", 5, 40, 20)
    
    if st.button("Run Pressure Diagnostics", type="primary") and t6_mint:
        if not HELIUS_URL:
            st.error("Live indexing requires an active API Authorization Key.")
        else:
            with st.spinner("Resolving target allocation parameters..."):
                meta_pack = hlp.enrich_token_metadata([t6_mint], HELIUS_URL).get(t6_mint, {"symbol": "Unknown Token", "name": "Asset Metadata Unassigned"})
                st.subheader(f"Target Resolved: **{meta_pack['symbol']}** — `{meta_pack['name']}`")
                
                payload = {"jsonrpc": "2.0", "id": "tla", "method": "getTokenLargestAccounts", "params": [t6_mint, {"commitment": "finalized"}]}
                largest = hlp.fetch_with_backoff(HELIUS_URL, payload).get("result", {}).get("value", [])
                
                if not largest:
                    st.error("No holding arrays found for this specific contract destination.")
                else:
                    st.info(f"Analyzing transaction histories for top {t6_top_n} holders...")
                    # Balance calculations logic goes here...

elif nav_select == "🐋 Cohort Analyzer":
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

elif nav_select == "🔍 Whale Overlap":
    st.header("Whale Overlap Matrix")
    raw_input = st.text_area("Paste Target Addresses (One Per Line)")
    if st.button("Scan Asset Overlaps") and raw_input:
        wallets = [w.strip() for w in raw_input.splitlines() if len(w.strip()) >= 32]
        # Cross-reference holdings loops logic...

elif nav_select == "📅 Recent Buys":
    st.header("Recent Purchases Tracer")
    t3_days = st.slider("Lookback Window Horizon (Days)", 1, 30, 7)
    # Stream transaction tracking logic...

elif nav_select == "📌 Watchlist":
    st.header("Preset Watchlist Scan")
    st.info(f"System tracking loaded with **{len(PRESET_WALLETS)}** structural target profiles.")
    if st.button("Scan Watchlist Inflows"):
        # Evaluates watchlist profiles...
        pass

elif nav_select == "🤝 Common Holders":
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
                st.dataframe(pd.DataFrame(common_set, columns=["Wallet Address"]), use_container_width=True, hide_index=True)

elif nav_select == "💰 Wallet PnL":
    st.header("Wallet Capital Performance Dashboard")
    target_wallet = st.text_input("Query Wallet Account Address")
    # Balance ledger logic...
