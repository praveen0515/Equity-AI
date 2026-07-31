# Equity AI 📈🤖

An AI-powered financial advisor tailored specifically for the Indian Stock Market (NSE/BSE). Equity AI aggregates live market metrics, scrapes the latest corporate news, and utilizes Anthropic's Claude 4.5/5 models to generate a comprehensive, intelligent investment thesis in seconds.

## ✨ Features

- **Live Market Data:** Fetches real-time pricing, market cap, P/E ratios, and 52-week highs/lows using `yfinance`.
- **Intelligent News Aggregation:** Pulls the latest news directly from Google News RSS using `feedparser` to ensure the AI has context on current market sentiment.
- **Anthropic Claude Integration:** Acts as an expert Indian Equity Analyst, synthesizing data into actionable insights and a quarterly summary.
- **Modern UI:** Built with React, Tailwind CSS v4, and Framer Motion for a stunning, glassmorphism-inspired dark mode experience.

## 🏗️ Architecture

The project is decoupled into two primary components:

- `backend/`: A highly concurrent Python FastAPI server.
- `frontend/`: A blazing fast React single-page application built on Vite.

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python 3.10+
- An Anthropic API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/equity-ai.git
   cd equity-ai
   ```

2. **Configure your API Key:**
   Navigate into the `backend/` directory and create a `.env` file:
   ```bash
   echo 'ANTHROPIC_API_KEY="your_actual_key_here"' > backend/.env
   ```

3. **Install dependencies:**
   The easiest way is to use the provided setup scripts, but manually:
   - Backend: `cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
   - Frontend: `cd frontend && npm install`

### Running the App

To start both the backend and frontend simultaneously, simply run the included bash script from the root of the project:

```bash
chmod +x run.sh
./run.sh
```

- Frontend will be available at: `http://localhost:5173`
- Backend API will be available at: `http://localhost:8000`

## 🛠️ Tech Stack

- **Frontend:** React, Vite, Tailwind CSS v4, Framer Motion, Axios, Lucide Icons, React Markdown.
- **Backend:** FastAPI, Uvicorn, Python, yFinance, Feedparser, Anthropic SDK.

## 📝 License

This project is licensed under the MIT License.
