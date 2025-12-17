
// // App.jsx - Main routing setup
// import { BrowserRouter as useNavigate } from 'react-router-dom';
// import { useState, useEffect } from 'react';
// import { motion, AnimatePresence } from 'framer-motion';
// import { 
//   ShoppingCart, Heart, Star, ChevronLeft, Search, SlidersHorizontal, 
//   TrendingUp, Truck, Shield, RefreshCcw, Loader
// } from 'lucide-react';
// import { supabase } from './lib/supabaseClient';

// // Products Listing Page
// function ProductsPage() {
//   const navigate = useNavigate();
//   const [products, setProducts] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);
//   const [hoveredCard, setHoveredCard] = useState(null);
//   const [filters, setFilters] = useState({
//     search: '',
//     type: 'all',
//     priceMin: 0,
//     priceMax: Infinity,
//     sortBy: 'featured'
//   });
  

//   const priceRanges = [
//     { label: 'All Prices', min: 0, max: Infinity },
//     { label: 'Under PKR 3k', min: 0, max: 3000 },
//     { label: 'PKR 5k - PKR 10k', min: 5000, max: 10000 },
//     { label: 'PKR 10k - PKR 15k', min: 10000, max: 15000 },
//     { label: 'Above PKR 15k', min: 15000, max: Infinity },
//   ];

//   useEffect(() => {
//     const fetchProducts = async () => {
//       try {
//         setLoading(true);
//         setError(null);
        
//         const { data, error: fetchError } = await supabase
//           .from('products')
//           .select('*')
//           .order('created_at', { ascending: false });
        
//         if (fetchError) throw fetchError;
//         setProducts(data || []);
//       } catch (err) {
//         console.error('Error fetching products:', err);
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchProducts();
//   }, []);

//   const filteredProducts = products
//     .filter(p => {
//       if (filters.search && !p.name.toLowerCase().includes(filters.search.toLowerCase())) {
//         return false;
//       }
//       if (filters.type !== 'all' && p.product_type !== filters.type) {
//         return false;
//       }
//       if (p.price < filters.priceMin || p.price > filters.priceMax) {
//         return false;
//       }
//       return true;
//     })
//     .sort((a, b) => {
//       switch (filters.sortBy) {
//         case 'price-low':
//           return a.price - b.price;
//         case 'price-high':
//           return b.price - a.price;
//         case 'rating':
//           return (b.rating || 0) - (a.rating || 0);
//         case 'newest':
//           return new Date(b.created_at) - new Date(a.created_at);
//         default:
//           return 0;
//       }
//     });

//   return (
//     <div className="bg-black min-h-screen">
//       {/* Background Effects */}
//       <div className="fixed inset-0 pointer-events-none">
//         <motion.div
//           animate={{ scale: [1, 1.2, 1], opacity: [0.05, 0.1, 0.05] }}
//           transition={{ duration: 10, repeat: Infinity }}
//           className="absolute top-0 left-1/4 w-96 h-96 bg-amber-500 rounded-full blur-3xl"
//         />
//         <motion.div
//           animate={{ scale: [1.2, 1, 1.2], opacity: [0.05, 0.1, 0.05] }}
//           transition={{ duration: 12, repeat: Infinity }}
//           className="absolute bottom-0 right-1/4 w-96 h-96 bg-yellow-500 rounded-full blur-3xl"
//         />
//       </div>

//       {/* Header */}
//       <div className="relative z-10 border-b border-amber-500/20 bg-black/50 backdrop-blur-xl sticky top-0">
//         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
//           <div className="flex flex-col gap-3">
//             <div className="flex items-center justify-between">
//               <div>
//                 <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold">
//                   <span className="bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 bg-clip-text text-transparent">
//                     Trending
//                   </span>
//                   <span className="text-white"> Products</span>
//                 </h1>
//                 <p className="text-amber-100/60 mt-1 text-sm sm:text-base">
//                   Discover {filteredProducts.length} luxury items
//                 </p>
//               </div>
//             </div>

