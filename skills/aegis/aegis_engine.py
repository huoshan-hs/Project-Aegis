import time
import requests
import json
import sys

# Project Aegis - Core Decision Engine (Pro Edition)
# Powered by Gemini 3 Pro logic for #USDCHackathon

CONFIG = {
    "threshold_panic": 40,    # Risk score threshold for partial hedge
    "threshold_critical": 80, # Risk score threshold for total exit
}

class AegisEngine:
    def __init__(self, chief_name):
        self.chief = chief_name
        self.active = True

    def get_market_data(self):
        # Primary: CoinGecko (more reliable from VPS)
        try:
            resp = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true",
                timeout=10
            )
            data = resp.json()
            btc = data.get('bitcoin', {})
            return {
                "symbol": "BTC",
                "price": btc.get('usd', 0),
                "change_pct": btc.get('usd_24h_change', 0),
                "volume": btc.get('usd_24h_vol', 0),
            }
        except Exception as e:
            return None

    def calculate_risk_score(self, data):
        if not data or data['price'] == 0:
            return 0
        
        score = 0.0
        change = data['change_pct']
        
        # 1. Price Momentum Analysis
        if change < 0:
            # Downside volatility weighs heavier in risk model
            # e.g., -5% -> 75 points, -7% -> 105 points (critical)
            score += abs(change) * 15
        else:
            # Upside reduces risk slightly
            score -= min(change * 3, 20)

        # 2. Extreme Drop Multiplier
        if change <= -10:
            score *= 1.5  # Flash crash scenario

        # 3. Moderate Correction Buffer
        # Small dips (-1% to -3%) are normal, don't overreact
        if -3 < change < 0:
            score *= 0.6

        return round(max(score, 0), 2)

    def decide(self, data):
        if not data:
            return "ERROR", 0
        
        risk_score = self.calculate_risk_score(data)
        
        if risk_score >= CONFIG['threshold_critical']:
            return "GLOBAL_EXIT", risk_score
        elif risk_score >= CONFIG['threshold_panic']:
            return "PANIC_HEDGE", risk_score
        else:
            return "HOLD", risk_score

    def execute(self):
        data = self.get_market_data()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if not data:
            return f"[{timestamp}] ❌ Aegis Sentry: Data feed connection failed."

        action, score = self.decide(data)
        
        report = f"[{timestamp}] BTC: ${data['price']:,.0f} ({data['change_pct']:+.2f}%) | Risk Score: {score:.0f}/100"
        
        if action == "GLOBAL_EXIT":
            return f"{report}\n🚨 CRITICAL: Risk score critical! Executing 100% USDC SWAP immediately."
        elif action == "PANIC_HEDGE":
            return f"{report}\n⚠️ WARNING: Elevated risk detected. Hedging 30% to USDC."
        else:
            return f"{report}\n✅ SAFE: Market conditions stable. Holding positions."

if __name__ == "__main__":
    engine = AegisEngine("长官")
    print(engine.execute())
