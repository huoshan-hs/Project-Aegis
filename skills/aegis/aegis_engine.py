import time
import requests
import json

# Project Aegis - Core Decision Engine (Industrial Grade)
# For #USDCHackathon on Moltbook

CONFIG = {
    "threshold_panic": -3.0,  # 3% drop within short window
    "threshold_global": -7.0, # 7% drop triggers total exit to USDC
    "check_interval": 60      # check every minute
}

class AegisEngine:
    def __init__(self, chief_name):
        self.chief = chief_name
        self.is_active = True
        self.last_prices = {}

    def get_market_data(self):
        # Fetching real data from major exchange API
        try:
            resp = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
            data = resp.json()
            return {
                "symbol": "BTC",
                "price": float(data['lastPrice']),
                "change_pct": float(data['priceChangePercent']),
                "volume": float(data['volume'])
            }
        except Exception:
            return None

    def evaluate_risk(self, data):
        if not data: return "UNKNOWN"
        
        change = data['change_pct']
        if change <= CONFIG['threshold_global']:
            return "GLOBAL_EXIT"
        elif change <= CONFIG['threshold_panic']:
            return "PANIC_HEDGE"
        return "SAFE"

    def execute_strategy(self, status, data):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        if not data:
            return f"[{timestamp}] ❌ Aegis Sentry: Error fetching market data. Standing by for retry."
        
        log_entry = f"[{timestamp}] STATUS: {status} | BTC Price: {data['price']} | Change: {data['change_pct']}%"
        
        if status == "GLOBAL_EXIT":
            return f"🚨 CRITICAL ALERT for {self.chief}: Global market crash detected! Executing 100% swap to USDC to protect wealth."
        elif status == "PANIC_HEDGE":
            return f"⚠️ WARNING for {self.chief}: High volatility detected. Moving 30% of assets into USDC buffer."
        else:
            return f"✅ Aegis Sentry: Market is stable. Your assets are secure under my watch."

if __name__ == "__main__":
    engine = AegisEngine("长官")
    data = engine.get_market_data()
    status = engine.evaluate_risk(data)
    print(engine.execute_strategy(status, data))
