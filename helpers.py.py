"""Centralized blockchain network engines for CabalScan processing."""
import time
import requests
from datetime import datetime, timezone
from config import SKIP_TOKENS

def fetch_with_backoff(url: str, payload: dict, max_retries: int = 3) -> dict:
    """Handles network timeouts and gracefully backs off when hitting 429 rate limits."""
    if not url:
        return {}
    for attempt in range(max_retries):
        try:
            r = requests.post(url, json=payload, timeout=20)
            if r.status_code == 429:
                time.sleep(1.5 * (attempt + 1))  # Exponential backoff
                continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                return {}
            time.sleep(1.0)
    return {}

def get_assets(wallet: str, helius_url: str) -> list:
    """Fetch fungible asset portfolio values for a wallet address via DAS."""
    payload = {
        "jsonrpc": "2.0", "id": "wai",
        "method": "getAssetsByOwner",
        "params": {
            "ownerAddress": wallet,
            "page": 1, "limit": 1000,
            "displayOptions": {"showFungible": True},
        },
    }
    res = fetch_with_backoff(helius_url, payload)
    return res.get("result", {}).get("items", [])

def fetch_signatures(wallet: str, helius_url: str, limit: int = 100) -> list:
    """Query recent execution block signatures for verification tracking."""
    payload = {
        "jsonrpc": "2.0", "id": "sigs",
        "method": "getSignaturesForAddress",
        "params": [wallet, {"limit": limit}],
    }
    res = fetch_with_backoff(helius_url, payload)
    return res.get("result", [])

def fetch_transaction(sig: str, helius_url: str) -> dict:
    """Extract individual parsed block metrics."""
    payload = {
        "jsonrpc": "2.0", "id": "tx",
        "method": "getTransaction",
        "params": [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}],
    }
    res = fetch_with_backoff(helius_url, payload)
    return res.get("result")

def parse_token_inflows(tx: dict, wallet: str, sig: str) -> list:
    """Evaluate asset balance changes to accurately pinpoint acquisition movements."""
    inflows = []
    if not tx:
        return inflows

    meta = tx.get("meta", {})
    block_time = tx.get("blockTime", 0)
    pre = {e["accountIndex"]: e for e in meta.get("preTokenBalances", [])}
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
        pre_amt = float((pre.get(idx, {}).get("uiTokenAmount") or {}).get("uiAmount") or 0)
        post_amt = float((post.get(idx, {}).get("uiTokenAmount") or {}).get("uiAmount") or 0)
        if post_amt > pre_amt:
            mint = post.get(idx, {}).get("mint") or pre.get(idx, {}).get("mint", "unknown")
            if mint in SKIP_TOKENS:
                continue
            inflows.append({
                "mint": mint,
                "amount_received": round(post_amt - pre_amt, 6),
                "timestamp": block_time,
                "date": datetime.fromtimestamp(block_time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                "tx_sig": sig,
            })
    return inflows

def enrich_token_metadata(mints: list, helius_url: str) -> dict:
    """Resolves names, trading symbols, and spot valuations for on-chain contract addresses."""
    meta = {}
    unique_mints = list(set(mints))
    for i in range(0, len(unique_mints), 100):
        batch = unique_mints[i:i+100]
        payload = {
            "jsonrpc": "2.0", "id": "batch-meta",
            "method": "getAssetBatch",
            "params": {"ids": batch},
        }
        res = fetch_with_backoff(helius_url, payload)
        for asset in res.get("result", []):
            if not asset:
                continue
            mint = asset.get("id", "")
            if mint:
                m = asset.get("content", {}).get("metadata", {})
                ti = asset.get("token_info", {})
                pi = ti.get("price_info", {})
                meta[mint] = {
                    "symbol": m.get("symbol", mint[:8]),
                    "name": m.get("name", "Unknown"),
                    "price_usd": float(pi.get("price_per_token", 0)) if pi else 0.0
                }
    return meta