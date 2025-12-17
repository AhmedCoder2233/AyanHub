// src/pages/ContactUs.jsx
import { motion } from "framer-motion";
import { Facebook, Phone } from "lucide-react";

export default function ContactUs() {
  return (
    <div className="bg-black min-h-screen flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 bg-clip-text text-transparent"
      >
        Contact Us
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.6 }}
        className="text-amber-100/60 mt-4 text-lg sm:text-xl"
      >
        We’d love to hear from you! Reach out via social media or call us directly.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="mt-10 flex flex-col sm:flex-row items-center gap-8"
      >
        {/* Phone */}
        <div className="flex items-center gap-3 bg-gray-900/50 border border-amber-500/30 rounded-xl px-6 py-4 hover:bg-gray-900/70 transition cursor-pointer">
          <Phone className="w-6 h-6 text-amber-400" />
          <span className="text-amber-100 font-medium text-lg">0306 5659811</span>
        </div>

        {/* Facebook */}
        <a
          href="https://www.facebook.com/profile.php?id=61584181445485" // replace with actual Facebook link
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-3 bg-gray-900/50 border border-amber-500/30 rounded-xl px-6 py-4 hover:bg-gray-900/70 transition"
        >
          <Facebook className="w-6 h-6 text-amber-400" />
          <span className="text-amber-100 font-medium text-lg">Facebook</span>
        </a>
      </motion.div>
    </div>
  );
}
