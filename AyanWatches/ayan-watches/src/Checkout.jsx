import { useState, useEffect } from "react";
import { supabase } from "../src/lib/supabaseClient";

export default function Checkout() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: "", text: "" }); // success or error messages
  const [paymentMethod, setPaymentMethod] = useState("cod"); // cod = Cash on Delivery
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    phone: "",
    address: "",
    city: "",
    postal_code: "",
  });
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const c = JSON.parse(localStorage.getItem("cart") || "[]");
    setCart(c);
  }, []);

  const subtotal = cart.reduce((acc, item) => acc + item.price * item.quantity, 0);
  const delivery_fee = 250;
  const total = subtotal + delivery_fee;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ type: "", text: "" });

    if (cart.length === 0) {
      setMessage({ type: "error", text: "Your cart is empty. Add items before placing an order." });
      return;
    }

    setLoading(true);

    const order = {
      ...form,
      items: cart,
      subtotal,
      delivery_fee,
      total,
      payment_method: paymentMethod,
      created_at: new Date().toISOString(), // UTC timestamp
    };

    const { error } = await supabase.from("orders").insert([order]);

    if (error) {
      console.error("Order save error:", error);
      setMessage({ type: "error", text: "Failed to place order. Please try again." });
    } else {
      setCart([]);
      localStorage.removeItem("cart");
      setMessage({ type: "success", text: "Order placed successfully!" });
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black py-10 px-4">
      <div className="max-w-2xl mx-auto bg-black text-white p-8 rounded-xl border border-amber-500 shadow-lg">
        <h1 className="text-3xl font-bold text-amber-400 mb-6">Checkout</h1>

        {/* Messages */}
        {message.text && (
          <div
            className={`p-3 rounded mb-4 ${
              message.type === "error" ? "bg-red-700 text-red-200" : "bg-amber-700 text-black"
            }`}
          >
            {message.text}
          </div>
        )}

        {/* Cart Items */}
        {cart.length > 0 && (
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-amber-300 mb-2">Items in your cart:</h2>
            <ul className="space-y-2 max-h-60 overflow-y-auto">
              {cart.map((item, index) => (
                <li key={index} className="flex justify-between items-center bg-gray-800 p-3 rounded border border-amber-500">
                  <div>
                    <p className="font-medium">{item.name}</p>
                    <p className="text-sm text-amber-300">Qty: {item.quantity}</p>
                  </div>
                  <p className="font-bold text-amber-400">Rs {item.price * item.quantity}</p>
                </li>
              ))}
            </ul>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            className="w-full p-3 rounded bg-black/80 placeholder-amber-300 text-white border border-amber-500"
            placeholder="Full Name"
            required
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          />
          <input
            type="email"
            className="w-full p-3 rounded bg-black/80 placeholder-amber-300 text-white border border-amber-500"
            placeholder="Email"
            required
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          <input
            className="w-full p-3 rounded bg-black/80 placeholder-amber-300 text-white border border-amber-500"
            placeholder="Phone"
            required
            onChange={(e) => setForm({ ...form, phone: e.target.value })}
          />
          <textarea
            className="w-full p-3 rounded bg-black/80 placeholder-amber-300 text-white border border-amber-500"
            placeholder="Address"
            required
            onChange={(e) => setForm({ ...form, address: e.target.value })}
          />
          <input
            className="w-full p-3 rounded bg-black/80 placeholder-amber-300 text-white border border-amber-500"
            placeholder="City"
            required
            onChange={(e) => setForm({ ...form, city: e.target.value })}
          />
          <input
            className="w-full p-3 rounded bg-black/80 placeholder-amber-300 text-white border border-amber-500"
            placeholder="Postal Code"
            required
            onChange={(e) => setForm({ ...form, postal_code: e.target.value })}
          />

          {/* Payment Method */}
          <div className="pt-4">
            <p className="text-amber-300 font-medium mb-2">Select Payment Method:</p>
            <label className="flex items-center gap-2">
              <input
                type="radio"
                name="payment"
                value="cod"
                checked={paymentMethod === "cod"}
                onChange={() => setPaymentMethod("cod")}
              />
              <span>Cash on Delivery</span>
            </label>
            <label className="flex items-center gap-2 mt-1">
              <input
                type="radio"
                name="payment"
                value="jazzcash"
                checked={paymentMethod === "jazzcash"}
                onChange={() => setPaymentMethod("jazzcash")}
              />
              <span>JazzCash</span>
            </label>
            {paymentMethod === "jazzcash" && (
              <p className="text-amber-400 text-sm mt-1">
                Please pay to <span className="font-bold">03002164090</span>. Delivery will not occur without payment.
              </p>
            )}
          </div>

          {/* Totals */}
          <div className="border-t border-amber-500 pt-4 text-amber-200">
            <p>Subtotal: Rs {subtotal}</p>
            <p>Delivery Fee: Rs {delivery_fee}</p>
            <p className="text-amber-300 mt-1 font-bold text-lg">Total: Rs {total}</p>
          </div>

          <button
            disabled={loading}
            className="w-full bg-amber-500 text-black font-bold p-3 rounded-lg mt-4 hover:brightness-105 transition"
          >
            {loading ? "Placing Order..." : "Place Order"}
          </button>
        </form>
      </div>
    </div>
  );
}