//             <div className="flex flex-col sm:flex-row gap-2 lg:hidden">
//               <div className="relative flex-1">
//                 <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-amber-400/60" />
//                 <input
//                   type="text"
//                   placeholder="Search products..."
//                   value={filters.search}
//                   onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
//                   className="w-full pl-10 pr-4 py-2 bg-black/50 border border-amber-500/30 rounded-lg text-white text-sm placeholder-amber-200/40 focus:outline-none focus:border-amber-500/60 transition-colors"
//                 />
//               </div>
//               <select
//                 value={filters.sortBy}
//                 onChange={(e) => setFilters(prev => ({ ...prev, sortBy: e.target.value }))}
//                 className="px-3 py-2 bg-black/50 border border-amber-500/30 rounded-lg text-amber-100 text-sm focus:outline-none focus:border-amber-500/60 transition-colors cursor-pointer"
//               >
//                 <option value="featured">Featured</option>
//                 <option value="price-low">Price: Low to High</option>
//                 <option value="price-high">Price: High to Low</option>
//                 <option value="rating">Highest Rated</option>
//                 <option value="newest">Newest First</option>
//               </select>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Main Content */}
//       <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
//         <div className="flex gap-6 lg:gap-8">
//           {/* Desktop Filter Sidebar */}
//           <div className="hidden lg:block w-80 shrink-0">
//             <div className="sticky top-24 bg-gradient-to-br from-gray-900 via-black to-gray-900 border rounded-2xl border-amber-500/20 p-6 space-y-6">
//               <div>
//                 <h3 className="text-xl font-bold text-white flex items-center gap-2">
//                   <SlidersHorizontal className="w-5 h-5 text-amber-400" />
//                   Filters
//                 </h3>
//                 <p className="text-sm text-amber-200/60 mt-1">Refine your search</p>
//               </div>

//               <div className="relative">
//                 <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-amber-400/60" />
//                 <input
//                   type="text"
//                   placeholder="Search products..."
//                   value={filters.search}
//                   onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
//                   className="w-full pl-10 pr-4 py-2.5 bg-black/50 border border-amber-500/30 rounded-lg text-white placeholder-amber-200/40 focus:outline-none focus:border-amber-500/60 transition-colors"
//                 />
//               </div>

//               <div>
//                 <h4 className="text-sm font-semibold text-amber-400 mb-3">Product Type</h4>
//                 <div className="space-y-2">
//                   {['all', 'watch', 'jewelry'].map((type) => (
//                     <label key={type} className="flex items-center gap-3 cursor-pointer group">
//                       <div className="relative">
//                         <input
//                           type="radio"
//                           name="type"
//                           checked={filters.type === type}
//                           onChange={() => setFilters(prev => ({ ...prev, type }))}
//                           className="sr-only"
//                         />
//                         <div className={`w-5 h-5 rounded-full border-2 transition-all ${
//                           filters.type === type
//                             ? 'border-amber-500 bg-amber-500'
//                             : 'border-amber-500/30 group-hover:border-amber-500/60'
//                         }`}>
//                           {filters.type === type && (
//                             <motion.div
//                               initial={{ scale: 0 }}
//                               animate={{ scale: 1 }}
//                               className="w-2 h-2 bg-black rounded-full m-auto mt-0.5"
//                             />
//                           )}
//                         </div>
//                       </div>
//                       <span className="text-amber-100/80 group-hover:text-amber-100 transition-colors capitalize">
//                         {type === 'all' ? 'All Products' : type === 'watch' ? 'Watches' : 'Jewelry'}
//                       </span>
//                     </label>
//                   ))}
//                 </div>
//               </div>

