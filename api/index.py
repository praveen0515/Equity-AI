import os
import requests
import feedparser
import urllib.parse
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = FastAPI(title="Indian AI Advisor API")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic Client safely so it doesn't crash the entire API on boot if missing
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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        # Fetch 6 months of historical data & meta info from Yahoo API
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{full_ticker}?range=6mo&interval=1d"
        res = requests.get(url, headers=headers)
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
            "market_cap": "N/A", # Yahoo chart API doesn't return market cap, but AI doesn't strictly need it to analyze trends
            "pe_ratio": "N/A",
            "52_week_high": meta.get("fiftyTwoWeekHigh"),
            "52_week_low": meta.get("fiftyTwoWeekLow"),
            "summary": "Data sourced directly from Yahoo Finance API.",
            "chart_data": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news/{ticker}")
def get_news(ticker: str):
    try:
        clean_ticker = ticker.replace(".NS", "").replace(".BO", "")
        query = urllib.parse.quote(f"{clean_ticker} stock news India")
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en")
        
        formatted_news = []
        for entry in feed.entries[:10]:
            pub_time = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_time = int(time.mktime(entry.published_parsed))
            
            formatted_news.append({
                "title": entry.title,
                "publisher": entry.source.title if hasattr(entry, 'source') else "Google News",
                "link": entry.link,
                "providerPublishTime": pub_time
            })
            
        if not formatted_news:
             formatted_news.append({
                 "title": f"Monitoring active news for {clean_ticker} across Indian markets.",
                 "publisher": "System Alert",
                 "link": "#",
                 "providerPublishTime": None
             })
             
        return {"news": formatted_news}
    except Exception as e:
        print(f"News fetch error: {e}")
        return {"news": []}

class AnalyzeRequest(BaseModel):
    ticker: str
    company_name: str
    stock_data: dict
    news_data: list

@app.post("/api/analyze")
def analyze_stock(request: AnalyzeRequest):
    if not anthropic_client:
        raise HTTPException(status_code=500, detail="Anthropic API Key is not configured in Vercel Environment Variables.")
    
    try:
        prompt = f"""
        You are an expert Indian Equity Analyst. Analyze the following information for {request.company_name} ({request.ticker}).
        
        Financial Context:
        Current Price: {request.stock_data.get('current_price')}
        P/E Ratio: {request.stock_data.get('pe_ratio')}
        Market Cap: {request.stock_data.get('market_cap')}
        Sector: {request.stock_data.get('sector')}
        
        Recent News:
        {chr(10).join([f"- {n['title']} ({n['publisher']})" for n in request.news_data])}
        
        Please provide a comprehensive summary and investment advice. Format your response in Markdown with the following sections:
        1. Executive Summary (2-3 sentences)
        2. Quarterly & News Analysis (Extract important info from the news and general context)
        3. Key Risks & Tailwinds
        4. Investment Suggestion (Buy/Hold/Sell) with clear rationale.
        
        Make sure the analysis is insightful, objective, and specifically focused on the Indian market context.
        """
        
        message = anthropic_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            temperature=0.2,
            system="You are a professional financial advisor specializing in the Indian Stock Market (NSE/BSE).",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return {"analysis": message.content[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
