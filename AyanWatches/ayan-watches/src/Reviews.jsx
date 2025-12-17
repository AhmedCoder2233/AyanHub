import { motion } from "framer-motion";

const testimonials = [
  {
    id: 1,
    name: "Imran Hashmi",
    role: "CEO, LuxTime",
    message: "The watches are absolutely exquisite. The quality and attention to detail are unmatched.",
  },
  {
    id: 2,
    name: "Kamran Ghulam",
    role: "Entrepreneur",
    message: "I purchased a business watch and a bracelet; both are stunning. Highly recommend this collection!",
  },
  {
    id: 3,
    name: "Waseem Yaqoob",
    role: "Designer",
    message: "Elegant, stylish, and premium. Every piece feels like a masterpiece.",
  },
];

export default function TestimonialsSection() {
  return (
    <section className="relative z-10 bg-black text-white w-full py-20 overflow-hidden">
      {/* Subtle Background Glow */}
      <motion.div
        animate={{ scale: [1, 1.2, 1], opacity: [0.05, 0.1, 0.05] }}
        transition={{ duration: 12, repeat: Infinity }}
        className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-br from-yellow-400 via-amber-500 to-yellow-400 rounded-full blur-3xl opacity-20"
      ></motion.div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold">
            <span className="bg-gradient-to-r from-yellow-400 via-amber-500 to-yellow-500 bg-clip-text text-transparent">
              Testimonials
            </span>
          </h2>
          <p className="text-amber-200/70 mt-2">
            What our clients are saying about our watches.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((t, index) => (
            <motion.div
              key={t.id}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              className="bg-gray-900/30 border border-amber-500/20 rounded-xl p-6 flex flex-col justify-between shadow-lg hover:shadow-amber-500/40 transition-all"
            >
              <p className="text-amber-100/80 mb-4 text-sm">{`"${t.message}"`}</p>
              <div className="mt-auto">
                <h4 className="text-lg font-semibold text-amber-400">{t.name}</h4>
                <p className="text-amber-200/70 text-sm">{t.role}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
