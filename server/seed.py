#!/usr/bin/env python3

import os
import sys
from datetime import datetime, date, timedelta
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Medicine, MedicineCategory, Manufacturer

def create_categories():
    """Create medicine categories"""
    categories_data = [
        {"name": "Tablets", "description": "Solid dosage forms for oral administration"},
        {"name": "Capsules", "description": "Encapsulated medicines in gelatin shells"},
        {"name": "Syrups", "description": "Liquid medicines with sweetening agents"},
        {"name": "Injections", "description": "Injectable medicines for IV, IM, or SC use"},
        {"name": "Ointments", "description": "Topical applications for skin conditions"},
        {"name": "Drops", "description": "Eye, ear, and nasal drops"},
        {"name": "Inhalers", "description": "Respiratory medicines for inhalation"},
        {"name": "Powders", "description": "Powder formulations for reconstitution"},
        {"name": "Creams", "description": "Topical creams for skin application"},
        {"name": "Gels", "description": "Gel formulations for topical use"}
    ]
    
    categories = []
    for cat_data in categories_data:
        category = MedicineCategory.query.filter_by(name=cat_data["name"]).first()
        if not category:
            category = MedicineCategory(
                name=cat_data["name"],
                description=cat_data["description"]
            )
            db.session.add(category)
            categories.append(category)
        else:
            categories.append(category)
    
    db.session.commit()
    return categories

def create_manufacturers():
    """Create manufacturers with enhanced contact information"""
    manufacturers_data = [
        {
            "name": "Cipla Limited",
            "contact_info": "+91-22-2482-6000",
            "address": "Cipla House, Peninsula Business Park, Mumbai, India",
            "email": "info@cipla.com",
            "phone": "+91-22-2482-6000"
        },
        {
            "name": "Sun Pharmaceutical",
            "contact_info": "+91-22-4324-4324",
            "address": "Sun House, 201 B/1, Western Express Highway, Mumbai, India",
            "email": "corporate@sunpharma.com",
            "phone": "+91-22-4324-4324"
        },
        {
            "name": "Dr. Reddy's Laboratories",
            "contact_info": "+91-40-4900-2900",
            "address": "8-2-337, Road No. 3, Banjara Hills, Hyderabad, India",
            "email": "info@drreddys.com",
            "phone": "+91-40-4900-2900"
        },
        {
            "name": "Lupin Pharmaceuticals",
            "contact_info": "+91-22-6640-2323",
            "address": "Kalina, Santacruz East, Mumbai, India",
            "email": "corporate@lupin.com",
            "phone": "+91-22-6640-2323"
        },
        {
            "name": "Aurobindo Pharma",
            "contact_info": "+91-40-6672-5000",
            "address": "Galaxy, Pragati Maidan, Hyderabad, India",
            "email": "info@aurobindo.com",
            "phone": "+91-40-6672-5000"
        },
        {
            "name": "Cadila Healthcare (Zydus)",
            "contact_info": "+91-79-2665-9999",
            "address": "Zydus Tower, Satellite Cross Roads, Ahmedabad, India",
            "email": "info@zyduscadila.com",
            "phone": "+91-79-2665-9999"
        },
        {
            "name": "Glenmark Pharmaceuticals",
            "contact_info": "+91-22-4018-9999",
            "address": "B/2, Mahalaxmi Chambers, Mumbai, India",
            "email": "info@glenmarkpharma.com",
            "phone": "+91-22-4018-9999"
        },
        {
            "name": "Torrent Pharmaceuticals",
            "contact_info": "+91-79-2665-3000",
            "address": "Torrent House, Off Ashram Road, Ahmedabad, India",
            "email": "info@torrentpharma.com",
            "phone": "+91-79-2665-3000"
        }
    ]
    
    manufacturers = []
    for mfg_data in manufacturers_data:
        manufacturer = Manufacturer.query.filter_by(name=mfg_data["name"]).first()
        if not manufacturer:
            manufacturer = Manufacturer(
                name=mfg_data["name"],
                contact_info=mfg_data["contact_info"],
                address=mfg_data["address"],
                email=mfg_data["email"],
                phone=mfg_data["phone"]
            )
            db.session.add(manufacturer)
            manufacturers.append(manufacturer)
        else:
            manufacturers.append(manufacturer)
    
    db.session.commit()
    return manufacturers

