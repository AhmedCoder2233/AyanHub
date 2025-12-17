import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Search, SlidersHorizontal, TrendingUp, Star } from "lucide-react";
import { motion } from "framer-motion";
import { supabase } from "./lib/supabaseClient";

export default function WatchesPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [hoveredCard, setHoveredCard] = useState(null);
  const [filters, setFilters] = useState({
    search: "",
    priceMin: 0,
    priceMax: Infinity,
    sortBy: "featured",
    trendingOnly: false,
  });

  const navigate = useNavigate();

  const priceRanges = [
    { label: "All Prices", min: 0, max: Infinity },
    { label: "Under PKR 3k", min: 0, max: 3000 },
    { label: "PKR 3k - PKR 10k", min: 3000, max: 10000 },
    { label: "PKR 10k - PKR 15k", min: 10000, max: 15000 },
    { label: "Above PKR 15k", min: 15000, max: Infinity },
  ];

  // Fetch watches only
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);

        const { data, error: fetchError } = await supabase
          .from("products")
          .select("*")
          .eq("product_type", "watch")
          .order("created_at", { ascending: false });

        if (fetchError) throw fetchError;
        setProducts(data || []);
      } catch (err) {
        console.error("Error fetching watches:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  // Filter & sort products
  const filteredProducts = products
    .filter((p) => {
      if (filters.search && !p.name.toLowerCase().includes(filters.search.toLowerCase())) return false;
      if (filters.trendingOnly && !p.is_trending) return false;
      if (p.price < filters.priceMin || p.price > filters.priceMax) return false;
      return true;
    })
    .sort((a, b) => {
      switch (filters.sortBy) {
        case "price-low":
          return a.price - b.price;
        case "price-high":
          return b.price - a.price;
        case "newest":
          return new Date(b.created_at) - new Date(a.created_at);
        default:
          return 0;
      }
    });

  return (
    <div className="bg-black min-h-screen">
      {/* Header */}
      <div className="relative z-10 border-b border-amber-500/20 bg-black/50 backdrop-blur-xl sticky top-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h1 className="text-3xl font-bold">
              <span className="bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 bg-clip-text text-transparent">
                Watches
              </span>
            </h1>
            <p className="text-amber-100/60 mt-1 text-sm sm:text-base">
              {filteredProducts.length} items available
            </p>
          </div>

          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-amber-400/60" />
              <input
                type="text"
                placeholder="Search watches..."
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                className="pl-10 pr-4 py-2 bg-black/50 border border-amber-500/30 rounded-lg text-white text-sm placeholder-amber-200/40 focus:outline-none focus:border-amber-500/60 transition-colors"
              />
            </div>

            <select
              value={filters.sortBy}
              onChange={(e) => setFilters({ ...filters, sortBy: e.target.value })}
              className="px-3 py-2 bg-black/50 border border-amber-500/30 rounded-lg text-amber-100 text-sm focus:outline-none focus:border-amber-500/60 transition-colors cursor-pointer"
            >
              <option value="featured">Featured</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="newest">Newest First</option>
            </select>

            <label className="flex items-center gap-2 text-amber-100 text-sm">
              <input
                type="checkbox"
                checked={filters.trendingOnly}
                onChange={() => setFilters(prev => ({ ...prev, trendingOnly: !prev.trendingOnly }))}
                className="w-4 h-4 accent-amber-500"
              />
              Trending Only
            </label>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <div className="col-span-full flex justify-center items-center py-20">
            <div className="w-12 h-12 border-4 border-amber-500/20 border-t-amber-500 rounded-full animate-spin"></div>
          </div>
        ) : error ? (
          <p className="col-span-full text-center text-red-400">{error}</p>
        ) : filteredProducts.length === 0 ? (
          <p className="col-span-full text-center text-amber-100/60">No watches found</p>
        ) : (
          filteredProducts.map((product) => (
            <motion.div
              key={product.id}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              onHoverStart={() => setHoveredCard(product.id)}
              onHoverEnd={() => setHoveredCard(null)}
              className="group relative bg-gradient-to-br from-gray-900 via-black to-gray-900 rounded-xl overflow-hidden border border-amber-500/20 hover:border-amber-500/50 transition-all duration-500"
            >
              {/* Trending Badge */}
              {product.is_trending && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute top-3 left-3 z-20 px-2.5 py-1 bg-gradient-to-r from-amber-500 to-yellow-600 rounded-full flex items-center gap-1 shadow-lg"
                >
                  <TrendingUp className="w-3 h-3 text-black" />
                  <span className="text-xs font-bold text-black">Trending</span>
                </motion.div>
              )}

              {/* Image */}
              <div className="relative h-56 overflow-hidden flex items-center justify-center bg-gradient-to-br from-amber-950/10 to-black">
                <motion.img
                  src={product.image_url}
                  alt={product.name}
                  className="h-full object-contain transition-transform duration-500 group-hover:scale-110"
                />
              </div>

              {/* Info */}
              <div className="p-4 space-y-2">
                <h3 className="text-lg font-bold text-white group-hover:text-amber-400 transition-colors line-clamp-1">
                  {product.name}
                </h3>
                <p className="text-xs text-amber-100/60 line-clamp-2">
                  {product.description.slice(0, 50)}{product.description.length > 50 && "..."}
                </p>
                {product.rating && (
                  <div className="flex items-center gap-1">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-3 h-3 ${i < product.rating ? "fill-amber-400 text-amber-400" : "text-amber-400/20"}`}
                      />
                    ))}
                  </div>
                )}
                <p className="text-xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent">
                  PKR {product.price}
                </p>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate(`/product/${product.slug}`)}
                  className="w-full py-2 bg-gradient-to-r from-amber-400 to-yellow-600 text-black font-semibold rounded-lg hover:shadow-lg hover:shadow-amber-500/30 transition-all"
                >
                  View Details
                </motion.button>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}
