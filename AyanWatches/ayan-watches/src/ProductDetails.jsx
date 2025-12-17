
import { ChevronLeft, Loader, RefreshCcw, Shield, ShoppingCart, Star, Truck } from 'lucide-react';
import { useEffect, useState } from 'react';
import {  useNavigate, useParams } from 'react-router-dom';
import { supabase } from './lib/supabaseClient';
import {AnimatePresence, motion} from 'framer-motion'
// Product Details Page
export default function ProductDetailsPage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [isLiked, setIsLiked] = useState(false);
  const [addingToCart, setAddingToCart] = useState(false);
  const [cartMessage, setCartMessage] = useState('');
  const [session, setSession] = useState(null);
  const [showAuthPrompt, setShowAuthPrompt] = useState(false);

  useEffect(() => {
    supabase.auth.getSession().then(res => {
      if (res?.data?.session) setSession(res.data.session);
    });

    const { data: listener } = supabase.auth.onAuthStateChange((_event, newSession) => {
      setSession(newSession);
    });

    return () => listener?.subscription?.unsubscribe?.();
  }, []);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const { data, error: fetchError } = await supabase
          .from('products')
          .select('*')
          .eq('slug', slug)
          .single();
        
        if (fetchError) throw fetchError;
        setProduct(data);
        
      } catch (err) {
        console.error('Error fetching product:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (slug) fetchProduct();
  }, [slug]);

