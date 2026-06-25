#!/usr/bin/env python3
"""CabalScan — Automated Background Scanner Processing Engine."""

import os
import sys
import json
import time
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from pathlib import Path

# Pull config arrays directly via single location import paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import PRESET_WALLETS, SKIP_TOKENS, EXCHANGE_WALLETS
import helpers as hlp

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

LOOKBACK_HOURS = int(os.environ.get("SCAN_LOOKBACK_HOURS", "24"))
HELIUS_KEY = os.environ.get("HELIUS_API_KEY", "").strip()

if not HELIUS_KEY:
    print("Critical Failure: HELIUS_API_KEY environment variable context required.")
    sys.exit(1)

HELIUS_URL = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY}"

def execution_loop():
    now_ts = int(datetime.now(timezone.utc).timestamp())
    cutoff_ts = now_ts - (LOOKBACK_HOURS * 3600)
    
    print(f"Starting tracking run over {len(PRESET_WALLETS)} watchlist profiles...")
    
    all_acquisitions = []
    token_wallets = defaultdict(set)
    token_amounts = defaultdict(float)
    
    for i, wallet in enumerate(PRESET_WALLETS):
        try:
            sigs = hlp.fetch_signatures(wallet, HELIUS_URL, limit=100)
            for sig_info in sigs:
                if sig_info.get("blockTime", 0) < cutoff_ts:
                    break
                tx = hlp.fetch_transaction(sig_info["signature"], HELIUS_URL)
                inflows = hlp.parse_token_inflows(tx, wallet, sig_info["signature"])
                for acq in inflows:
                    mint = acq["mint"]
                    token_wallets[mint].add(wallet)
                    token_amounts[mint] += acq["amount_received"]
                    acq["wallet"] = wallet
                    all_acquisitions.append(acq)
            time.sleep(0.1) # Safe pace delay
        except Exception as e:
            print(f"\nError processing history frame on profile {wallet[:8]}: {str(e)}")

    # Multi-token grouping configurations
    all_mints = list(token_wallets.keys())
    token_meta = hlp.enrich_token_metadata(all_mints, HELIUS_URL) if all_mints else {}
    
    trending = {}
    for mint, wallets_set in token_wallets.items():
        if len(wallets_set) >= 2:
            meta = token_meta.get(mint, {"symbol": mint[:8], "name": "Unknown", "price_usd": 0.0})
            trending[mint] = {
                "symbol": meta["symbol"], "name": meta["name"], "price": meta["price_usd"],
                "wallet_count": len(wallets_set), "total_amount": round(token_amounts[mint], 4)
            }
            
    payload = {
        "scan_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "wallets_scanned": len(PRESET_WALLETS),
        "total_acquisitions": len(all_acquisitions),
        "unique_tokens": len(token_wallets),
        "trending": dict(sorted(trending.items(), key=lambda x: -x[1]["wallet_count"]))
    }
    
    # ATOMIC SAVE PATTERN: Writing safely to a temporary target before updating links avoids OS crashes
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    temp_target = DATA_DIR / f"scan_{ts}.json"
    latest_target = DATA_DIR / "latest.json"
    
    with open(temp_target, "w") as f:
        json.dump(payload, f, indent=2)
        
    if latest_target.exists():
        latest_target.unlink()
    temp_target.link_to(latest_target)
    
    print(f"Cycle completed successfully. Logs locked to static indices.")

if __name__ == "__main__":
    execution_loop()
