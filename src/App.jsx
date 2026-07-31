import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { fetchStockData, fetchNewsData, analyzeStock } from './api';
import SearchBar from './components/SearchBar';
import Dashboard from './components/Dashboard';
import AIAnalyst from './components/AIAnalyst';
import NewsFeed from './components/NewsFeed';

export default function App() {
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState('');
  
  const [stockData, setStockData] = useState(null);
  const [newsData, setNewsData] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  const handleSearch = async (ticker) => {
    setLoading(true);
    setError('');
    setStockData(null);
    setNewsData(null);
    setAnalysis(null);
    setAnalyzing(false);

    try {
      // 1. Fetch Stock Data
      const stock = await fetchStockData(ticker);
      setStockData(stock);

      // 2. Fetch News
      const news = await fetchNewsData(ticker);
      setNewsData(news.news);

      // 3. Request AI Analysis
      setAnalyzing(true);
      setLoading(false); // UI can show data while AI thinks
      
      const aiResponse = await analyzeStock({
        ticker: stock.ticker,
        company_name: stock.name,
        stock_data: stock,
        news_data: news.news
      });
      
      setAnalysis(aiResponse.analysis);
      setAnalyzing(false);
      
    } catch (err) {
      console.error(err);
      const status = err.response?.status ? `(HTTP ${err.response.status}) ` : '';
      const detail = err.response?.data?.detail || err.message;
      const htmlWarning = typeof err.response?.data === 'string' && err.response.data.includes('<html') ? ' - Vercel returned an HTML page (Routing issue)' : '';
      setError(`Error: ${status}${detail}${htmlWarning}`);
    } finally {setLoading(false);
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-slate-200 selection:bg-primary/30 font-sans relative overflow-x-hidden">
      {/* Abstract Background Elements */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px] mix-blend-screen"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-accent/10 rounded-full blur-[120px] mix-blend-screen"></div>
      </div>

      <main className="relative z-10 container mx-auto px-6 py-12">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-block px-3 py-1 mb-4 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm text-xs font-medium tracking-widest text-accent uppercase">
            NSE / BSE Powered
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-4 text-white">
            Equity <span className="gradient-text">AI</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Deep-dive fundamental analysis, real-time news synthesis, and expert investing advice powered by Anthropic Claude.
          </p>
        </motion.div>

        <SearchBar onSearch={handleSearch} loading={loading} />

        <AnimatePresence>
          {error && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl max-w-2xl mx-auto mb-8 text-center"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        {stockData && (
          <div className="mt-12 space-y-8">
            <Dashboard stock={stockData} />
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2">
                <AIAnalyst analysis={analysis} loading={analyzing} />
              </div>
              <div className="lg:col-span-1">
                <NewsFeed news={newsData} />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
