import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { EmptyState } from '../../components/ui/EmptyState';
import { ShoppingBag, ShoppingCart, Package, Info } from 'lucide-react';
import { Badge } from '../../components/ui/Badge';

export const ShopPage: React.FC = () => {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [addingId, setAddingId] = useState<string | null>(null);
  const [cartAdded, setCartAdded] = useState<Set<string>>(new Set());

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await api.get('/shop/products');
        setProducts(res.data);
      } catch {
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  const handleAddToCart = async (productId: string) => {
    setAddingId(productId);
    try {
      await api.post('/cart/items', { product_id: productId, quantity: 1 });
      setCartAdded((prev) => new Set([...prev, productId]));
    } finally {
      setAddingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Prototype Shop</h1>
          <p className="text-sm text-gray-600 mt-0.5">Browse aspirational food product prototypes — demo checkout only.</p>
        </div>
        <div className="flex items-center gap-2">
          <PrototypeBadge />
          <Link to="/app/cart">
            <Button variant="outline" size="sm">
              <ShoppingCart className="w-4 h-4 mr-1.5" />
              View Cart
            </Button>
          </Link>
        </div>
      </div>

      <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 flex gap-2 text-xs text-amber-800">
        <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <span>All products are prototype demonstrations. No actual sale, payment, or delivery occurs. Nutrient values are computed from IFCT 2017 reference data for the displayed serving size.</span>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {[1, 2, 3, 4, 5].map((i) => <div key={i} className="h-56 bg-gray-200 rounded-2xl animate-pulse" />)}
        </div>
      ) : products.length === 0 ? (
        <EmptyState
          icon={<ShoppingBag className="w-10 h-10 text-gray-400" />}
          title="No products available"
          description="Generate a personalized formulation first to see matching products in the shop."
          action={<Link to="/app/generate"><Button variant="primary">Generate Formulation</Button></Link>}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {products.map((product: any) => (
            <Card key={product.id} className="flex flex-col p-5 space-y-4 hover:border-primary-300 transition">
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Package className="w-5 h-5 text-primary-500 shrink-0" />
                  <div>
                    <h3 className="text-sm font-bold text-gray-900 leading-tight">{product.name}</h3>
                    <p className="text-xs text-gray-500">{product.format}</p>
                  </div>
                </div>
                <Badge variant="outline" className="text-xs text-primary-700 border-primary-200 bg-primary-50 shrink-0">
                  Prototype
                </Badge>
              </div>

              <p className="text-xs text-gray-600 leading-relaxed flex-1">{product.description}</p>

              <div className="grid grid-cols-3 gap-2 text-center">
                <div className="p-2 bg-primary-50 rounded-lg">
                  <div className="text-xs font-bold text-primary-900">{product.iron_mg_per_serving} mg</div>
                  <div className="text-[10px] text-primary-700">Iron/Serving</div>
                </div>
                <div className="p-2 bg-gray-50 rounded-lg">
                  <div className="text-xs font-bold text-gray-900">{product.serving_size_g}g</div>
                  <div className="text-[10px] text-gray-600">Serving</div>
                </div>
                <div className="p-2 bg-amber-50 rounded-lg">
                  <div className="text-xs font-bold text-amber-900">₹{product.price_inr}</div>
                  <div className="text-[10px] text-amber-700">Est. Price</div>
                </div>
              </div>

              <PrototypeBadge />

              <Button
                variant={cartAdded.has(product.id) ? 'ghost' : 'primary'}
                size="sm"
                className="w-full"
                onClick={() => handleAddToCart(product.id)}
                disabled={addingId === product.id || cartAdded.has(product.id)}
              >
                <ShoppingCart className="w-4 h-4 mr-1.5" />
                {cartAdded.has(product.id) ? 'Added to Demo Cart ✓' : addingId === product.id ? 'Adding…' : 'Add to Demo Cart'}
              </Button>
            </Card>
          ))}
        </div>
      )}

      <MedicalDisclaimer />
    </div>
  );
};

