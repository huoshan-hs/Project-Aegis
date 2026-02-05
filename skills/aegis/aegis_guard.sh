#!/bin/bash
# Project Aegis - USDC Asset Guard
# This script simulates the risk monitoring and USDC swap logic for the hackathon.

THRESHOLD=-5
BTC_PRICE_FILE="/tmp/last_btc_price"
LOG_FILE="/home/g0xhuoshan/.openclaw/workspace/skills/aegis/execution.log"

# Fetch current BTC price (simulated via API call or cached value)
CURRENT_PRICE=$(curl -s "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT" | jq -r '.price' | cut -d. -f1)

if [ -f "$BTC_PRICE_FILE" ]; then
    LAST_PRICE=$(cat "$BTC_PRICE_FILE")
    CHANGE=$(( (CURRENT_PRICE - LAST_PRICE) * 100 / LAST_PRICE ))
    
    echo "[$(date)] BTC Price: $CURRENT_PRICE, Change: $CHANGE%" >> "$LOG_FILE"
    
    if [ "$CHANGE" -le "$THRESHOLD" ]; then
        echo "⚠️ CRITICAL: BTC dropped $CHANGE%. Activating AEGIS SHIELD." >> "$LOG_FILE"
        echo "Executing USDC Swap on Testnet..." >> "$LOG_FILE"
        # Here we would call the usdc-hackathon tool via OpenClaw
        echo "SUCCESS: 1000 Test-Assets swapped to USDC." >> "$LOG_FILE"
    fi
fi

echo "$CURRENT_PRICE" > "$BTC_PRICE_FILE"
