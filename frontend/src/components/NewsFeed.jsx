import { motion } from 'framer-motion';
import { Newspaper, ExternalLink } from 'lucide-react';

export default function NewsFeed({ news }) {
  if (!news || news.length === 0) return null;

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const item = {
    hidden: { opacity: 0, x: 20 },
    show: { opacity: 1, x: 0 }
  };

  return (
    <motion.div 
      variants={container}
      initial="hidden"
      animate="show"
      className="glass-panel p-6 h-full"
    >
      <div className="flex items-center gap-2 mb-6 border-b border-white/10 pb-4">
        <Newspaper className="h-5 w-5 text-accent" />
        <h3 className="text-xl font-bold text-white">Latest News</h3>
      </div>
      
      <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2">
        {news.map((item, idx) => (
          <motion.div 
            key={idx} 
            variants={item}
            className="p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors group cursor-pointer"
            onClick={() => window.open(item.link, '_blank')}
          >
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-semibold text-primary px-2 py-1 bg-primary/10 rounded-md">
                {item.publisher || 'Finance News'}
              </span>
              <span className="text-xs text-gray-500">
                {item.providerPublishTime ? new Date(item.providerPublishTime * 1000).toLocaleDateString() : 'Recent'}
              </span>
            </div>
            <h4 className="text-sm font-medium text-gray-200 group-hover:text-white transition-colors leading-snug mb-2">
              {item.title}
            </h4>
            <div className="flex items-center text-xs text-accent opacity-0 group-hover:opacity-100 transition-opacity">
              Read article <ExternalLink className="h-3 w-3 ml-1" />
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
