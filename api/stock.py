from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import requests
import time

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed_path.query)
            ticker = query.get('ticker', [''])[0]
            
            if not ticker:
                self._send_error(400, "Ticker is required")
                return
                
            full_ticker = ticker if ticker.endswith(".NS") or ticker.endswith(".BO") else f"{ticker}.NS"
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{full_ticker}?range=6mo&interval=1d"
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            data = res.json()
            
            result = data.get("chart", {}).get("result", [])
            if not result:
                self._send_error(404, "Stock data not found.")
                return
                
            meta = result[0].get("meta", {})
            timestamps = result[0].get("timestamp", [])
            indicators = result[0].get("indicators", {}).get("quote", [{}])[0]
            
            chart_data = []
            for i, ts in enumerate(timestamps):
                if i < len(indicators.get("close", [])) and indicators["close"][i] is not None:
                    chart_data.append({
                        "date": time.strftime('%Y-%m-%d', time.localtime(ts)),
                        "close": indicators["close"][i],
                        "high": indicators["high"][i],
                        "low": indicators["low"][i]
                    })
            
            response_data = {
                "ticker": full_ticker,
                "name": meta.get("longName", meta.get("symbol")),
                "sector": "Indian Equities",
                "industry": "Public Company",
                "current_price": meta.get("regularMarketPrice"),
                "market_cap": None,
                "pe_ratio": None,
                "52_week_high": meta.get("fiftyTwoWeekHigh"),
                "52_week_low": meta.get("fiftyTwoWeekLow"),
                "summary": "Data sourced directly from Yahoo Finance API.",
                "chart_data": chart_data
            }
            self._send_response(200, response_data)
            
        except Exception as e:
            self._send_error(500, f"Yahoo API Error: {str(e)}")

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()

    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _send_error(self, status, detail):
        self._send_response(status, {"detail": detail})
