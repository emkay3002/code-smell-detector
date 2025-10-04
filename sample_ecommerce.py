
import json
import datetime
import hashlib
import random
import os
from typing import List, Dict, Any, Optional


class ECommerceSystem:
    """E-commerce system demonstrating God Class code smell."""
    
    def __init__(self):
        self.products = {}
        self.users = {}
        self.orders = {}
        self.inventory = {}
        self.payments = {}
        self.shipping = {}
        self.reviews = {}
        self.categories = {}
        self.discounts = {}
        self.coupons = {}
        self.analytics = {}
        self.notifications = {}
        self.settings = {}
        self.logs = []
        self.session_data = {}
        self.cache = {}
        self.temp_data = {}
        
    def add_product(self, name, price, description, category, stock, weight, dimensions, 
                   brand, sku, tags, images, specifications, warranty, return_policy, 
                   shipping_info, tax_rate, discount_rate, review_score, popularity, 
                   related_products, variations, metadata):
        """Add product with Large Parameter List code smell (25 parameters)."""
        product_id = len(self.products) + 1
        self.products[product_id] = {
            'name': name, 'price': price, 'description': description,
            'category': category, 'stock': stock, 'weight': weight,
            'dimensions': dimensions, 'brand': brand, 'sku': sku,
            'tags': tags, 'images': images, 'specifications': specifications,
            'warranty': warranty, 'return_policy': return_policy,
            'shipping_info': shipping_info, 'tax_rate': tax_rate,
            'discount_rate': discount_rate, 'review_score': review_score,
            'popularity': popularity, 'related_products': related_products,
            'variations': variations, 'metadata': metadata
        }
        return product_id
    
    def process_order_workflow(self, order_data):
        """Long Method code smell - handles entire order workflow."""
        # Validate order data
        if not order_data.get('customer_id'):
            raise ValueError("Customer ID required")
        if not order_data.get('items'):
            raise ValueError("Order must contain items")
        if not order_data.get('shipping_address'):
            raise ValueError("Shipping address required")
        if not order_data.get('payment_method'):
            raise ValueError("Payment method required")
        
        # Calculate totals
        subtotal = 0
        tax_amount = 0
        shipping_cost = 0
        discount_amount = 0
        
        for item in order_data['items']:
            product_id = item['product_id']
            quantity = item['quantity']
            product = self.products.get(product_id)
            
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            item_price = product['price'] * quantity
            subtotal += item_price
            
            # Calculate tax (Magic number: 0.08)
            tax_amount += item_price * 0.08
            
            # Calculate shipping (Magic numbers: 10, 0.05)
            if item_price > 100:
                shipping_cost += 0
            else:
                shipping_cost += 10 + (item_price * 0.05)
        
        # Apply discounts (Magic numbers: 0.1, 0.2, 0.15)
        if subtotal > 500:
            discount_amount = subtotal * 0.1
        elif subtotal > 200:
            discount_amount = subtotal * 0.2
        elif subtotal > 100:
            discount_amount = subtotal * 0.15
        
        # Calculate final total
        total = subtotal + tax_amount + shipping_cost - discount_amount
        
        # Create order
        order_id = len(self.orders) + 1
        order = {
            'id': order_id,
            'customer_id': order_data['customer_id'],
            'items': order_data['items'],
            'subtotal': subtotal,
            'tax': tax_amount,
            'shipping': shipping_cost,
            'discount': discount_amount,
            'total': total,
            'status': 'pending',
            'created_at': datetime.datetime.now(),
            'shipping_address': order_data['shipping_address'],
            'payment_method': order_data['payment_method']
        }
        
        # Process payment
        payment_result = self.process_payment(total, order_data['payment_method'])
        if not payment_result['success']:
            raise ValueError("Payment failed")
        
        # Update inventory
        for item in order_data['items']:
            product_id = item['product_id']
            quantity = item['quantity']
            if product_id in self.inventory:
                self.inventory[product_id] -= quantity
            else:
                self.inventory[product_id] = -quantity
        
        # Send notifications
        self.send_order_confirmation(order)
        self.send_inventory_alert()
        self.send_analytics_event('order_created', order)
        
        # Update order status
        order['status'] = 'confirmed'
        order['payment_id'] = payment_result['payment_id']
        
        self.orders[order_id] = order
        return order
    
    def process_payment(self, amount, payment_method):
        """Process payment with magic numbers."""
        # Magic numbers: 0.029, 0.3, 0.1, 0.05
        processing_fee = amount * 0.029
        if payment_method == 'credit_card':
            processing_fee += amount * 0.3
        elif payment_method == 'paypal':
            processing_fee += amount * 0.1
        else:
            processing_fee += amount * 0.05
        
        # Simulate payment processing
        payment_id = random.randint(100000, 999999)
        success = random.random() > 0.1  # 90% success rate
        
        return {
            'success': success,
            'payment_id': payment_id,
            'processing_fee': processing_fee,
            'total_charged': amount + processing_fee
        }
    
    def send_order_confirmation(self, order):
        """Send order confirmation - Feature Envy code smell."""
        email_service = EmailService()
        email_service.send_email(order['customer_id'], "Order Confirmation", 
                               f"Your order #{order['id']} has been confirmed")
        email_service.log_email_sent(order['customer_id'])
        email_service.update_customer_stats(order['customer_id'])
        email_service.send_sms_notification(order['customer_id'])
    
    def send_inventory_alert(self):
        """Send inventory alert - Feature Envy code smell."""
        inventory_service = InventoryService()
        inventory_service.check_low_stock()
        inventory_service.send_restock_alerts()
        inventory_service.update_supplier_notifications()
        inventory_service.generate_purchase_orders()
    
    def send_analytics_event(self, event_type, data):
        """Send analytics event - Feature Envy code smell."""
        analytics_service = AnalyticsService()
        analytics_service.track_event(event_type, data)
        analytics_service.update_metrics()
        analytics_service.send_to_external_api()
        analytics_service.log_performance_data()
    
    def validate_email_address(self, email):
        """Validate email - Duplicated Code smell."""
        if not email or '@' not in email:
            return False
        parts = email.split('@')
        if len(parts) != 2:
            return False
        local, domain = parts
        if not local or not domain:
            return False
        if '.' not in domain:
            return False
        return True
    
    def validate_phone_number(self, phone):
        """Validate phone - Duplicated Code smell."""
        if not phone or len(phone) < 10:
            return False
        if not phone.isdigit():
            return False
        if len(phone) > 15:
            return False
        return True
    
    def calculate_shipping_cost(self, weight, distance, priority, insurance, 
                               fragile, express, weekend, holiday, weather, 
                               traffic, fuel_surcharge, handling_fee, 
                               packaging_cost, delivery_time, route_optimization,
                               driver_experience, vehicle_type, road_conditions,
                               customer_preference, special_requirements):
        """Calculate shipping with Large Parameter List (20 parameters)."""
        # Magic numbers: 0.5, 0.1, 0.2, 0.3, 0.15, 0.25, 0.4, 0.6, 0.8, 0.9
        base_cost = weight * 0.5 + distance * 0.1
        if priority:
            base_cost *= 1.2
        if insurance:
            base_cost += weight * 0.2
        if fragile:
            base_cost += weight * 0.3
        if express:
            base_cost *= 1.5
        if weekend:
            base_cost += 15
        if holiday:
            base_cost += 25
        if weather == 'bad':
            base_cost += 20
        if traffic == 'heavy':
            base_cost += 10
        if fuel_surcharge:
            base_cost += 5
        if handling_fee:
            base_cost += 8
        if packaging_cost:
            base_cost += 12
        if delivery_time < 24:
            base_cost *= 1.4
        if route_optimization:
            base_cost -= 5
        if driver_experience > 5:
            base_cost += 3
        if vehicle_type == 'truck':
            base_cost += 15
        if road_conditions == 'poor':
            base_cost += 8
        if customer_preference == 'morning':
            base_cost += 5
        if special_requirements:
            base_cost += 20
        
        return base_cost


