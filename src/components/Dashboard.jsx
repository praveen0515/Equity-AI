import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, DollarSign, Activity, PieChart, Info } from 'lucide-react';

export default function Dashboard({ stock }) {
  if (!stock) return null;

  const formatNumber = (num) => {
    if (!num) return 'N/A';
    if (num >= 1e12) return `₹${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e7) return `₹${(num / 1e7).toFixed(2)}Cr`; // Indian formatting (Crores)
    return `₹${num.toLocaleString()}`;
  };

  const isPositive = true; // For demo, you'd calculate this based on previous close vs current

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <motion.div 
      variants={container}
      initial="hidden"
      animate="show"
      className="w-full"
    >
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            {stock.name} 
            <span className="text-sm px-2 py-1 bg-white/10 rounded-md text-gray-300 border border-white/10 font-normal">
              {stock.ticker}
            </span>
          </h1>
          <p className="text-gray-400 mt-1">{stock.sector} • {stock.industry}</p>
        </div>
        <div className="text-right">
          <div className="text-4xl font-bold text-white">₹{stock.current_price?.toLocaleString() || 'N/A'}</div>
          {/* Mocked positive change for aesthetics, real implementation would compare with prev close */}
          <div className={`flex items-center justify-end mt-1 font-medium ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
            {isPositive ? <TrendingUp className="h-4 w-4 mr-1" /> : <TrendingDown className="h-4 w-4 mr-1" />}
            +1.24% Today
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Market Cap', value: formatNumber(stock.market_cap), icon: PieChart },
          { label: 'P/E Ratio', value: typeof stock.pe_ratio === 'number' ? stock.pe_ratio.toFixed(2) : 'N/A', icon: Activity },
          { label: '52W High', value: stock['52_week_high'] ? `₹${stock['52_week_high'].toLocaleString()}` : 'N/A', icon: TrendingUp },
          { label: '52W Low', value: stock['52_week_low'] ? `₹${stock['52_week_low'].toLocaleString()}` : 'N/A', icon: TrendingDown },
        ].map((stat, idx) => (
          <motion.div variants={item} key={idx} className="glass-card">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 bg-primary/10 rounded-lg text-primary">
                <stat.icon className="h-4 w-4" />
              </div>
              <span className="text-sm text-gray-400">{stat.label}</span>
            </div>
            <div className="text-xl font-semibold text-white">{stat.value}</div>
          </motion.div>
        ))}
      </div>
      
      <motion.div variants={item} className="glass-panel p-6">
         <h3 className="text-lg font-medium text-white mb-4 flex items-center gap-2">
            <Info className="h-5 w-5 text-accent" /> Company Overview
         </h3>
         <p className="text-gray-300 text-sm leading-relaxed line-clamp-4 hover:line-clamp-none transition-all">
            {stock.summary || 'No business summary available.'}
         </p>
      </motion.div>
    </motion.div>
  );
}