//               <div>
//                 <h4 className="text-sm font-semibold text-amber-400 mb-3">Price Range</h4>
//                 <div className="space-y-2">
//                   {priceRanges.map((range) => (
//                     <label key={range.label} className="flex items-center gap-3 cursor-pointer group">
//                       <div className="relative">
//                         <input
//                           type="radio"
//                           name="price"
//                           checked={filters.priceMin === range.min && filters.priceMax === range.max}
//                           onChange={() => setFilters(prev => ({
//                             ...prev,
//                             priceMin: range.min,
//                             priceMax: range.max
//                           }))}
//                           className="sr-only"
//                         />
//                         <div className={`w-5 h-5 rounded-full border-2 transition-all ${
//                           filters.priceMin === range.min && filters.priceMax === range.max
//                             ? 'border-amber-500 bg-amber-500'
//                             : 'border-amber-500/30 group-hover:border-amber-500/60'
//                         }`}>
//                           {filters.priceMin === range.min && filters.priceMax === range.max && (
//                             <motion.div
//                               initial={{ scale: 0 }}
//                               animate={{ scale: 1 }}
//                               className="w-2 h-2 bg-black rounded-full m-auto mt-0.5"
//                             />
//                           )}
//                         </div>
//                       </div>
//                       <span className="text-amber-100/80 group-hover:text-amber-100 transition-colors text-sm">
//                         {range.label}
//                       </span>
//                     </label>
//                   ))}
//                 </div>
//               </div>

//               <div>
//                 <h4 className="text-sm font-semibold text-amber-400 mb-3">Sort By</h4>
//                 <select
//                   value={filters.sortBy}
//                   onChange={(e) => setFilters(prev => ({ ...prev, sortBy: e.target.value }))}
//                   className="w-full px-4 py-2.5 bg-black/50 border border-amber-500/30 rounded-lg text-amber-100 focus:outline-none focus:border-amber-500/60 transition-colors cursor-pointer"
//                 >
//                   <option value="featured">Featured</option>
//                   <option value="price-low">Price: Low to High</option>
//                   <option value="price-high">Price: High to Low</option>
//                   <option value="rating">Highest Rated</option>
//                   <option value="newest">Newest First</option>
//                 </select>
//               </div>

//               <button
//                 onClick={() => setFilters({
//                   search: '',
//                   type: 'all',
//                   priceMin: 0,
//                   priceMax: Infinity,
//                   sortBy: 'featured'
//                 })}
//                 className="w-full py-2.5 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-400 font-semibold hover:bg-amber-500/20 transition-all"
//               >
//                 Reset Filters
//               </button>
//             </div>
//           </div>

//           {/* Products Grid */}
//           <div className="flex-1 min-w-0">
//             {loading ? (
//               <div className="flex justify-center items-center py-20">
//                 <div className="w-12 h-12 border-4 border-amber-500/20 border-t-amber-500 rounded-full animate-spin"></div>
//               </div>
//             ) : error ? (
//               <div className="text-center py-20">
//                 <p className="text-xl sm:text-2xl text-red-400">Error loading products</p>
//                 <p className="text-amber-100/40 mt-2">{error}</p>
//                 <button
//                   onClick={() => window.location.reload()}
//                   className="mt-4 px-6 py-2.5 bg-amber-500 text-black font-semibold rounded-lg hover:bg-amber-400 transition-all"
//                 >
//                   Retry
//                 </button>
//               </div>
//             ) : filteredProducts.length === 0 ? (
//               <div className="text-center py-20">
//                 <p className="text-xl sm:text-2xl text-amber-100/60">No products found</p>
//                 <p className="text-amber-100/40 mt-2">Try adjusting your filters</p>
//               </div>
//             ) : (
//               <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
//                 {filteredProducts.map((product, index) => (
//                   <motion.div
//                     key={product.id}
//                     initial={{ opacity: 0, y: 50 }}
//                     animate={{ opacity: 1, y: 0 }}
//                     transition={{ duration: 0.5, delay: index * 0.05 }}
//                     onHoverStart={() => setHoveredCard(product.id)}
//                     onHoverEnd={() => setHoveredCard(null)}
//                     className="group relative"
//                   >
//                     <div className="relative bg-gradient-to-br from-gray-900 via-black to-gray-900 rounded-xl sm:rounded-2xl overflow-hidden border border-amber-500/20 hover:border-amber-500/50 transition-all duration-500 h-full">
//                       {product.is_trending && (
//                         <motion.div
//                           initial={{ scale: 0 }}
//                           animate={{ scale: 1 }}
//                           className="absolute top-3 left-3 z-20 px-2.5 py-1 sm:px-3 sm:py-1.5 bg-gradient-to-r from-amber-500 to-yellow-600 rounded-full flex items-center gap-1 sm:gap-1.5 shadow-lg"
//                         >
//                           <TrendingUp className="w-3 h-3 text-black" />
//                           <span className="text-xs font-bold text-black">Trending</span>
//                         </motion.div>
//                       )}

