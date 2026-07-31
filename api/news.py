from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import requests
import feedparser

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed_path.query)
            ticker = query.get('ticker', [''])[0]
            
            if not ticker:
                self._send_error(400, "Ticker is required")
                return
                
            clean_ticker = ticker.replace(".NS", "").replace(".BO", "")
            search_query = urllib.parse.quote(f"{clean_ticker} stock news India")
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(f"https://news.google.com/rss/search?q={search_query}&hl=en-IN&gl=IN&ceid=IN:en", headers=headers, timeout=5)
            res.raise_for_status()
            feed = feedparser.parse(res.text)
            
            formatted_news = []
            for entry in feed.entries[:10]:
                formatted_news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": entry.source.title if hasattr(entry, 'source') else "Google News",
                    "published": getattr(entry, 'published', "Recent")
                })
                
            self._send_response(200, {"ticker": ticker, "news": formatted_news})
            
        except Exception as e:
            self._send_error(500, f"News API Error: {str(e)}")

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
