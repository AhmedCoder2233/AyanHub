// src/components/WatchHeader.jsx
import React, { useState, useEffect } from 'react';
import { Watch, ShoppingCart, User, Menu, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router';
import { supabase } from '../lib/supabaseClient';

export default function WatchHeader() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const [session, setSession] = useState(null);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [isSignup, setIsSignup] = useState(false);
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authMessage, setAuthMessage] = useState('');
  const [loadingAuth, setLoadingAuth] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    supabase.auth.getSession().then(res => {
      if (res?.data?.session) setSession(res.data.session);
    });
    const { data: listener } = supabase.auth.onAuthStateChange((_event, newSession) => {
      setSession(newSession);
    });
    return () => listener?.subscription?.unsubscribe?.();
  }, []);

  const navItems = [
    { name: 'Home', route: "/"},
    { name: 'Watches', route: '/watches' },
    { name: 'Contact Us', route: '/contact' },
  ];

  const handleSignUp = async (e) => {
    e.preventDefault();
    setLoadingAuth(true); setAuthMessage('');
    try {
      const { error } = await supabase.auth.signUp({ email: authEmail, password: authPassword });
      if (error) throw error;
      setAuthMessage('Check your email for confirmation link.');
      setAuthEmail(''); setAuthPassword('');
    } catch (err) {
      setAuthMessage(err.message || 'Error signing up');
    } finally { setLoadingAuth(false); }
  };

  const handleSignIn = async (e) => {
    e.preventDefault();
    setLoadingAuth(true); setAuthMessage('');
    try {
      const { error } = await supabase.auth.signInWithPassword({ email: authEmail, password: authPassword });
      if (error) throw error;
      setAuthMessage('Signed in successfully.'); setAuthModalOpen(false);
      setAuthEmail(''); setAuthPassword('');
    } catch (err) {
      setAuthMessage(err.message || 'Error signing in');
    } finally { setLoadingAuth(false); }
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    setSession(null);
  };

  const openAuthModalFor = (signup = false) => {
    setIsSignup(signup); setAuthModalOpen(true); setAuthMessage('');
  };

  return (
    <>
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className={`left-0 right-0 z-50 transition-all duration-300 ${
          isScrolled ? 'bg-black/95 backdrop-blur-md shadow-2xl shadow-amber-900/20' : 'bg-black'
        }`}
      >
        {/* Main Navigation */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">

            {/* Logo */}
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="flex items-center gap-3 cursor-pointer group"
              onClick={() => navigate("/")}
            >
              <div className="relative w-12 h-12 flex items-center justify-center">
                <div className="absolute inset-0 bg-gradient-to-r from-amber-400 to-yellow-600 blur-lg opacity-50 group-hover:opacity-75 transition-opacity"></div>
                <img src="/logo.jpeg" alt="Ayan Logo" className="w-12 h-12 object-contain rounded-full" />
              </div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 bg-clip-text text-transparent">Ayan</h1>
                <p className="text-[10px] text-amber-200/60 tracking-widest">Watches Hub</p>
              </div>
            </motion.div>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex items-center gap-8">
              {navItems.map((item) => (
                <button
                  key={item.name}
                  onClick={() => navigate(item.route)}
                  className="text-amber-100 hover:text-amber-400 transition-colors font-medium text-sm uppercase tracking-wide"
                >
                  {item.name}
                </button>
              ))}
            </nav>

            {/* Right Icons */}
            <div className="flex items-center gap-4 sm:gap-6">
              {!session?.user ? (
                <>
                  <button onClick={() => openAuthModalFor(false)} className="text-amber-100 hover:text-amber-400 flex items-center gap-2">
                    <User className="w-5 h-5 sm:w-6 sm:h-6" /> <span className="hidden sm:inline">Sign In</span>
                  </button>
                  <button onClick={() => openAuthModalFor(true)} className="bg-amber-400 text-black px-3 py-1 rounded-md font-medium hover:brightness-95 transition">Sign Up</button>
                </>
              ) : (
                <div className="flex items-center gap-3 text-amber-100">
                  <div className="text-sm hidden sm:block">{session.user.email}</div>
                  <button onClick={handleSignOut} className="px-3 py-1 bg-amber-600/80 rounded hover:bg-amber-600 transition">Sign Out</button>
                </div>
              )}

              <button onClick={() => navigate("/cart")}><ShoppingCart className="w-6 h-6 text-amber-400" /></button>

              <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="lg:hidden text-amber-100 hover:text-amber-400 transition-colors">
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="lg:hidden border-t border-amber-500/20 bg-black">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 space-y-2">
                <div className="mb-4 pb-4 border-b border-amber-500/20">
                  <input type="text" placeholder="Search watches..." className="w-full pl-10 pr-4 py-2 bg-black/50 border border-amber-500/30 rounded-lg text-amber-100 placeholder-amber-200/40 focus:outline-none focus:border-amber-400" />
                </div>
                {navItems.map((item) => (
                  <button key={item.name} onClick={() => navigate(item.route)} className="block w-full text-left py-3 text-amber-100 hover:text-amber-400 transition-colors font-medium uppercase tracking-wide border-b border-amber-500/10 last:border-0">
                    {item.name}
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.header>

      {/* Auth Modal */}
      <AnimatePresence>
        {authModalOpen && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: 20, opacity: 0 }} className="w-full max-w-md bg-gray-900 rounded-xl p-6 border border-amber-500/20 shadow-2xl">
              <h3 className="text-xl font-semibold text-amber-100 mb-2">{isSignup ? 'Create an account' : 'Sign in'}</h3>
              <form onSubmit={isSignup ? handleSignUp : handleSignIn} className="space-y-3">
                <div>
                  <label className="text-sm text-amber-200 block mb-1">Email</label>
                  <input type="email" required value={authEmail} onChange={(e) => setAuthEmail(e.target.value)} className="w-full px-3 py-2 bg-black/40 border border-amber-500/20 rounded text-amber-100 focus:outline-none"/>
                </div>
                <div>
                  <label className="text-sm text-amber-200 block mb-1">Password</label>
                  <input type="password" required minLength={6} value={authPassword} onChange={(e) => setAuthPassword(e.target.value)} className="w-full px-3 py-2 bg-black/40 border border-amber-500/20 rounded text-amber-100 focus:outline-none"/>
                </div>
                {authMessage && <div className="text-sm text-amber-300">{authMessage}</div>}
                <div className="flex items-center justify-between gap-3 mt-2">
                  <button type="submit" disabled={loadingAuth} className="px-4 py-2 bg-amber-400 text-black rounded font-medium">{loadingAuth ? 'Please wait...' : (isSignup ? 'Sign up' : 'Sign in')}</button>
                  <button type="button" onClick={() => {setIsSignup(!isSignup); setAuthMessage('')}} className="text-sm text-amber-300 underline">{isSignup ? 'Have an account? Sign in' : "Don't have an account? Sign up"}</button>
                  <button type="button" onClick={() => setAuthModalOpen(false)} className="text-sm text-amber-300">Close</button>
                </div>
                <div className="mt-4 text-xs text-amber-400/60">Note: Confirm your email after signing up.</div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