class EmailService:
    """Email service for notifications."""
    
    def __init__(self):
        self.sent_emails = []
        self.email_stats = {}
    
    def send_email(self, to, subject, body):
        """Send email."""
        print(f"Email sent to {to}: {subject}")
        self.sent_emails.append({'to': to, 'subject': subject, 'body': body})
    
    def log_email_sent(self, to):
        """Log email."""
        print(f"Logged email to {to}")
    
    def update_customer_stats(self, customer_id):
        """Update stats."""
        if customer_id not in self.email_stats:
            self.email_stats[customer_id] = 0
        self.email_stats[customer_id] += 1
    
    def send_sms_notification(self, phone):
        """Send SMS."""
        print(f"SMS sent to {phone}")


class InventoryService:
    """Inventory management service."""
    
    def __init__(self):
        self.inventory = {}
        self.alerts = []
    
    def check_low_stock(self):
        """Check low stock."""
        print("Checking low stock levels")
    
    def send_restock_alerts(self):
        """Send restock alerts."""
        print("Sending restock alerts")
    
    def update_supplier_notifications(self):
        """Update supplier notifications."""
        print("Updating supplier notifications")
    
    def generate_purchase_orders(self):
        """Generate purchase orders."""
        print("Generating purchase orders")


class AnalyticsService:
    """Analytics service."""
    
    def __init__(self):
        self.events = []
        self.metrics = {}
    
    def track_event(self, event_type, data):
        """Track event."""
        print(f"Tracking event: {event_type}")
        self.events.append({'type': event_type, 'data': data})
    
    def update_metrics(self):
        """Update metrics."""
        print("Updating metrics")
    
    def send_to_external_api(self):
        """Send to external API."""
        print("Sending to external API")
    
    def log_performance_data(self):
        """Log performance data."""
        print("Logging performance data")


def main():
    """Main function demonstrating the e-commerce system."""
    system = ECommerceSystem()
    
    # Add a product
    product_id = system.add_product(
        "Laptop", 999.99, "High-performance laptop", "Electronics", 50,
        2.5, "15x10x1", "TechBrand", "LT001", ["laptop", "computer"],
        ["img1.jpg", "img2.jpg"], {"RAM": "16GB", "Storage": "512GB"},
        "2 years", "30 days", "Free shipping", 0.08, 0.1, 4.5, 100,
        [1, 2, 3], {"color": ["black", "silver"], "size": ["13", "15"]},
        {"warranty": "extended", "support": "premium"}
    )
    
    # Create an order
    order_data = {
        'customer_id': 'user123',
        'items': [{'product_id': product_id, 'quantity': 1}],
        'shipping_address': {'street': '123 Main St', 'city': 'Anytown'},
        'payment_method': 'credit_card'
    }
    
    try:
        order = system.process_order_workflow(order_data)
        print(f"Order created: {order['id']}")
        print(f"Total: ${order['total']:.2f}")
    except ValueError as e:
        print(f"Order failed: {e}")
    
    # Test validation functions
    print(f"Email valid: {system.validate_email_address('test@example.com')}")
    print(f"Phone valid: {system.validate_phone_number('1234567890')}")


if __name__ == "__main__":
    main()
