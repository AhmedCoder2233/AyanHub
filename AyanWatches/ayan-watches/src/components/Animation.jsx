import React, { useState, useEffect } from 'react';
import { Watch, ShoppingCart, User, Search, Menu, X, ChevronDown, ArrowRight, Star, Award, Shield } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Loading Animation Component
export function LoadingAnimation({ onComplete }) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(timer);
          setTimeout(onComplete, 500);
          return 100;
        }
        return prev + 2;
      });
    }, 20);

    return () => clearInterval(timer);
  }, [onComplete]);

  return (
    <motion.div
      initial={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed inset-0 z-[100] bg-black flex flex-col items-center justify-center"
    >
      {/* Logo Image */}
      <motion.div
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="mb-8"
      >
        <div className="relative">
          <motion.div
            animate={{ 
              boxShadow: [
                "0 0 30px rgba(251, 191, 36, 0.3)",
                "0 0 60px rgba(251, 191, 36, 0.6)",
                "0 0 30px rgba(251, 191, 36, 0.3)"
              ]
            }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-32 h-32 sm:w-40 sm:h-40 rounded-full overflow-hidden border-4 border-amber-400"
          >
            <img 
              src="/logo.jpeg" 
              alt="Chronos Logo" 
              className="w-full h-full object-cover"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }}
            />
            <div style={{ display: 'none' }} className="w-full h-full bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center">
              <Watch className="w-16 h-16 text-black" />
            </div>
          </motion.div>
        </div>
      </motion.div>

      {/* Brand Name */}
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.8 }}
        className="text-2xl text-center sm:text-5xl font-bold bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 bg-clip-text text-transparent mb-2"
      >
        Ayan Watches Hub
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.8 }}
        className="text-amber-200/60 tracking-widest text-sm mb-12"
      >
        LUXURY PRODUCTS
      </motion.p>

      {/* Progress Bar */}
      <div className="w-64 h-1 bg-gray-800 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          className="h-full bg-gradient-to-r from-amber-400 to-yellow-600"
        />
      </div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
        className="text-amber-200/40 text-sm mt-4"
      >
        Loading Excellence...
      </motion.p>
    </motion.div>
  );
}