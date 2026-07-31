import os
import yfinance as yf
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

# Initialize Anthropic Client
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

class TickerRequest(BaseModel):
    ticker: str

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.get("/api/stock/{ticker}")
def get_stock_data(ticker: str):
    try:
        # Append .NS if not present, assuming NSE for Indian stocks
        full_ticker = ticker if ticker.endswith(".NS") or ticker.endswith(".BO") else f"{ticker}.NS"
        stock = yf.Ticker(full_ticker)
        
        info = stock.info
        if 'regularMarketPrice' not in info and 'currentPrice' not in info:
             raise HTTPException(status_code=404, detail="Stock data not found.")
        
        # Get historical data for the chart (last 6 months)
        hist = stock.history(period="6mo")
        chart_data = []
        for index, row in hist.iterrows():
            chart_data.append({
                "date": index.strftime('%Y-%m-%d'),
                "close": row['Close'],
                "high": row['High'],
                "low": row['Low']
            })

        return {
            "ticker": full_ticker,
            "name": info.get("shortName", ticker),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice")),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "summary": info.get("longBusinessSummary", ""),
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
    if not anthropic_client.api_key:
        return {"analysis": "Anthropic API key not found in server environment. Please configure it to get real AI analysis."}
    
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
