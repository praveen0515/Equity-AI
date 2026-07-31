import traceback
import sys

global_boot_error = None
try:
    import os
    import requests
    import feedparser
    import urllib.parse
    import time
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import anthropic
    
    app = FastAPI(title="Indian AI Advisor API")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    try:
        anthropic_client = anthropic.Anthropic(api_key=api_key) if api_key else None
    except Exception:
        anthropic_client = None
    
    class TickerRequest(BaseModel):
        ticker: str
    
    @app.get("/")
    def read_root():
        return {"status": "API is running"}
    
    @app.get("/api/stock/{ticker}")
    def get_stock_data(ticker: str):
        try:
            full_ticker = ticker if ticker.endswith(".NS") or ticker.endswith(".BO") else f"{ticker}.NS"
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{full_ticker}?range=6mo&interval=1d"
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            data = res.json()
            
            result = data.get("chart", {}).get("result", [])
            if not result:
                raise HTTPException(status_code=404, detail="Stock data not found.")
                
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
    
            return {
                "ticker": full_ticker,
                "name": meta.get("longName", meta.get("symbol")),
                "sector": "Indian Equities",
                "industry": "Public Company",
                "current_price": meta.get("regularMarketPrice"),
                "market_cap": "N/A",
                "pe_ratio": "N/A",
                "52_week_high": meta.get("fiftyTwoWeekHigh"),
                "52_week_low": meta.get("fiftyTwoWeekLow"),
                "summary": "Data sourced directly from Yahoo Finance API.",
                "chart_data": chart_data
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Yahoo API Error: {str(e)}")
    
    @app.get("/api/news/{ticker}")
    def get_news(ticker: str):
        try:
            clean_ticker = ticker.replace(".NS", "").replace(".BO", "")
            query = urllib.parse.quote(f"{clean_ticker} stock news India")
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en", headers=headers, timeout=5)
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
            return {"ticker": ticker, "news": formatted_news}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"News API Error: {str(e)}")
            
    class AnalyzeRequest(BaseModel):
        ticker: str
        stock_data: dict
        news_data: list
    
    @app.post("/api/analyze")
    def analyze_stock(request: AnalyzeRequest):
        if not anthropic_client:
            raise HTTPException(status_code=500, detail="Anthropic API Key is not configured in Vercel.")
        try:
            prompt = f"Analyze {request.ticker} based on this data: {request.stock_data} and news: {request.news_data}"
            message = anthropic_client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1500,
                temperature=0.2,
                system="You are a professional financial advisor specializing in the Indian Stock Market.",
                messages=[{"role": "user", "content": prompt}]
            )
            return {"analysis": message.content[0].text}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Anthropic API Error: {str(e)}")

except Exception as e:
    global_boot_error = traceback.format_exc()
    
    async def app(scope, receive, send):
        assert scope['type'] == 'http'
        import json
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [
                [b'content-type', b'application/json'],
                [b'access-control-allow-origin', b'*']
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({"detail": f"ASGI BOOT ERROR: {global_boot_error}"}).encode('utf-8'),
        })

