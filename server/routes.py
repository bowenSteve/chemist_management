from flask import request, jsonify, Blueprint
from models import db, Medicine, MedicineCategory, Manufacturer
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from sqlalchemy import and_, or_

# Create blueprint
api_bp = Blueprint('api', __name__)

# =============================================================================
# ENHANCED MEDICINE ROUTES
# =============================================================================

@api_bp.route('/medicines', methods=['GET'])
def get_all_medicines():
    """Get all medicines with enhanced filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filter parameters
        category_id = request.args.get('category_id', type=int)
        manufacturer_id = request.args.get('manufacturer_id', type=int)
        search = request.args.get('search')
        
        # Status filters
        expired = request.args.get('expired', type=bool)
        expiring_soon = request.args.get('expiring_soon', type=bool)  # Within 30 days
        low_stock = request.args.get('low_stock', type=bool)
        
        # Date filters
        purchase_date_from = request.args.get('purchase_date_from')
        purchase_date_to = request.args.get('purchase_date_to')
        
        query = Medicine.query
        
        # Apply filters
        if category_id:
            query = query.filter(Medicine.category_id == category_id)
        if manufacturer_id:
            query = query.filter(Medicine.manufacturer_id == manufacturer_id)
        if search:
            query = query.filter(
                or_(
                    Medicine.name.ilike(f'%{search}%'),
                    Medicine.description.ilike(f'%{search}%'),
                    Medicine.batch_number.ilike(f'%{search}%')
                )
            )
        
        # Status filters
        if expired:
            query = query.filter(Medicine.expiry_date < date.today())
        if expiring_soon:
            from datetime import timedelta
            soon_date = date.today() + timedelta(days=30)
            query = query.filter(
                and_(
                    Medicine.expiry_date >= date.today(),
                    Medicine.expiry_date <= soon_date
                )
            )
        if low_stock:
            query = query.filter(Medicine.quantity <= Medicine.minimum_stock)
        
        # Date range filters
        if purchase_date_from:
            from_date = datetime.strptime(purchase_date_from, '%Y-%m-%d').date()
            query = query.filter(Medicine.purchase_date >= from_date)
        if purchase_date_to:
            to_date = datetime.strptime(purchase_date_to, '%Y-%m-%d').date()
            query = query.filter(Medicine.purchase_date <= to_date)
        
        # Order by expiry date (closest first)
        query = query.order_by(Medicine.expiry_date.asc())
        
        # Paginate results
        medicines = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'medicines': [medicine.to_dict() for medicine in medicines.items],
            'total': medicines.total,
            'pages': medicines.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/medicines', methods=['POST'])
def create_medicine():
    """Create a new medicine with all required fields"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'name', 'batch_number', 'selling_price', 'quantity', 
            'manufacturer_id', 'category_id', 'expiry_date'
        ]
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate manufacturer exists
        manufacturer = Manufacturer.query.get(data['manufacturer_id'])
        if not manufacturer:
            return jsonify({'error': 'Manufacturer not found'}), 400
        
        # Validate category exists
        category = MedicineCategory.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Category not found'}), 400
        
        # Parse dates
        try:
            expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
            purchase_date = date.today()
            if 'purchase_date' in data and data['purchase_date']:
                purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Validate expiry date is in the future
        if expiry_date <= date.today():
            return jsonify({'error': 'Expiry date must be in the future'}), 400
        
        # Create new medicine
        medicine = Medicine(
            name=data['name'],
            description=data.get('description', ''),
            batch_number=data['batch_number'],
            selling_price=data['selling_price'],
            cost_price=data.get('cost_price'),
            quantity=data['quantity'],
            minimum_stock=data.get('minimum_stock', 10),
            manufacturer_id=data['manufacturer_id'],
            category_id=data['category_id'],
            dosage=data.get('dosage', ''),
            form=data.get('form', ''),
            purchase_date=purchase_date,
            expiry_date=expiry_date
        )
        
        db.session.add(medicine)
        db.session.commit()
        
        return jsonify({
            'message': 'Medicine created successfully',
            'medicine': medicine.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Medicine with this batch number already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/medicines/<int:medicine_id>', methods=['PUT'])
def update_medicine(medicine_id):
    """Update an existing medicine"""
    try:
        medicine = Medicine.query.get_or_404(medicine_id)
        data = request.get_json()
        
        # Update basic fields
        if 'name' in data:
            medicine.name = data['name']
        if 'description' in data:
            medicine.description = data['description']
        if 'batch_number' in data:
            medicine.batch_number = data['batch_number']
        if 'selling_price' in data:
            medicine.selling_price = data['selling_price']
        if 'cost_price' in data:
            medicine.cost_price = data['cost_price']
        if 'quantity' in data:
            medicine.quantity = data['quantity']
        if 'minimum_stock' in data:
            medicine.minimum_stock = data['minimum_stock']
        if 'dosage' in data:
            medicine.dosage = data['dosage']
        if 'form' in data:
            medicine.form = data['form']
        
        # Update relationships
        if 'manufacturer_id' in data:
            manufacturer = Manufacturer.query.get(data['manufacturer_id'])
            if not manufacturer:
                return jsonify({'error': 'Manufacturer not found'}), 400
            medicine.manufacturer_id = data['manufacturer_id']
        
        if 'category_id' in data:
            category = MedicineCategory.query.get(data['category_id'])
            if not category:
                return jsonify({'error': 'Category not found'}), 400
            medicine.category_id = data['category_id']
        
        # Update dates
        if 'expiry_date' in data:
            try:
                expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
                if expiry_date <= date.today():
                    return jsonify({'error': 'Expiry date must be in the future'}), 400
                medicine.expiry_date = expiry_date
            except ValueError:
                return jsonify({'error': 'Invalid expiry date format. Use YYYY-MM-DD'}), 400
        
        if 'purchase_date' in data:
            try:
                purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
                medicine.purchase_date = purchase_date
            except ValueError:
                return jsonify({'error': 'Invalid purchase date format. Use YYYY-MM-DD'}), 400
        
        medicine.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Medicine updated successfully',
            'medicine': medicine.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/medicines/alerts', methods=['GET'])
def get_medicine_alerts():
    """Get medicines that need attention (expired, expiring soon, low stock)"""
    try:
        from datetime import timedelta
        
        today = date.today()
        soon_date = today + timedelta(days=30)
        
        # Get expired medicines
        expired = Medicine.query.filter(Medicine.expiry_date < today).all()
        
        # Get medicines expiring soon (within 30 days)
        expiring_soon = Medicine.query.filter(
            and_(
                Medicine.expiry_date >= today,
                Medicine.expiry_date <= soon_date
            )
        ).all()
        
        # Get low stock medicines
        low_stock = Medicine.query.filter(
            Medicine.quantity <= Medicine.minimum_stock
        ).all()
        
        return jsonify({
            'alerts': {
                'expired': {
                    'count': len(expired),
                    'medicines': [med.to_dict() for med in expired]
                },
                'expiring_soon': {
                    'count': len(expiring_soon),
                    'medicines': [med.to_dict() for med in expiring_soon]
                },
                'low_stock': {
                    'count': len(low_stock),
                    'medicines': [med.to_dict() for med in low_stock]
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/medicines/reports/inventory', methods=['GET'])
def get_inventory_report():
    """Get comprehensive inventory report"""
    try:
        # Total medicines and value
        total_medicines = Medicine.query.count()
        total_value = db.session.query(
            db.func.sum(Medicine.selling_price * Medicine.quantity)
        ).scalar() or 0
        
        total_cost = db.session.query(
            db.func.sum(Medicine.cost_price * Medicine.quantity)
        ).filter(Medicine.cost_price.isnot(None)).scalar() or 0
        
        # Category breakdown
        category_stats = db.session.query(
            MedicineCategory.name,
            db.func.count(Medicine.id).label('count'),
            db.func.sum(Medicine.quantity).label('total_quantity'),
            db.func.sum(Medicine.selling_price * Medicine.quantity).label('value')
        ).join(Medicine).group_by(MedicineCategory.name).all()
        
        # Manufacturer breakdown
        manufacturer_stats = db.session.query(
            Manufacturer.name,
            db.func.count(Medicine.id).label('count'),
            db.func.sum(Medicine.quantity).label('total_quantity')
        ).join(Medicine).group_by(Manufacturer.name).all()
        
        return jsonify({
            'summary': {
                'total_medicines': total_medicines,
                'total_inventory_value': float(total_value),
                'total_cost_value': float(total_cost),
                'potential_profit': float(total_value - total_cost)
            },
            'by_category': [
                {
                    'category': stat.name,
                    'medicine_count': stat.count,
                    'total_quantity': stat.total_quantity,
                    'total_value': float(stat.value or 0)
                }
                for stat in category_stats
            ],
            'by_manufacturer': [
                {
                    'manufacturer': stat.name,
                    'medicine_count': stat.count,
                    'total_quantity': stat.total_quantity
                }
                for stat in manufacturer_stats
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Keep existing routes for backward compatibility
@api_bp.route('/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
    """Get a specific medicine by ID"""
    try:
        medicine = Medicine.query.get_or_404(medicine_id)
        return jsonify(medicine.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Medicine not found'}), 404

@api_bp.route('/medicines/<int:medicine_id>', methods=['DELETE'])
def delete_medicine(medicine_id):
    """Delete a medicine"""
    try:
        medicine = Medicine.query.get_or_404(medicine_id)
        db.session.delete(medicine)
        db.session.commit()
        
        return jsonify({'message': 'Medicine deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500