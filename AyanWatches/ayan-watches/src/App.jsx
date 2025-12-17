import { useEffect, useState } from "react";
import { LoadingAnimation } from "./components/Animation";
import WatchHeader from "./components/Header";
import  HeroSection  from "./Hero";
import { AnimatePresence } from "framer-motion";
import ProductsPage from "./TrendingProducts";
import TestimonialsSection from "./Reviews";
import Footer from "./components/Footer";
import ProductDetailsPage from "./ProductDetails";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CartPage from "./Cart";
import Checkout from "./Checkout";
import WatchesPage from "./Watches";
import ContactUs from "./ContactUs";

export default function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    document.documentElement.style.scrollBehavior = "smooth";
    return () => {
      document.documentElement.style.scrollBehavior = "auto";
    };
  }, []);

  return (
    <>
      <AnimatePresence>
        {isLoading && <LoadingAnimation onComplete={() => setIsLoading(false)} />}
      </AnimatePresence>

      {!isLoading && (
        <Router>
          <WatchHeader />

          <Routes>
            {/* HOME PAGE */}
            <Route
              path="/checkout"
              element={
                <Checkout/>
              }
            >


            </Route>
            <Route
              path="/"
              element={
                <>
                  <HeroSection />
                  <ProductsPage />
                  <TestimonialsSection />
                  <Footer />
                </>
              }
            />

              <Route path="/cart" element={<CartPage />} />
              <Route path="/watches" element={<WatchesPage/>}/>
              <Route path="/contact" element={<ContactUs/>} />
            {/* PRODUCT DETAILS PAGE */}
            <Route path="/product/:slug" element={<ProductDetailsPage />} />
          </Routes>
        </Router>
      )}
    </>
  );
}
