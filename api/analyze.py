from http.server import BaseHTTPRequestHandler
import json
import os
import anthropic

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error(400, "Empty request body")
                return
                
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))
            
            ticker = body.get('ticker')
            stock_data = body.get('stock_data')
            news_data = body.get('news_data')
            
            if not ticker:
                self._send_error(400, "Ticker is required")
                return

            api_key = os.getenv("ANTHROPIC_API_KEY", "")
            if not api_key:
                self._send_error(500, "Anthropic API Key is not configured in Vercel.")
                return
                
            client = anthropic.Anthropic(api_key=api_key)
            prompt = f"Analyze {ticker} based on this data: {stock_data} and news: {news_data}"
            
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1500,
                temperature=0.2,
                system="You are a professional financial advisor specializing in the Indian Stock Market.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            self._send_response(200, {"analysis": message.content[0].text})
            
        except Exception as e:
            self._send_error(500, f"Anthropic API Error: {str(e)}")

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
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
