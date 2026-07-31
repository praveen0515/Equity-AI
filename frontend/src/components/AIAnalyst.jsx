import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { Sparkles, BrainCircuit } from 'lucide-react';

export default function AIAnalyst({ analysis, loading }) {
  if (loading) {
    return (
      <div className="glass-panel p-8 min-h-[400px] flex flex-col items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-accent/10 opacity-50 animate-pulse"></div>
        <BrainCircuit className="h-16 w-16 text-primary animate-bounce mb-6" />
        <h3 className="text-xl font-medium text-white mb-2">Anthropic AI is analyzing...</h3>
        <p className="text-gray-400 text-sm text-center max-w-sm">
          Processing quarterly reports, financial metrics, and recent news to generate investment advice.
        </p>
      </div>
    );
  }

  if (!analysis) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="glass-panel p-8 relative overflow-hidden"
    >
      <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
         <Sparkles className="h-48 w-48 text-accent" />
      </div>
      
      <div className="flex items-center gap-3 mb-6 border-b border-white/10 pb-4">
        <div className="p-2 bg-gradient-to-r from-primary to-accent rounded-lg">
          <BrainCircuit className="h-6 w-6 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">AI Investment Thesis</h2>
        <span className="ml-auto text-xs font-mono px-3 py-1 bg-white/5 rounded-full border border-white/10 text-gray-400">
          Powered by Claude
        </span>
      </div>

      <div className="prose prose-invert prose-p:text-gray-300 prose-headings:text-white prose-a:text-accent prose-strong:text-white max-w-none">
        <ReactMarkdown>{analysis}</ReactMarkdown>
      </div>
    </motion.div>
  );
}
