#!/usr/bin/env python3
"""
Quick migration script to fix the price column issue
Run this before using the enhanced seed script
"""

import os
import sys
from datetime import datetime, date

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db
from sqlalchemy import text

def fix_database_schema():
    """Fix the database schema to work with enhanced model"""
    print("🔧 Fixing database schema...")
    
    with app.app_context():
        try:
            # First, let's see what columns exist
            print("📋 Checking current table structure...")
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'medicines' 
                ORDER BY ordinal_position
            """))
            
            existing_columns = {row[0]: {'type': row[1], 'nullable': row[2]} for row in result.fetchall()}
            print(f"Found columns: {list(existing_columns.keys())}")
            
            # Add new columns if they don't exist
            new_columns = [
                ("description", "TEXT"),
                ("purchase_date", "DATE"),
                ("expiry_date", "DATE"),
                ("cost_price", "NUMERIC(10,2)"),
                ("selling_price", "NUMERIC(10,2)"),
                ("minimum_stock", "INTEGER DEFAULT 10"),
                ("dosage", "VARCHAR(50)"),
                ("form", "VARCHAR(30)"),
                ("manufacturer_id", "INTEGER"),
                ("category_id", "INTEGER")
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in existing_columns:
                    print(f"➕ Adding column: {col_name}")
                    db.session.execute(text(f"ALTER TABLE medicines ADD COLUMN {col_name} {col_type}"))
                else:
                    print(f"✅ Column exists: {col_name}")
            
            # Update manufacturer and category relationships
            print("🔗 Updating manufacturer relationships...")
            db.session.execute(text("""
                UPDATE medicines 
                SET manufacturer_id = m.id 
                FROM manufacturers m 
                WHERE medicines.manufacturer = m.name 
                AND medicines.manufacturer_id IS NULL
            """))
            
            print("🔗 Updating category relationships...")
            db.session.execute(text("""
                UPDATE medicines 
                SET category_id = c.id 
                FROM medicine_categories c 
                WHERE medicines.category = c.name 
                AND medicines.category_id IS NULL
            """))
            
            # Set selling_price from existing price column
            if 'price' in existing_columns and 'selling_price' in existing_columns:
                print("💰 Migrating price to selling_price...")
                db.session.execute(text("""
                    UPDATE medicines 
                    SET selling_price = price 
                    WHERE selling_price IS NULL AND price IS NOT NULL
                """))
            
            # Set default values for required fields
            print("📅 Setting default dates...")
            default_expiry = (date.today().replace(year=date.today().year + 2)).isoformat()
            default_purchase = date.today().isoformat()
            
            db.session.execute(text(f"""
                UPDATE medicines 
                SET 
                    expiry_date = COALESCE(expiry_date, '{default_expiry}'),
                    purchase_date = COALESCE(purchase_date, '{default_purchase}'),
                    description = COALESCE(description, ''),
                    minimum_stock = COALESCE(minimum_stock, 10),
                    dosage = COALESCE(dosage, ''),
                    form = COALESCE(form, '')
                WHERE expiry_date IS NULL OR purchase_date IS NULL
            """))
            
            # Make the old price column nullable or remove NOT NULL constraint
            if 'price' in existing_columns:
                print("🔧 Making old price column nullable...")
                try:
                    db.session.execute(text("ALTER TABLE medicines ALTER COLUMN price DROP NOT NULL"))
                except Exception as e:
                    print(f"⚠️  Could not modify price column: {e}")
            
            db.session.commit()
            print("✅ Database schema fixed successfully!")
            
            # Verify the fix
            count_result = db.session.execute(text("SELECT COUNT(*) FROM medicines"))
            medicine_count = count_result.scalar()
            print(f"📊 Current medicine count: {medicine_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error fixing schema: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = fix_database_schema()
    if success:
        print("\n🎉 Migration completed! You can now run the enhanced seed script.")
        print("Run: python enhanced_seed.py --clear")
    else:
        print("\n💡 If issues persist, you may need to backup your data and recreate the database.")