//                       <div className="relative h-48 sm:h-64 overflow-hidden bg-gradient-to-br from-amber-950/10 to-black">
//                         <motion.div
//                           animate={{
//                             scale: hoveredCard === product.id ? 1.5 : 1,
//                             opacity: hoveredCard === product.id ? 0.3 : 0.1,
//                           }}
//                           transition={{ duration: 0.5 }}
//                           className="absolute inset-0 bg-gradient-to-r from-amber-400 to-yellow-600 blur-3xl"
//                         />
                        
//                         <div className="relative h-full flex items-center justify-center">
//                           <img 
//                             src={product.image_url} 
//                             alt={product.name}
//                             className="w-full h-full object-cover"
//                           />
//                         </div>
//                       </div>

//                       <div className="p-4 sm:p-5 space-y-2 sm:space-y-3">
//                         <span className="inline-block px-2.5 py-0.5 sm:px-3 sm:py-1 bg-amber-500/10 border border-amber-500/30 rounded-full text-amber-400 text-xs font-medium">
//                           {product.product_type === 'watch' ? 'Watch' : 'Jewelry'}
//                         </span>

//                         <h3 className="text-lg sm:text-xl font-bold text-white group-hover:text-amber-400 transition-colors duration-300 line-clamp-1">
//                           {product.name}
//                         </h3>

//                         <p className="text-xs sm:text-sm text-amber-100/60 line-clamp-2">
//                           {product.description}
//                         </p>

//                         {product.rating && (
//                           <div className="flex items-center gap-2">
//                             <div className="flex gap-0.5">
//                               {[...Array(5)].map((_, i) => (
//                                 <Star
//                                   key={i}
//                                   className={`w-3 h-3 sm:w-4 sm:h-4 ${
//                                     i < product.rating
//                                       ? 'fill-amber-400 text-amber-400'
//                                       : 'text-amber-400/20'
//                                   }`}
//                                 />
//                               ))}
//                             </div>
//                             {product.reviews && (
//                               <span className="text-xs sm:text-sm text-amber-200/60">
//                                 ({product.reviews})
//                               </span>
//                             )}
//                           </div>
//                         )}

//                         <div className="flex items-center justify-between pt-2 sm:pt-3 border-t border-amber-500/20">
//                           <div>
//                             <p className="text-xs text-amber-200/60">Price</p>
//                             <p className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent">
//                               PKR {product.price}
//                             </p>
//                           </div>
//                           <motion.button
//                             whileHover={{ scale: 1.05 }}
//                             whileTap={{ scale: 0.95 }}
//                             onClick={() => navigate(`/product/${product.slug}`)}
//                             className="px-3 py-1.5 sm:px-5 sm:py-2.5 bg-gradient-to-r from-amber-400 to-yellow-600 text-black text-sm font-semibold rounded-lg hover:shadow-lg hover:shadow-amber-500/30 transition-all duration-300"
//                           >
//                             View Details
//                           </motion.button>
//                         </div>
//                       </div>
//                     </div>
//                   </motion.div>
//                 ))}
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }