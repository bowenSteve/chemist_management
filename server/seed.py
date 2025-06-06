#!/usr/bin/env python3

import os
import sys
from datetime import datetime
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Medicine, MedicineCategory, Manufacturer

def create_categories():
    """Create medicine categories"""
    categories_data = [
        {"name": "Tablets", "description": "Solid dosage forms"},
        {"name": "Capsules", "description": "Encapsulated medicines"},
        {"name": "Syrups", "description": "Liquid medicines"},
        {"name": "Injections", "description": "Injectable medicines"},
        {"name": "Ointments", "description": "Topical applications"},
        {"name": "Drops", "description": "Eye and ear drops"},
        {"name": "Inhalers", "description": "Respiratory medicines"},
        {"name": "Powders", "description": "Powder formulations"}
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
    """Create manufacturers"""
    manufacturers_data = [
        {
            "name": "Cipla Limited",
            "contact_info": "+91-22-2482-6000",
            "address": "Cipla House, Peninsula Business Park, Mumbai, India"
        },
        {
            "name": "Sun Pharmaceutical",
            "contact_info": "+91-22-4324-4324",
            "address": "Sun House, 201 B/1, Western Express Highway, Mumbai, India"
        },
        {
            "name": "Dr. Reddy's Laboratories",
            "contact_info": "+91-40-4900-2900",
            "address": "8-2-337, Road No. 3, Banjara Hills, Hyderabad, India"
        },
        {
            "name": "Lupin Pharmaceuticals",
            "contact_info": "+91-22-6640-2323",
            "address": "Kalina, Santacruz East, Mumbai, India"
        },
        {
            "name": "Aurobindo Pharma",
            "contact_info": "+91-40-6672-5000",
            "address": "Galaxy, Pragati Maidan, Hyderabad, India"
        },
        {
            "name": "Cadila Healthcare",
            "contact_info": "+91-79-2665-9999",
            "address": "Zydus Tower, Satellite Cross Roads, Ahmedabad, India"
        },
        {
            "name": "Glenmark Pharmaceuticals",
            "contact_info": "+91-22-4018-9999",
            "address": "B/2, Mahalaxmi Chambers, Mumbai, India"
        },
        {
            "name": "Torrent Pharmaceuticals",
            "contact_info": "+91-79-2665-3000",
            "address": "Torrent House, Off Ashram Road, Ahmedabad, India"
        }
    ]
    
    manufacturers = []
    for mfg_data in manufacturers_data:
        manufacturer = Manufacturer.query.filter_by(name=mfg_data["name"]).first()
        if not manufacturer:
            manufacturer = Manufacturer(
                name=mfg_data["name"],
                contact_info=mfg_data["contact_info"],
                address=mfg_data["address"]
            )
            db.session.add(manufacturer)
            manufacturers.append(manufacturer)
        else:
            manufacturers.append(manufacturer)
    
    db.session.commit()
    return manufacturers

def create_medicines():
    """Create 20 random medicines"""
    medicines_data = [
        {"name": "Paracetamol 500mg", "category": "Tablets", "price_range": (15, 25)},
        {"name": "Aspirin 75mg", "category": "Tablets", "price_range": (20, 30)},
        {"name": "Ibuprofen 400mg", "category": "Tablets", "price_range": (25, 35)},
        {"name": "Amoxicillin 500mg", "category": "Capsules", "price_range": (80, 120)},
        {"name": "Cetirizine 10mg", "category": "Tablets", "price_range": (40, 60)},
        {"name": "Cough Syrup", "category": "Syrups", "price_range": (60, 90)},
        {"name": "Multivitamin Syrup", "category": "Syrups", "price_range": (150, 200)},
        {"name": "Insulin Injection", "category": "Injections", "price_range": (300, 500)},
        {"name": "Betadine Ointment", "category": "Ointments", "price_range": (45, 65)},
        {"name": "Eye Drops", "category": "Drops", "price_range": (80, 120)},
        {"name": "Salbutamol Inhaler", "category": "Inhalers", "price_range": (200, 300)},
        {"name": "Omeprazole 20mg", "category": "Capsules", "price_range": (50, 80)},
        {"name": "Metformin 500mg", "category": "Tablets", "price_range": (30, 50)},
        {"name": "Atorvastatin 10mg", "category": "Tablets", "price_range": (100, 150)},
        {"name": "Amlodipine 5mg", "category": "Tablets", "price_range": (35, 55)},
        {"name": "Azithromycin 250mg", "category": "Tablets", "price_range": (150, 200)},
        {"name": "Diclofenac Gel", "category": "Ointments", "price_range": (70, 100)},
        {"name": "Loratadine 10mg", "category": "Tablets", "price_range": (45, 70)},
        {"name": "Vitamin D3 Powder", "category": "Powders", "price_range": (120, 180)},
        {"name": "Iron Tablets", "category": "Tablets", "price_range": (25, 40)},
        {"name": "Calcium Carbonate", "category": "Tablets", "price_range": (35, 55)},
        {"name": "Antacid Syrup", "category": "Syrups", "price_range": (40, 60)}
    ]
    
    # Get all categories and manufacturers
    categories = MedicineCategory.query.all()
    manufacturers = Manufacturer.query.all()
    
    category_map = {cat.name: cat for cat in categories}
    
    medicines = []
    
    for i, med_data in enumerate(medicines_data[:20]):  # Limit to 20 medicines
        # Check if medicine already exists
        existing = Medicine.query.filter_by(name=med_data["name"]).first()
        if existing:
            continue
            
        # Generate random data
        batch_number = f"B{2024}{str(i+1).zfill(3)}"
        price = round(random.uniform(med_data["price_range"][0], med_data["price_range"][1]), 2)
        quantity = random.randint(10, 500)
        manufacturer = random.choice(manufacturers)
        
        # Get category, fallback to first category if not found
        category_name = med_data["category"]
        if category_name not in category_map:
            category_name = categories[0].name
        
        medicine = Medicine(
            name=med_data["name"],
            batch_number=batch_number,
            price=price,
            quantity=quantity,
            manufacturer=manufacturer.name,
            category=category_name
        )
        
        db.session.add(medicine)
        medicines.append(medicine)
        print(f"Created: {medicine.name} - {manufacturer.name} - ₹{price} - Qty: {quantity}")
    
    db.session.commit()
    return medicines

def seed_database():
    """Main seeding function"""
    print("🌱 Starting database seeding...")
    
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
            
            print("\n💊 Creating medicines...")
            medicines = create_medicines()
            print(f"✅ Created {len(medicines)} medicines")
            
            print(f"\n🎉 Database seeding completed successfully!")
            print(f"📊 Summary:")
            print(f"   - Categories: {MedicineCategory.query.count()}")
            print(f"   - Manufacturers: {Manufacturer.query.count()}")
            print(f"   - Medicines: {Medicine.query.count()}")
            
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
    
    parser = argparse.ArgumentParser(description="Seed the chemist store database")
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