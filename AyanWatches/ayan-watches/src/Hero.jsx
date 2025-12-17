import { Watch, ArrowRight, Star, Award, Shield } from 'lucide-react';
import { motion } from 'framer-motion';

// Hero Section Component
export default function HeroSection() {
  return (
    <>      
      {/* Hero Section */}
      <section className="relative h-[1150px] sm:h-[1300px] lg:h-[900px] overflow-hidden bg-gradient-to-b from-black via-gray-900 to-black">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-900/20 via-black to-black"></div>
          <motion.div
            animate={{
              scale: [1, 1.3, 1],
              rotate: [0, 180, 360],
              opacity: [0.3, 0.5, 0.3]
            }}
            transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
            className="absolute top-1/4 -right-1/4 w-[500px] h-[500px] bg-gradient-to-br from-amber-500/20 to-yellow-600/20 rounded-full blur-3xl"
          ></motion.div>
          <motion.div
            animate={{
              scale: [1.3, 1, 1.3],
              rotate: [360, 180, 0],
              opacity: [0.4, 0.6, 0.4]
            }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            className="absolute -bottom-1/4 -left-1/4 w-[500px] h-[500px] bg-gradient-to-tr from-yellow-500/20 to-amber-600/20 rounded-full blur-3xl"
          ></motion.div>
          {/* Additional ambient glow */}
          <div className="absolute inset-0 bg-gradient-to-t from-amber-950/10 via-transparent to-transparent"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 sm:pt-16 lg:pt-20 pb-16 sm:pb-24 lg:pb-32">
          <div className="grid lg:grid-cols-2 gap-8 sm:gap-12 items-center">
            {/* Left Content */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="space-y-6 sm:space-y-8"
            >
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="inline-block"
              >
                <span className="px-4 py-2 bg-gradient-to-r from-amber-500/20 to-yellow-500/20 border border-amber-500/30 rounded-full text-amber-400 text-sm font-medium backdrop-blur-sm">
                  ✨ New Collection 2025
                </span>
              </motion.div>

              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-tight"
              >
                <span className="bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 bg-clip-text text-transparent">
                  Every Second,
                </span>
                <br />
                <span className="text-white">Every Shine</span>
              </motion.h1>
              
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.45 }}
                className="text-xl sm:text-2xl lg:text-3xl font-semibold text-amber-200/80 italic"
              >
                Luxury Redefined
              </motion.p>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="text-base sm:text-lg lg:text-xl text-amber-100/80 leading-relaxed max-w-lg"
              >
                Discover exquisite timepieces and fine Watches built with high quality. Each piece tells a story of elegance, sophistication, and timeless beauty.
              </motion.p>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="flex flex-col sm:flex-row flex-wrap gap-3 sm:gap-4"
              >
                <button className="group px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-amber-400 to-yellow-600 text-black font-semibold rounded-lg hover:shadow-2xl hover:shadow-amber-500/50 transition-all duration-300 flex items-center justify-center gap-2">
                  Explore Collection
                  <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5 group-hover:translate-x-1 transition-transform" />
                </button>
              </motion.div>

              {/* Stats */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 }}
                className="grid grid-cols-3 gap-4 mt-2 sm:pt-6 sm:pt-8 border-t border-amber-500/20"
              >
                <div>
                  <h3 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent">20+</h3>
                  <p className="text-amber-200/60 text-xs sm:text-sm">Luxury Items</p>
                </div>
                <div>
                  <h3 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent">5+</h3>
                  <p className="text-amber-200/60 text-xs sm:text-sm">Elite Brands</p>
                </div>
                <div>
                  <h3 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent">100+</h3>
                  <p className="text-amber-200/60 text-xs sm:text-sm">Satisfied Clients</p>
                </div>
              </motion.div>
            </motion.div>

            {/* Right Content - Watch Display */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="relative mt-12 lg:mt-0"
            >
              {/* Main Watch Circle */}
              <div className="relative w-full aspect-square max-w-md lg:max-w-lg mx-auto">
                {/* Rotating Border */}
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  className="absolute inset-0 rounded-full bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 opacity-20 blur-xl"
                ></motion.div>

                {/* Inner Circle */}
                <div className="absolute inset-4 sm:inset-8 rounded-full bg-gradient-to-br from-gray-900 via-black to-gray-900 border-2 border-amber-500/40 flex items-center justify-center overflow-hidden shadow-2xl shadow-amber-500/20">
                  {/* Watch Icon/Image */}
                  <motion.div
                    animate={{ 
                      scale: [1, 1.08, 1],
                      rotate: [0, 5, 0, -5, 0]
                    }}
                    transition={{ duration: 5, repeat: Infinity }}
                    className="relative"
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-amber-400 to-yellow-600 blur-3xl opacity-40"></div>
                    <Watch className="w-32 h-32 sm:w-48 sm:h-48 lg:w-64 lg:h-64 text-amber-400 relative z-10 drop-shadow-2xl" strokeWidth={1.5} />
                  </motion.div>
                </div>

                {/* Floating Elements */}
                <motion.div
                  animate={{ y: [-10, 10, -10] }}
                  transition={{ duration: 3, repeat: Infinity }}
                  className="absolute top-4 right-4 sm:-top-4 sm:-right-4 lg:top-8 lg:-right-8 bg-gradient-to-br from-gray-900 to-black border border-amber-500/30 rounded-2xl p-3 sm:p-4 backdrop-blur-sm shadow-xl"
                >
                  <Star className="w-5 h-5 sm:w-6 sm:h-6 text-amber-400 mb-1 sm:mb-2" />
                  <p className="text-xs text-amber-100 font-semibold whitespace-nowrap">Premium</p>
                  <p className="text-xs text-amber-200/60 whitespace-nowrap">Quality</p>
                </motion.div>

                <motion.div
                  animate={{ y: [10, -10, 10] }}
                  transition={{ duration: 4, repeat: Infinity }}
                  className="absolute bottom-4 left-4 sm:-bottom-4 sm:-left-4 lg:bottom-8 lg:-left-8 bg-gradient-to-br from-gray-900 to-black border border-amber-500/30 rounded-2xl p-3 sm:p-4 backdrop-blur-sm shadow-xl"
                >
                  <Award className="w-5 h-5 sm:w-6 sm:h-6 text-amber-400 mb-1 sm:mb-2" />
                  <p className="text-xs text-amber-100 font-semibold whitespace-nowrap">Certified</p>
                  <p className="text-xs text-amber-200/60 whitespace-nowrap">Authentic</p>
                </motion.div>

                <motion.div
                  animate={{ x: [-10, 10, -10] }}
                  transition={{ duration: 3.5, repeat: Infinity }}
                  className="absolute top-1/2 -translate-y-1/2 right-4 sm:-right-4 lg:-right-12 bg-gradient-to-br from-gray-900 to-black border border-amber-500/30 rounded-2xl p-3 sm:p-4 backdrop-blur-sm shadow-xl"
                >
                  <Shield className="w-5 h-5 sm:w-6 sm:h-6 text-amber-400 mb-1 sm:mb-2" />
                  <p className="text-xs text-amber-100 font-semibold whitespace-nowrap">Warranty</p>
                  <p className="text-xs text-amber-200/60 whitespace-nowrap">Included</p>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="absolute bottom-4 sm:bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2"
        >
          <p className="text-amber-200/60 text-xs sm:text-sm">Scroll to explore</p>
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
            className="w-5 h-8 sm:w-6 sm:h-10 border-2 border-amber-500/30 rounded-full flex justify-center pt-1.5 sm:pt-2"
          >
            <div className="w-1 h-1.5 sm:h-2 bg-amber-400 rounded-full"></div>
          </motion.div>
        </motion.div>
      </section>
    </>
  );
}