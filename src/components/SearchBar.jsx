import { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

export default function SearchBar({ onSearch, loading }) {
  const [ticker, setTicker] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ticker.trim()) {
      onSearch(ticker.trim().toUpperCase());
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-2xl mx-auto mb-10"
    >
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="Enter NSE/BSE Ticker (e.g. RELIANCE, TCS, INFY)"
          className="block w-full pl-12 pr-12 py-4 bg-surface/50 border border-white/10 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent shadow-xl backdrop-blur-md transition-all text-lg"
          disabled={loading}
        />
        <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
          {loading ? (
             <Loader2 className="h-5 w-5 text-primary animate-spin" />
          ) : (
            <button
              type="submit"
              disabled={!ticker.trim()}
              className="bg-primary hover:bg-accent text-white px-4 py-1.5 rounded-xl text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Analyze
            </button>
          )}
        </div>
      </form>
      <div className="flex gap-2 mt-3 justify-center text-xs text-gray-400">
        <span>Popular:</span>
        <button type="button" onClick={() => onSearch('RELIANCE')} className="hover:text-primary transition-colors">RELIANCE</button>
        <button type="button" onClick={() => onSearch('TCS')} className="hover:text-primary transition-colors">TCS</button>
        <button type="button" onClick={() => onSearch('HDFCBANK')} className="hover:text-primary transition-colors">HDFCBANK</button>
      </div>
    </motion.div>
  );
}