def create_enhanced_medicines():
    """Create medicines with all the new enhanced fields"""
    medicines_data = [
        {
            "name": "Paracetamol",
            "description": "Pain reliever and fever reducer",
            "dosage": "500mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (10, 15),
            "selling_range": (18, 25)
        },
        {
            "name": "Aspirin",
            "description": "Anti-inflammatory and blood thinner",
            "dosage": "75mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (15, 20),
            "selling_range": (25, 35)
        },
        {
            "name": "Ibuprofen",
            "description": "Non-steroidal anti-inflammatory drug",
            "dosage": "400mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (20, 25),
            "selling_range": (30, 40)
        },
        {
            "name": "Amoxicillin",
            "description": "Broad-spectrum antibiotic",
            "dosage": "500mg",
            "form": "capsule",
            "category": "Capsules",
            "cost_range": (60, 80),
            "selling_range": (90, 130)
        },
        {
            "name": "Cetirizine",
            "description": "Antihistamine for allergies",
            "dosage": "10mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (30, 40),
            "selling_range": (45, 65)
        },
        {
            "name": "Cough Syrup",
            "description": "Relieves cough and throat irritation",
            "dosage": "100ml",
            "form": "syrup",
            "category": "Syrups",
            "cost_range": (40, 60),
            "selling_range": (70, 100)
        },
        {
            "name": "Multivitamin Syrup",
            "description": "Daily vitamin and mineral supplement",
            "dosage": "200ml",
            "form": "syrup",
            "category": "Syrups",
            "cost_range": (100, 150),
            "selling_range": (180, 220)
        },
        {
            "name": "Insulin",
            "description": "Hormone for diabetes management",
            "dosage": "100IU/ml",
            "form": "injection",
            "category": "Injections",
            "cost_range": (250, 350),
            "selling_range": (400, 550)
        },
        {
            "name": "Betadine Ointment",
            "description": "Antiseptic for wound care",
            "dosage": "25g",
            "form": "ointment",
            "category": "Ointments",
            "cost_range": (30, 45),
            "selling_range": (50, 70)
        },
        {
            "name": "Eye Drops",
            "description": "Lubricating drops for dry eyes",
            "dosage": "10ml",
            "form": "drops",
            "category": "Drops",
            "cost_range": (60, 80),
            "selling_range": (90, 130)
        },
        {
            "name": "Salbutamol Inhaler",
            "description": "Bronchodilator for asthma",
            "dosage": "100mcg",
            "form": "inhaler",
            "category": "Inhalers",
            "cost_range": (150, 200),
            "selling_range": (250, 320)
        },
        {
            "name": "Omeprazole",
            "description": "Proton pump inhibitor for acid reflux",
            "dosage": "20mg",
            "form": "capsule",
            "category": "Capsules",
            "cost_range": (35, 50),
            "selling_range": (60, 85)
        },
        {
            "name": "Metformin",
            "description": "Diabetes medication",
            "dosage": "500mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (20, 30),
            "selling_range": (35, 55)
        },
        {
            "name": "Atorvastatin",
            "description": "Cholesterol-lowering medication",
            "dosage": "10mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (70, 100),
            "selling_range": (120, 170)
        },
        {
            "name": "Amlodipine",
            "description": "Blood pressure medication",
            "dosage": "5mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (25, 35),
            "selling_range": (40, 60)
        },
        {
            "name": "Azithromycin",
            "description": "Macrolide antibiotic",
            "dosage": "250mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (100, 150),
            "selling_range": (180, 230)
        },
        {
            "name": "Diclofenac Gel",
            "description": "Topical anti-inflammatory",
            "dosage": "30g",
            "form": "gel",
            "category": "Gels",
            "cost_range": (50, 70),
            "selling_range": (80, 110)
        },
        {
            "name": "Loratadine",
            "description": "Non-drowsy antihistamine",
            "dosage": "10mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (30, 45),
            "selling_range": (50, 75)
        },
        {
            "name": "Vitamin D3",
            "description": "Vitamin D supplement",
            "dosage": "1000IU",
            "form": "powder",
            "category": "Powders",
            "cost_range": (80, 120),
            "selling_range": (140, 190)
        },
        {
            "name": "Iron Tablets",
            "description": "Iron supplement for anemia",
            "dosage": "65mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (15, 25),
            "selling_range": (30, 45)
        },
        {
            "name": "Calcium Carbonate",
            "description": "Calcium supplement",
            "dosage": "500mg",
            "form": "tablet",
            "category": "Tablets",
            "cost_range": (20, 35),
            "selling_range": (40, 60)
        },
        {
            "name": "Antacid Syrup",
            "description": "Relief from acidity and heartburn",
            "dosage": "170ml",
            "form": "syrup",
            "category": "Syrups",
            "cost_range": (25, 40),
            "selling_range": (45, 65)
        }
    ]
    
    # Get all categories and manufacturers
    categories = MedicineCategory.query.all()
    manufacturers = Manufacturer.query.all()
    
    category_map = {cat.name: cat for cat in categories}
    
    medicines = []
    
    for i, med_data in enumerate(medicines_data):
        # Check if medicine already exists
        existing = Medicine.query.filter_by(
            name=med_data["name"], 
            dosage=med_data["dosage"]
        ).first()
        if existing:
            continue
        
        # Generate dates
        purchase_date = date.today() - timedelta(days=random.randint(1, 365))
        expiry_date = purchase_date + timedelta(days=random.randint(365, 1095))  # 1-3 years
        
        # Generate batch number
        batch_number = f"B{2024}{str(i+1).zfill(3)}{random.randint(10, 99)}"
        
        # Generate prices
        cost_price = round(random.uniform(med_data["cost_range"][0], med_data["cost_range"][1]), 2)
        selling_price = round(random.uniform(med_data["selling_range"][0], med_data["selling_range"][1]), 2)
        
        # Generate quantity (some will be low stock for testing alerts)
        if random.random() < 0.2:  # 20% chance of low stock
            quantity = random.randint(1, 8)
            minimum_stock = 10
        else:
            quantity = random.randint(20, 500)
            minimum_stock = random.randint(5, 20)
        
        # Select random manufacturer
        manufacturer = random.choice(manufacturers)
        
        # Get category
        category_name = med_data["category"]
        if category_name not in category_map:
            category_name = categories[0].name
        
        category = category_map[category_name]
        
        medicine = Medicine(
            name=med_data["name"],
            description=med_data["description"],
            dosage=med_data["dosage"],
            form=med_data["form"],
            batch_number=batch_number,
            cost_price=cost_price,
            selling_price=selling_price,
            quantity=quantity,
            minimum_stock=minimum_stock,
            manufacturer_id=manufacturer.id,
            category_id=category.id,
            purchase_date=purchase_date,
            expiry_date=expiry_date
        )
        
        db.session.add(medicine)
        medicines.append(medicine)
        
        status_indicators = []
        if medicine.is_low_stock:
            status_indicators.append("🔴 LOW STOCK")
        if medicine.days_to_expiry < 90:
            status_indicators.append("⚠️ EXPIRING SOON")
        if medicine.is_expired:
            status_indicators.append("❌ EXPIRED")
        
        status_text = " ".join(status_indicators) if status_indicators else "✅"
        
        print(f"Created: {medicine.name} {medicine.dosage} - {manufacturer.name}")
        print(f"   Cost: ₹{cost_price} | Selling: ₹{selling_price} | Qty: {quantity} | {status_text}")
    
    db.session.commit()
    return medicines

