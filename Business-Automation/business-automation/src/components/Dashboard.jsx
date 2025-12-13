import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API = "http://127.0.0.1:8000";

const Dashboard = () => {
  const [selectedSection, setSelectedSection] = useState('add');
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [form, setForm] = useState({
    name: '',
    price: '',
    quantity: '',
    description: ''
  });

  useEffect(() => {
    fetchProducts();
    fetchOrders();
  }, []);

  const fetchProducts = async () => {
    const res = await axios.get(`${API}/product/`);
    setProducts(res.data);
  };

  const fetchOrders = async () => {
    const res = await axios.get(`${API}/userinfo/`);
    setOrders(res.data);
  };

  const handleAddProduct = async () => {
    await axios.post(`${API}/product/`, {
      name: form.name,
      price: Number(form.price),
      quantity: Number(form.quantity),
      description: form.description
    });
    fetchProducts();
    setForm({ name: '', price: '', quantity: '', description: '' });
    alert("Product added!");
  };

  const changeStatus = async (orderId, newStatus) => {
    await axios.post(`${API}/statuschange/`, {
      order_id: orderId,
      status: newStatus
    });
    fetchOrders();
  };

  return (
    <div className="dashboard-container" style={{ display: 'flex', minHeight: '100vh' }}>
      <aside className="sidebar" style={{ width: '250px', background: '#111', color: '#fff', padding: '20px' }}>
        <h2>Inventory Panel</h2>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ cursor: 'pointer', marginBottom: '10px' }} onClick={() => setSelectedSection('add')}>Add Product</li>
          <li style={{ cursor: 'pointer', marginBottom: '10px' }} onClick={() => setSelectedSection('purchased')}>Purchased Items</li>
        </ul>
      </aside>

      <main className="content" style={{ flex: 1, padding: '30px' }}>
        {selectedSection === 'add' && (
          <div className="section">
            <h2>Add Product</h2>
            <input type="text" placeholder="Product Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            <input type="number" placeholder="Price" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} />
            <input type="number" placeholder="Quantity" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} />
            <textarea placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })}></textarea>
            <button onClick={handleAddProduct}>Add Product</button>
          </div>
        )}

        {selectedSection === 'purchased' && (
          <div className="section">
            <h2>Purchased Items</h2>
            {orders.length === 0 ? (
              <p>No orders yet.</p>
            ) : (
              orders.map((order, i) => (
                <div
                  key={i}
                  className="purchased-item"
                  style={{
                    border: '1px solid #ccc',
                    borderRadius: '8px',
                    padding: '15px',
                    marginBottom: '20px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                  }}
                >
                  <p><strong>Order ID:</strong> {order.order_id}</p>
                  <p><strong>Product:</strong> {order.product_name}</p>
                  <p><strong>Email:</strong> {order.email}</p>
                  <p><strong>Quantity:</strong> {order.product_quantity}</p>
                  <p><strong>Payment:</strong> {order.payment_method}</p>
                  <p><strong>Status:</strong> {order.status}</p>

                  <select
                    value={order.status}
                    onChange={(e) => changeStatus(order.order_id, e.target.value)}
                    style={{ padding: '6px', marginTop: '10px' }}
                  >
                    <option value="Pending">Pending</option>
                    <option value="Rider has taken your order">Rider has taken your order</option>
                    <option value="Cancelled">Cancelled</option>
                    <option value="Delivered">Delivered</option>
                  </select>
                </div>
              ))
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
