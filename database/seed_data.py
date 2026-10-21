"""
SmartBiz Analytics - Repeatable Deterministic Retail Seed Data Generator
Populates at least:
- 12 Suppliers
- 120 Customers
- 36 Products (across 5 categories)
- 650 Orders (with 1800+ order items across 5 regions over past 15 months)
- 36 Inventory records (including healthy, low-stock, and critical replenishment items)
- Initial anomaly alerts and baseline customer segments
"""

import os
import sys
import random
from datetime import datetime, date, timedelta
from decimal import Decimal
from pathlib import Path

# Ensure backend can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.db.session import SessionLocal, engine
from backend.app.models import (
    Supplier, Customer, Product, Order, OrderItem,
    Inventory, Forecast, CustomerSegment, AnomalyAlert, AlgorithmRun
)

# Seed random number generator for exact deterministic reproducibility
random.seed(42)

def seed_database(reset: bool = False):
    db = SessionLocal()
    try:
        if reset:
            print("[INFO] Resetting database tables for fresh seeding...")
            db.query(AlgorithmRun).delete()
            db.query(AnomalyAlert).delete()
            db.query(CustomerSegment).delete()
            db.query(Forecast).delete()
            db.query(OrderItem).delete()
            db.query(Order).delete()
            db.query(Inventory).delete()
            db.query(Product).delete()
            db.query(Customer).delete()
            db.query(Supplier).delete()
            db.commit()

        # Check if suppliers already exist
        existing_suppliers = db.query(Supplier).count()
        if existing_suppliers > 0 and not reset:
            print(f"[INFO] Database already seeded ({existing_suppliers} suppliers found). Skipping seed.")
            return

        print("[INFO] Seeding Suppliers...")
        supplier_data = [
            ("Apex Global Tech", "contact@apextech.com", "+1-555-0101", "San Jose"),
            ("Nordic Industrial Supplies", "orders@nordicind.com", "+1-555-0102", "Chicago"),
            ("Zenith Electronics Ltd", "support@zenithelec.com", "+1-555-0103", "Austin"),
            ("Crestview Goods Co", "sales@crestview.com", "+1-555-0104", "Seattle"),
            ("Summit Warehousing & Supply", "info@summitsupply.com", "+1-555-0105", "Denver"),
            ("Pacific Horizon Traders", "dispatch@pacifichorizon.com", "+1-555-0106", "Los Angeles"),
            ("Keystone Manufacturing", "orders@keystonemfg.com", "+1-555-0107", "Philadelphia"),
            ("Beacon Valley Logistics", "service@beaconvalley.com", "+1-555-0108", "Boston"),
            ("Vanguard Retail Partners", "b2b@vanguardrp.com", "+1-555-0109", "Atlanta"),
            ("Atlas Office Solutions", "support@atlasoffice.com", "+1-555-0110", "Dallas"),
            ("Pinnacle Home Essentials", "team@pinnaclehome.com", "+1-555-0111", "Phoenix"),
            ("Evergreen Apparel Wholesale", "orders@evergreenapp.com", "+1-555-0112", "Portland"),
        ]
        suppliers = []
        for name, email, phone, city in supplier_data:
            s = Supplier(supplier_name=name, contact_email=email, phone=phone, city=city, is_active=True)
            db.add(s)
            suppliers.append(s)
        db.commit()

        print("[INFO] Seeding Products (36 items across 5 categories)...")
        # Structure: (name, category, supplier_idx, unit_cost, selling_price)
        raw_products = [
            # Electronics
            ("UltraHD 4K Monitor 27-inch", "Electronics", 0, 185.00, 299.99),
            ("Mechanical Ergonomic Keyboard", "Electronics", 2, 45.00, 89.99),
            ("Precision Wireless Optical Mouse", "Electronics", 2, 14.50, 34.99),
            ("Active Noise-Cancelling Headphones", "Electronics", 0, 75.00, 149.99),
            ("USB-C Multiport Hub 8-in-1", "Electronics", 0, 18.00, 42.50),
            ("High-Speed External SSD 1TB", "Electronics", 2, 52.00, 109.99),
            ("Smart HD Conference Webcam", "Electronics", 0, 32.00, 69.99),
            ("Braided Fast-Charging Cable 2m", "Electronics", 2, 3.50, 12.99),

            # Office Supplies
            ("Executive High-Back Mesh Chair", "Office Supplies", 9, 110.00, 229.00),
            ("Motorized Height-Adjustable Desk", "Office Supplies", 9, 195.00, 399.00),
            ("A4 Recycled Multipurpose Paper (5 Reams)", "Office Supplies", 9, 16.00, 32.50),
            ("Heavy-Duty Metal Desktop Stapler", "Office Supplies", 3, 6.00, 15.99),
            ("Retractable Gel Pens (Pack of 12)", "Office Supplies", 3, 4.00, 11.50),
            ("Dry-Erase Magnetic Whiteboard 36x24", "Office Supplies", 9, 22.00, 54.00),
            ("Steel Mesh Desktop Organizer", "Office Supplies", 3, 7.50, 18.99),

            # Home & Kitchen
            ("Stainless Steel Thermal Travel Mug", "Home & Kitchen", 10, 8.50, 24.99),
            ("Smart Electric Pour-Over Kettle", "Home & Kitchen", 10, 35.00, 79.99),
            ("Compact Single-Serve Coffee Maker", "Home & Kitchen", 10, 42.00, 94.50),
            ("Cast Iron Dutch Oven 6-Quart", "Home & Kitchen", 1, 38.00, 84.99),
            ("Non-Stick Professional Frying Pan 10-inch", "Home & Kitchen", 1, 19.00, 44.99),
            ("Digital Food Kitchen Scale", "Home & Kitchen", 10, 9.00, 21.99),
            ("Silicone Cooking Utensil Set (10-Piece)", "Home & Kitchen", 1, 11.00, 26.50),

            # Apparel
            ("Heavyweight Organic Cotton T-Shirt", "Apparel", 11, 7.00, 22.00),
            ("Water-Resistant Technical Windbreaker", "Apparel", 11, 32.00, 79.00),
            ("Thermal Fleece Quarter-Zip Pullover", "Apparel", 11, 21.00, 49.50),
            ("Comfort-Stretch Everyday Chino Pants", "Apparel", 11, 18.00, 45.00),
            ("Merino Wool Hiking Socks (3-Pack)", "Apparel", 11, 8.00, 19.99),
            ("Breathable Running Performance Cap", "Apparel", 11, 6.50, 18.00),

            # Health & Personal Care
            ("Sonic Rechargeable Electric Toothbrush", "Health & Personal Care", 4, 22.00, 54.99),
            ("Smart Bluetooth Body Composition Scale", "Health & Personal Care", 4, 18.00, 42.00),
            ("Deep Tissue Muscle Massage Gun", "Health & Personal Care", 4, 45.00, 99.00),
            ("Ultrasonic Cool Mist Aromatherapy Diffuser", "Health & Personal Care", 7, 12.00, 29.99),
            ("Ergonomic Lumbar Support Memory Cushion", "Health & Personal Care", 7, 14.00, 34.50),
            ("Compact Travel First-Aid Kit (100 Pieces)", "Health & Personal Care", 7, 6.50, 16.99),
            ("HEPA Room Air Purifier Filter", "Health & Personal Care", 4, 28.00, 68.00),
            ("Stainless Steel Digital Thermometer", "Health & Personal Care", 7, 5.00, 14.50),
        ]

        products = []
        for name, cat, s_idx, cost, price in raw_products:
            p = Product(
                product_name=name,
                category=cat,
                supplier_id=suppliers[s_idx].supplier_id,
                unit_cost=Decimal(str(cost)),
                selling_price=Decimal(str(price)),
                is_active=True
            )
            db.add(p)
            products.append(p)
        db.commit()

        print("[INFO] Seeding Customers (125 customers across 15 major cities)...")
        first_names = [
            "Emma", "Liam", "Olivia", "Noah", "Ava", "Oliver", "Sophia", "Elijah", "Charlotte", "William",
            "Amelia", "James", "Mia", "Benjamin", "Harper", "Lucas", "Evelyn", "Henry", "Abigail", "Alexander",
            "Emily", "Michael", "Elizabeth", "Daniel", "Mila", "Matthew", "Ella", "Jackson", "Avery", "Sebastian",
            "Sofia", "David", "Camila", "Carter", "Aria", "Wyatt", "Scarlett", "Jayden", "Victoria", "John",
            "Madison", "Owen", "Luna", "Dylan", "Grace", "Luke", "Chloe", "Gabriel", "Penelope", "Anthony"
        ]
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
            "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
            "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
            "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
        ]
        cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Seattle", "Denver", "Boston", "Atlanta"
        ]

        customers = []
        base_reg_date = date.today() - timedelta(days=600)
        for i in range(125):
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            cname = f"{fname} {lname}"
            email = f"{fname.lower()}.{lname.lower()}{i+1}@example.com"
            city = random.choice(cities)
            reg_offset = random.randint(0, 500)
            reg_date = base_reg_date + timedelta(days=reg_offset)
            c = Customer(
                customer_name=cname,
                email=email,
                city=city,
                registration_date=reg_date
            )
            db.add(c)
            customers.append(c)
        db.commit()

        print("[INFO] Seeding Orders and Order Items (680 orders, 1800+ items)...")
        regions = ["North", "South", "East", "West", "Central"]
        start_date = date.today() - timedelta(days=400)
        end_date = date.today() - timedelta(days=2)

        # Distribute orders across customers: some frequent (VIPs), some regular, some one-time
        # Give first 15 customers higher order counts (Loyal / Champions)
        order_records = []
        order_items_records = []

        total_orders_target = 680
        created_orders = 0

        # We will create anomalies deliberately on a few specific orders:
        # 1. Extreme order quantity (150 units of high-cost monitor)
        # 2. Extreme monetary value order ($18,000+)
        # 3. Off-pattern rapid burst orders
        anomaly_targets = [15, 88, 142, 280, 420]

        current_date_pointer = start_date
        date_step_days = (end_date - start_date).days / total_orders_target

        for o_idx in range(total_orders_target):
            # Pick customer: bias towards VIPs
            if random.random() < 0.40:
                cust = random.choice(customers[:20]) # VIP cohort
            elif random.random() < 0.75:
                cust = random.choice(customers[20:70]) # Mid-tier
            else:
                cust = random.choice(customers[70:]) # Occasional

            # Calculate order date chronologically
            jitter_days = random.randint(0, 3)
            order_day = start_date + timedelta(days=int(o_idx * date_step_days) + jitter_days)
            if order_day > end_date:
                order_day = end_date
            # Ensure order is on or after customer registration date
            if order_day < cust.registration_date:
                order_day = cust.registration_date + timedelta(days=random.randint(1, 10))

            reg = random.choice(regions)
            status_rand = random.random()
            if status_rand < 0.88:
                status = "Completed"
            elif status_rand < 0.95:
                status = "Pending"
            else:
                status = "Cancelled"

            order_obj = Order(
                customer_id=cust.customer_id,
                order_date=order_day,
                region=reg,
                order_status=status
            )
            db.add(order_obj)
            db.flush() # get order_id

            # Generate 1 to 5 line items per order
            is_anomaly = o_idx in anomaly_targets
            if is_anomaly:
                num_items = random.randint(4, 7)
            else:
                num_items = random.randint(1, 4)

            chosen_products = random.sample(products, k=min(num_items, len(products)))
            order_total_value = Decimal("0.00")

            for p in chosen_products:
                if is_anomaly and p.category == "Electronics":
                    qty = random.randint(40, 90) # Unusual massive volume
                else:
                    qty = random.randint(1, 5)

                unit_p = p.selling_price
                unit_c = p.unit_cost
                item_total = unit_p * Decimal(str(qty))
                order_total_value += item_total

                oi = OrderItem(
                    order_id=order_obj.order_id,
                    product_id=p.product_id,
                    quantity=qty,
                    unit_price=unit_p,
                    unit_cost=unit_c
                )
                db.add(oi)

            # If anomaly target, add anomaly record immediately
            if is_anomaly:
                score = round(random.uniform(0.85, 0.98), 4)
                severity = "Critical" if score > 0.92 else "High"
                reason = f"Transaction total of ${order_total_value:,.2f} with excessive single-order item quantities deviates significantly from regional baseline."
                alert = AnomalyAlert(
                    order_id=order_obj.order_id,
                    customer_id=cust.customer_id,
                    anomaly_score=Decimal(str(score)),
                    severity=severity,
                    reason=reason,
                    status="Pending Review",
                    detected_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.add(alert)

            created_orders += 1

        db.commit()

        print("[INFO] Seeding Inventory (36 items with healthy, low, and critical stock)...")
        for idx, p in enumerate(products):
            # Mix of healthy stock, low stock (< reorder level), and critical zero stock
            if idx in [1, 5, 8, 14, 21, 28]: # Critical / below reorder
                reorder = random.randint(25, 50)
                stock = random.randint(2, reorder - 5)
            elif idx in [3, 10, 19]: # Near reorder
                reorder = random.randint(20, 35)
                stock = reorder + random.randint(1, 5)
            else: # Healthy stock
                reorder = random.randint(15, 30)
                stock = random.randint(50, 220)

            inv = Inventory(
                product_id=p.product_id,
                supplier_id=p.supplier_id,
                stock_quantity=stock,
                reorder_level=reorder,
                last_updated=datetime.utcnow()
            )
            db.add(inv)
        db.commit()

        print("[INFO] Seeding Baseline Demand Forecasts (historical 14-day horizon)...")
        for p in products[:10]: # Store forecasts for top 10 products
            base_forecast_date = date.today()
            for day_offset in range(1, 15):
                f_date = base_forecast_date + timedelta(days=day_offset)
                pred_qty = Decimal(str(round(random.uniform(12.0, 48.0), 2)))
                lower = round(pred_qty * Decimal("0.82"), 2)
                upper = round(pred_qty * Decimal("1.22"), 2)
                f = Forecast(
                    product_id=p.product_id,
                    forecast_date=f_date,
                    predicted_quantity=pred_qty,
                    lower_bound=lower,
                    upper_bound=upper,
                    model_name="Moving-Average (7D)",
                    generated_at=datetime.utcnow()
                )
                db.add(f)
        db.commit()

        print("[INFO] Seeding Initial RFM Customer Segments...")
        # Create baseline customer segment assignments for demo view
        segment_profiles = [
            ("Champions", 12, 14, Decimal("3200.00")),
            ("Loyal Customers", 25, 9, Decimal("1850.00")),
            ("Potential Loyalists", 40, 5, Decimal("980.00")),
            ("At Risk", 95, 4, Decimal("750.00")),
            ("Hibernating", 180, 2, Decimal("260.00")),
            ("Lost", 280, 1, Decimal("85.00")),
        ]
        for idx, c in enumerate(customers):
            prof = segment_profiles[idx % len(segment_profiles)]
            rec = prof[1] + random.randint(-5, 10)
            freq = max(1, prof[2] + random.randint(-1, 2))
            mon = max(Decimal("50.00"), prof[3] + Decimal(str(random.randint(-100, 200))))
            cs = CustomerSegment(
                customer_id=c.customer_id,
                segment_name=prof[0],
                recency_days=max(1, rec),
                frequency=freq,
                monetary_value=mon,
                model_version="KMeans-RFM-v1.0",
                assigned_at=datetime.utcnow()
            )
            db.add(cs)
        db.commit()

        print("[SUCCESS] Seeding completed successfully!")
        print(f"Total Suppliers: {db.query(Supplier).count()}")
        print(f"Total Customers: {db.query(Customer).count()}")
        print(f"Total Products: {db.query(Product).count()}")
        print(f"Total Orders: {db.query(Order).count()}")
        print(f"Total Order Items: {db.query(OrderItem).count()}")
        print(f"Total Inventory Records: {db.query(Inventory).count()}")
        print(f"Total Anomaly Alerts: {db.query(AnomalyAlert).count()}")
        print(f"Total Forecasts: {db.query(Forecast).count()}")
        print(f"Total Customer Segments: {db.query(CustomerSegment).count()}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seeding failed: {e}", file=sys.stderr)
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv
    seed_database(reset=reset_flag)
