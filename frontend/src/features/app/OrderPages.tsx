import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import { EmptyState } from '../../components/ui/EmptyState';
import {
  ShoppingCart,
  Trash2,
  Plus,
  Minus,
  ShoppingBag,
  ArrowRight,
  Package,
  CheckCircle2,
  Clock
} from 'lucide-react';

export const CartPage: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'cart' | 'browse' | 'orders'>('cart');
  const [items, setItems] = useState<any[]>([]);
  const [products, setProducts] = useState<any[]>([]);
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [addingId, setAddingId] = useState<string | null>(null);
  const [addedToast, setAddedToast] = useState<string | null>(null);

  const fetchCart = async () => {
    try {
      const res = await api.get('/cart');
      setItems(res.data.items || []);
    } catch {
      setItems([]);
    }
  };

  const fetchProducts = async () => {
    try {
      const res = await api.get('/shop/products');
      setProducts(res.data || []);
    } catch {
      setProducts([]);
    }
  };

  const fetchOrders = async () => {
    try {
      const res = await api.get('/orders');
      setOrders(res.data || []);
    } catch {
      setOrders([]);
    }
  };

  const loadAll = async () => {
    setLoading(true);
    await Promise.all([fetchCart(), fetchProducts(), fetchOrders()]);
    setLoading(false);
  };

  useEffect(() => {
    loadAll();
  }, []);

  const updateQty = async (itemId: string, qty: number) => {
    if (qty < 1) return removeItem(itemId);
    await api.patch(`/cart/items/${itemId}`, { quantity: qty });
    fetchCart();
  };

  const removeItem = async (itemId: string) => {
    await api.delete(`/cart/items/${itemId}`);
    fetchCart();
  };

  const handleAddToCart = async (productId: string, productName: string) => {
    setAddingId(productId);
    try {
      await api.post('/cart/items', { product_id: productId, quantity: 1 });
      await fetchCart();
      setAddedToast(`Added "${productName}" to cart!`);
      setTimeout(() => setAddedToast(null), 3000);
    } finally {
      setAddingId(null);
    }
  };

  const total = items.reduce((sum: number, it: any) => sum + it.price_inr * it.quantity, 0);

  if (loading) return <div className="h-64 bg-gray-200 rounded-2xl animate-pulse" />;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <ShoppingCart className="w-6 h-6 text-primary-600" />
            Order / Cart
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Order prototype food products and manage your cart with demo sandbox checkout.
          </p>
        </div>
        <PrototypeBadge />
      </div>

      {/* Toast Notification */}
      {addedToast && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold rounded-xl flex items-center gap-2 animate-fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{addedToast}</span>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-2 border-b border-gray-200 pb-2">
        <button
          onClick={() => setActiveTab('cart')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all ${
            activeTab === 'cart'
              ? 'bg-primary-600 text-white shadow-sm'
              : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
          }`}
        >
          <ShoppingCart className="w-4 h-4" />
          My Cart ({items.length})
        </button>

        <button
          onClick={() => setActiveTab('browse')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all ${
            activeTab === 'browse'
              ? 'bg-primary-600 text-white shadow-sm'
              : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
          }`}
        >
          <ShoppingBag className="w-4 h-4" />
          Available Products ({products.length})
        </button>

        <button
          onClick={() => setActiveTab('orders')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all ${
            activeTab === 'orders'
              ? 'bg-primary-600 text-white shadow-sm'
              : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
          }`}
        >
          <Package className="w-4 h-4" />
          Past Demo Orders ({orders.length})
        </button>
      </div>

      {/* TAB 1: CART */}
      {activeTab === 'cart' && (
        <div className="space-y-4">
          {items.length === 0 ? (
            <EmptyState
              icon={<ShoppingCart className="w-10 h-10 text-gray-400" />}
              title="Your cart is empty"
              description="Explore our prototype foods and add items to your cart."
              action={
                <Button variant="primary" onClick={() => setActiveTab('browse')}>
                  <ShoppingBag className="w-4 h-4 mr-2" />
                  Browse Available Products
                </Button>
              }
            />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-2 space-y-3">
                {items.map((item: any) => (
                  <Card key={item.id} className="p-4 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
                    <div className="space-y-1">
                      <h3 className="text-sm font-bold text-gray-900">{item.product_name}</h3>
                      <p className="text-xs text-gray-500">{item.format}</p>
                      <PrototypeBadge />
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => updateQty(item.id, item.quantity - 1)}
                          className="p-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700"
                        >
                          <Minus className="w-3.5 h-3.5" />
                        </button>
                        <span className="text-sm font-bold w-8 text-center">{item.quantity}</span>
                        <button
                          onClick={() => updateQty(item.id, item.quantity + 1)}
                          className="p-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700"
                        >
                          <Plus className="w-3.5 h-3.5" />
                        </button>
                      </div>
                      <span className="text-sm font-bold text-gray-900 w-16 text-right">
                        ₹{(item.price_inr * item.quantity).toFixed(0)}
                      </span>
                      <button
                        onClick={() => removeItem(item.id)}
                        className="p-1.5 text-red-400 hover:text-red-600 rounded-lg hover:bg-red-50"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </Card>
                ))}
              </div>

              {/* Order Summary */}
              <div className="space-y-4">
                <Card className="p-5 space-y-4 bg-gray-50 border border-gray-200">
                  <h3 className="text-sm font-bold text-gray-900">Order Summary</h3>
                  <div className="flex justify-between text-xs text-gray-600">
                    <span>Subtotal ({items.length} items)</span>
                    <span className="font-semibold text-gray-900">₹{total.toFixed(0)}</span>
                  </div>
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Demo Shipping</span>
                    <span className="text-emerald-700 font-semibold">FREE</span>
                  </div>
                  <div className="border-t border-gray-200 pt-3 flex justify-between font-bold text-sm">
                    <span>Total (Demo)</span>
                    <span className="text-primary-700">₹{total.toFixed(0)}</span>
                  </div>
                  <PrototypeBadge />
                  <Button variant="primary" className="w-full" onClick={() => navigate('/app/checkout')}>
                    Proceed to Demo Checkout
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </Card>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: BROWSE AVAILABLE PRODUCTS */}
      {activeTab === 'browse' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {products.map((prod: any) => (
              <Card key={prod.id} className="p-5 flex flex-col justify-between hover:border-primary-300 transition-all">
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-primary-100 text-primary-800">
                      {prod.category || 'Aspirational Prototype'}
                    </span>
                    <span className="text-sm font-bold text-gray-900">₹{prod.price_inr}</span>
                  </div>
                  <h3 className="text-sm font-bold text-gray-900">{prod.name}</h3>
                  <p className="text-xs text-gray-600 line-clamp-2">{prod.description}</p>

                  {prod.iron_mg && (
                    <div className="p-2 bg-emerald-50 rounded-lg text-[11px] text-emerald-800 font-medium">
                      ⚡ Iron: {prod.iron_mg} mg • Vit C: {prod.vit_c_mg || 12} mg
                    </div>
                  )}
                </div>

                <div className="pt-4 mt-3 border-t border-gray-100 flex items-center justify-between">
                  <PrototypeBadge />
                  <Button
                    size="sm"
                    variant="primary"
                    disabled={addingId === prod.id}
                    onClick={() => handleAddToCart(prod.id, prod.name)}
                  >
                    {addingId === prod.id ? 'Adding...' : 'Add to Cart'}
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* TAB 3: PAST ORDERS */}
      {activeTab === 'orders' && (
        <div className="space-y-4">
          {orders.length === 0 ? (
            <EmptyState
              icon={<Package className="w-10 h-10 text-gray-400" />}
              title="No demo orders placed yet"
              description="Checkout items from your cart to see order tracking here."
            />
          ) : (
            <div className="space-y-3">
              {orders.map((ord: any) => (
                <Card key={ord.id} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold text-gray-900">
                        Order #{ord.id?.slice(0, 8)}
                      </span>
                      <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                        {ord.status || 'Placed'}
                      </span>
                      <PrototypeBadge />
                    </div>
                    <p className="text-xs text-gray-600">
                      {ord.item_count || 1} items • ₹{ord.total_inr} • {new Date(ord.created_at || Date.now()).toLocaleDateString()}
                    </p>
                  </div>
                  <span className="text-xs text-gray-500 italic">Demo Sandbox Order</span>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export const CheckoutPage: React.FC = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', address: '', city: '', state: '', pin: '', phone: '' });
  const [submitting, setSubmitting] = useState(false);
  const [orderId, setOrderId] = useState<string | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      const res = await api.post('/orders', { delivery_address: form, payment_mode: 'demo_sandbox' });
      setOrderId(res.data.order_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Order placement failed. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (orderId) return (
    <div className="max-w-2xl mx-auto text-center space-y-6 py-16">
      <div className="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto">
        <ShoppingBag className="w-8 h-8 text-emerald-600" />
      </div>
      <div>
        <h2 className="text-xl font-bold text-gray-900">Demo Order Placed!</h2>
        <p className="text-sm text-gray-600 mt-1">Order ID: <code className="bg-gray-100 px-2 py-0.5 rounded">{orderId}</code></p>
      </div>
      <PrototypeBadge />
      <p className="text-xs text-gray-500 max-w-sm mx-auto">
        This is a demonstration order only. No payment was charged and no product will be shipped. This prototype shows the end-to-end food ordering workflow.
      </p>
      <div className="flex gap-3 justify-center">
        <Button variant="primary" onClick={() => navigate('/app/cart')}>Return to Order / Cart</Button>
        <Button variant="outline" onClick={() => navigate('/app/progress')}>Track Progress</Button>
      </div>
    </div>
  );

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">Demo Checkout</h1>
        <PrototypeBadge />
      </div>

      <Card className="p-5 space-y-4">
        <h3 className="text-sm font-semibold text-gray-900">Delivery Address</h3>
        {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-xs text-red-700">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              { label: 'Full Name', key: 'name', placeholder: 'Kaviya Shree' },
              { label: 'Phone', key: 'phone', placeholder: '+91 98765 43210' },
            ].map(({ label, key, placeholder }) => (
              <div key={key}>
                <label className="block text-xs font-medium text-gray-700 mb-1">{label} *</label>
                <input
                  required
                  value={(form as any)[key]}
                  onChange={e => setForm({ ...form, [key]: e.target.value })}
                  placeholder={placeholder}
                  className="w-full text-sm px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
            ))}
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Address *</label>
            <input
              required
              value={form.address}
              onChange={e => setForm({ ...form, address: e.target.value })}
              placeholder="House No., Street, Area"
              className="w-full text-sm px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: 'City', key: 'city', placeholder: 'Chennai' },
              { label: 'State', key: 'state', placeholder: 'Tamil Nadu' },
              { label: 'PIN Code', key: 'pin', placeholder: '600001' },
            ].map(({ label, key, placeholder }) => (
              <div key={key}>
                <label className="block text-xs font-medium text-gray-700 mb-1">{label} *</label>
                <input
                  required
                  value={(form as any)[key]}
                  onChange={e => setForm({ ...form, [key]: e.target.value })}
                  placeholder={placeholder}
                  className="w-full text-sm px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
            ))}
          </div>

          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 space-y-2">
            <h4 className="text-xs font-semibold text-amber-900">Payment: Demo Sandbox Mode</h4>
            <p className="text-xs text-amber-800">
              No real payment is processed. This demonstrates the checkout flow for research purposes only. No financial data is collected.
            </p>
          </div>

          <Button type="submit" variant="primary" className="w-full" disabled={submitting}>
            {submitting ? 'Placing Demo Order…' : 'Place Demo Order (Free)'}
          </Button>
        </form>
      </Card>
    </div>
  );
};

export const OrdersPage: React.FC = () => {
  return <CartPage />;
};