const handleAddToCart = () => {
  if (!session) {
    setCartMessage("Please sign in to add items to your cart!");
    setShowAuthPrompt(true);
    return;
  }

  setAddingToCart(true);

  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const existing = cart.find((item) => item.id === product.id);

  if (existing) {
    existing.quantity += quantity;
  } else {
    cart.push({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image_url,
      quantity,
    });
  }

  localStorage.setItem("cart", JSON.stringify(cart));

  setCartMessage("Added to cart successfully! ✓");
  setTimeout(() => setCartMessage(""), 3000);
  setAddingToCart(false);
};

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <Loader className="w-12 h-12 text-amber-400 animate-spin" />
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <p className="text-2xl text-red-400">Product not found</p>
          <p className="text-amber-100/60 mt-2">{error}</p>
          <button
            onClick={() => navigate('/products')}
            className="mt-4 px-6 py-2.5 bg-amber-500 text-black font-semibold rounded-lg"
          >
            Go Back to Products
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      <div className="fixed inset-0 pointer-events-none">
        <motion.div
          animate={{ scale: [1, 1.2, 1], opacity: [0.05, 0.1, 0.05] }}
          transition={{ duration: 10, repeat: Infinity }}
          className="absolute top-0 left-1/4 w-96 h-96 bg-amber-500 rounded-full blur-3xl"
        />
        <motion.div
          animate={{ scale: [1.2, 1, 1.2], opacity: [0.05, 0.1, 0.05] }}
          transition={{ duration: 12, repeat: Infinity }}
          className="absolute bottom-0 right-1/4 w-96 h-96 bg-yellow-500 rounded-full blur-3xl"
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-amber-400 hover:text-amber-300 mb-6 transition-colors"
        >
          <ChevronLeft className="w-5 h-5" />
          <span>Back to Products</span>
        </button>

        <div className="grid lg:grid-cols-2 gap-8 lg:gap-12">
          <div className="space-y-4">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              className="relative bg-gradient-to-br from-gray-900 via-black to-gray-900 rounded-2xl overflow-hidden border border-amber-500/20 aspect-square"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-amber-400/10 to-yellow-600/10 blur-3xl" />
              <img
                src={product.image_url}
                alt={product.name}
                className="w-full h-full object-cover relative z-10"
              />
              
              {product.is_trending && (
                <div className="absolute top-4 right-4 px-4 py-2 bg-gradient-to-r from-amber-500 to-yellow-600 rounded-full flex items-center gap-2 shadow-lg z-20">
                  <Star className="w-4 h-4 text-black fill-black" />
                  <span className="text-sm font-bold text-black">Trending</span>
                </div>
              )}
            </motion.div>
          </div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <div>
              <span className="inline-block px-3 py-1 bg-amber-500/10 border border-amber-500/30 rounded-full text-amber-400 text-sm font-medium mb-3">
              'Luxury Watch'
              </span>
              
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4">
                {product.name}
              </h1>

              {product.rating && (
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex gap-1">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-5 h-5 ${
                          i < product.rating
                            ? 'fill-amber-400 text-amber-400'
                            : 'text-amber-400/20'
                        }`}
                      />
                    ))}
                  </div>
                  <span className="text-amber-200/60">
                    {product.rating}.0 ({product.reviews || 0} reviews)
                  </span>
                </div>
              )}

              <p className="text-amber-100/70 text-lg leading-relaxed">
                {product.description}
              </p>
            </div>

            <div className="py-6 border-y border-amber-500/20">
              <p className="text-sm text-amber-200/60 mb-1">Price</p>
              <p className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent">
                PKR {product.price?.toLocaleString()}
              </p>
            </div>

            <div className="flex items-center gap-4">
              <span className="text-amber-100 font-medium">Quantity:</span>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="w-10 h-10 bg-amber-500/10 border border-amber-500/30 rounded-lg flex items-center justify-center hover:bg-amber-500/20 transition-colors"
                >
                  <span className="text-amber-400 text-xl">−</span>
                </button>
                <span className="text-white text-xl font-semibold w-12 text-center">
                  {quantity}
                </span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="w-10 h-10 bg-amber-500/10 border border-amber-500/30 rounded-lg flex items-center justify-center hover:bg-amber-500/20 transition-colors"
                >
                  <span className="text-amber-400 text-xl">+</span>
                </button>
              </div>
            </div>

            <AnimatePresence>
              {cartMessage && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className={`p-3 rounded-lg ${
                    cartMessage.includes('successfully')
                      ? 'bg-green-500/10 border border-green-500/30 text-green-400'
                      : 'bg-red-500/10 border border-red-500/30 text-red-400'
                  }`}
                >
                  {cartMessage}
                </motion.div>
              )}
            </AnimatePresence>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleAddToCart}
              disabled={addingToCart}
              className="w-full py-4 bg-gradient-to-r from-amber-400 to-yellow-600 text-black text-lg font-bold rounded-xl hover:shadow-2xl hover:shadow-amber-500/30 transition-all duration-300 flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {addingToCart ? (
                <Loader className="w-6 h-6 animate-spin" />
              ) : (
                <>
                  <ShoppingCart className="w-6 h-6" />
                  Add to Cart
                </>
              )}
            </motion.button>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6">
              {[
                { icon: Truck, text: '250 Shipping' },
                { icon: Shield, text: 'Cash On Delivery' },
                { icon: RefreshCcw, text: 'Quality Products' },
              ].map((feature, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 p-4 bg-amber-500/5 border border-amber-500/20 rounded-xl"
                >
                  <feature.icon className="w-5 h-5 text-amber-400" />
                  <span className="text-amber-100/80 text-sm">{feature.text}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      <AnimatePresence>
        {showAuthPrompt && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4"
            onClick={() => setShowAuthPrompt(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-gradient-to-br from-gray-900 via-black to-gray-900 border border-amber-500/30 rounded-2xl p-8 max-w-md w-full"
            >
              <div className="text-center">
                <div className="w-16 h-16 bg-amber-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <ShoppingCart className="w-8 h-8 text-amber-400" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">
                  Sign In Required
                </h3>
                <p className="text-amber-100/60 mb-6">
                  Please sign in or create an account to add items to your cart
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={() => setShowAuthPrompt(false)}
                    className="flex-1 py-3 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-400 font-semibold hover:bg-amber-500/20 transition-all"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => {
                      setShowAuthPrompt(false);
                      navigate('/');
                    }}
                    className="flex-1 py-3 bg-gradient-to-r from-amber-400 to-yellow-600 text-black font-bold rounded-lg hover:shadow-lg transition-all"
                  >
                    Sign In
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}