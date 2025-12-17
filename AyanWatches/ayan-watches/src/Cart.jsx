import { useEffect, useState } from "react";
import { Trash2, Plus, Minus } from "lucide-react";
import { useNavigate } from "react-router";

export default function CartPage() {
  const [cart, setCart] = useState([]);

    const navigate = useNavigate()

  const DELIVERY_CHARGES = 250;

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("cart")) || [];
    setCart(saved);
  }, []);

  const updateLocal = (updatedCart) => {
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const increaseQty = (id) => {
    const updated = cart.map((item) =>
      item.id === id ? { ...item, quantity: item.quantity + 1 } : item
    );
    updateLocal(updated);
  };

  const decreaseQty = (id) => {
    const updated = cart
      .map((item) =>
        item.id === id ? { ...item, quantity: Math.max(1, item.quantity - 1) } : item
      );
    updateLocal(updated);
  };

  const removeItem = (id) => {
    const updated = cart.filter((item) => item.id !== id);
    updateLocal(updated);
  };

  const subtotal = cart.reduce(
    (acc, item) => acc + item.price * item.quantity,
    0
  );

  const grandTotal = subtotal + DELIVERY_CHARGES;

  return (
    <div className="min-h-screen bg-black text-white px-6 py-10">
      <h1 className="text-4xl font-bold text-center mb-10 text-amber-400">
        Your Cart
      </h1>

      {cart.length === 0 ? (
        <p className="text-center text-amber-300">Your cart is empty.</p>
      ) : (
        <div className="max-w-3xl mx-auto space-y-6">
          {cart.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between bg-gray-900 p-5 rounded-xl border border-amber-500/20"
            >
              <div className="flex items-center gap-4">
                <img
                  src={item.image}
                  className="w-24 h-24 rounded-lg object-cover border border-amber-500/30"
                />
                <div>
                  <p className="text-lg font-bold">{item.name}</p>
                  <p className="text-amber-400">
                    PKR {item.price.toLocaleString()}
                  </p>

                  {/* Quantity */}
                  <div className="flex items-center gap-3 mt-2">
                    <button
                      onClick={() => decreaseQty(item.id)}
                      className="p-1 bg-gray-800 rounded-full border border-amber-500/30"
                    >
                      <Minus className="w-4 h-4 text-amber-400" />
                    </button>

                    <span className="text-lg font-semibold">{item.quantity}</span>

                    <button
                      onClick={() => increaseQty(item.id)}
                      className="p-1 bg-gray-800 rounded-full border border-amber-500/30"
                    >
                      <Plus className="w-4 h-4 text-amber-400" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Remove */}
              <button
                onClick={() => removeItem(item.id)}
                className="text-red-400 hover:text-red-300"
              >
                <Trash2 className="w-6 h-6" />
              </button>
            </div>
          ))}

          {/* Summary Box */}
          <div className="bg-gray-900 p-6 rounded-xl border border-amber-500/30 mt-8">
            <h2 className="text-2xl font-bold mb-4 text-amber-400">Order Summary</h2>

            <div className="flex justify-between py-2">
              <p className="text-gray-300">Subtotal</p>
              <p className="text-white">PKR {subtotal.toLocaleString()}</p>
            </div>

            <div className="flex justify-between py-2">
              <p className="text-gray-300">Delivery Charges</p>
              <p className="text-white">PKR {DELIVERY_CHARGES}</p>
            </div>

            <div className="h-[1px] w-full bg-amber-500/30 my-3" />

            <div className="flex justify-between py-2 text-xl font-bold">
              <p className="text-amber-400">Grand Total</p>
              <p className="text-amber-400">
                PKR {grandTotal.toLocaleString()}
              </p>
            </div>

            <button
            onClick={() => navigate("/checkout")}
              className="w-full mt-6 bg-gradient-to-r from-amber-400 to-yellow-600 text-black font-bold py-3 rounded-lg hover:shadow-lg hover:shadow-amber-500/40 transition-all"
            >
              Proceed to Checkout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
