from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime, date

db = SQLAlchemy()

class Medicine(db.Model):
    __tablename__ = 'medicines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    batch_number = db.Column(db.String(50), nullable=False)
    
    # Keep old price column for compatibility (make it nullable)
    price = db.Column(Numeric(10, 2), nullable=True)
    
    # New price columns
    cost_price = db.Column(Numeric(10, 2))
    selling_price = db.Column(Numeric(10, 2), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False, default=0)
    minimum_stock = db.Column(db.Integer, default=10)
    
    # Keep old string fields for compatibility
    manufacturer = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    
    # New relationship fields
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'), nullable=True)
    manufacturer_rel = db.relationship('Manufacturer', backref='medicines')
    
    category_id = db.Column(db.Integer, db.ForeignKey('medicine_categories.id'), nullable=True)
    category_rel = db.relationship('MedicineCategory', backref='medicines')
    
    # New fields
    dosage = db.Column(db.String(50), default='')
    form = db.Column(db.String(30), default='')
    purchase_date = db.Column(db.Date, nullable=True, default=date.today)
    expiry_date = db.Column(db.Date, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Medicine {self.name} - Batch: {self.batch_number}>'
    
    @property
    def is_expired(self):
        """Check if medicine is expired"""
        if self.expiry_date:
            return self.expiry_date < date.today()
        return False
    
    @property
    def days_to_expiry(self):
        """Days until expiry (negative if expired)"""
        if self.expiry_date:
            return (self.expiry_date - date.today()).days
        return None
    
    @property
    def is_low_stock(self):
        """Check if stock is below minimum level"""
        return self.quantity <= self.minimum_stock
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.cost_price and self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0
    
    @property
    def effective_manufacturer(self):
        """Get manufacturer name from relationship or string field"""
        if self.manufacturer_rel:
            return self.manufacturer_rel.name
        return self.manufacturer or "Unknown"
    
    @property
    def effective_category(self):
        """Get category name from relationship or string field"""
        if self.category_rel:
            return self.category_rel.name
        return self.category or "Unknown"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description or '',
            'batch_number': self.batch_number,
            'quantity': self.quantity,
            'cost_price': float(self.cost_price) if self.cost_price else None,
            'selling_price': float(self.selling_price),
            'price': float(self.price) if self.price else float(self.selling_price),  # Backward compatibility
            'minimum_stock': self.minimum_stock,
            'dosage': self.dosage or '',
            'form': self.form or '',
            
            # Manufacturer and category (prefer relationships)
            'manufacturer': self.effective_manufacturer,
            'category': self.effective_category,
            'manufacturer_info': {
                'id': self.manufacturer_rel.id if self.manufacturer_rel else None,
                'name': self.effective_manufacturer
            },
            'category_info': {
                'id': self.category_rel.id if self.category_rel else None,
                'name': self.effective_category
            },
            
            # Dates
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            
            # Computed properties
            'is_expired': self.is_expired,
            'days_to_expiry': self.days_to_expiry,
            'is_low_stock': self.is_low_stock,
            'profit_margin': round(self.profit_margin, 2)
        }

class MedicineCategory(db.Model):
    __tablename__ = 'medicine_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'medicine_count': len(self.medicines) if hasattr(self, 'medicines') else 0
        }

class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    contact_info = db.Column(db.String(200))
    address = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Manufacturer {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_info': self.contact_info,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'medicine_count': len(self.medicines) if hasattr(self, 'medicines') else 0
        }