def seed_database():
    """Main seeding function with enhanced data"""
    print("🌱 Starting enhanced database seeding...")
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            print("\n📦 Creating categories...")
            categories = create_categories()
            print(f"✅ Created {len(categories)} categories")
            
            print("\n🏭 Creating manufacturers...")
            manufacturers = create_manufacturers()
            print(f"✅ Created {len(manufacturers)} manufacturers")
            
            print("\n💊 Creating enhanced medicines...")
            medicines = create_enhanced_medicines()
            print(f"✅ Created {len(medicines)} medicines")
            
            # Generate summary statistics
            total_medicines = Medicine.query.count()
            total_value = db.session.query(
                db.func.sum(Medicine.selling_price * Medicine.quantity)
            ).scalar() or 0
            
            low_stock_count = Medicine.query.filter(
                Medicine.quantity <= Medicine.minimum_stock
            ).count()
            
            expired_count = Medicine.query.filter(
                Medicine.expiry_date < date.today()
            ).count()
            
            expiring_soon_count = Medicine.query.filter(
                Medicine.expiry_date.between(
                    date.today(), 
                    date.today() + timedelta(days=90)
                )
            ).count()
            
            print(f"\n🎉 Enhanced database seeding completed successfully!")
            print(f"📊 Summary:")
            print(f"   - Categories: {MedicineCategory.query.count()}")
            print(f"   - Manufacturers: {Manufacturer.query.count()}")
            print(f"   - Medicines: {total_medicines}")
            print(f"   - Total Inventory Value: ₹{total_value:,.2f}")
            print(f"   - Low Stock Items: {low_stock_count}")
            print(f"   - Expired Items: {expired_count}")
            print(f"   - Expiring Soon (90 days): {expiring_soon_count}")
            
            if low_stock_count > 0 or expired_count > 0 or expiring_soon_count > 0:
                print(f"\n⚠️  Alerts:")
                if low_stock_count > 0:
                    print(f"   🔴 {low_stock_count} items need restocking")
                if expired_count > 0:
                    print(f"   ❌ {expired_count} items are expired")
                if expiring_soon_count > 0:
                    print(f"   ⚠️  {expiring_soon_count} items expiring within 90 days")
            
        except Exception as e:
            print(f"❌ Error during seeding: {str(e)}")
            db.session.rollback()
            return False
    
    return True

def clear_database():
    """Clear all data from the database"""
    print("🗑️  Clearing database...")
    
    with app.app_context():
        try:
            Medicine.query.delete()
            MedicineCategory.query.delete()
            Manufacturer.query.delete()
            db.session.commit()
            print("✅ Database cleared successfully!")
        except Exception as e:
            print(f"❌ Error clearing database: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed the enhanced chemist store database")
    parser.add_argument("--clear", action="store_true", help="Clear database before seeding")
    parser.add_argument("--clear-only", action="store_true", help="Only clear the database")
    
    args = parser.parse_args()
    
    if args.clear_only:
        clear_database()
    elif args.clear:
        clear_database()
        seed_database()
    else:
        seed_database()