from flask import request, jsonify, Blueprint
from models import db, Medicine, MedicineCategory, Manufacturer
from sqlalchemy.exc import IntegrityError

# Create blueprint
api_bp = Blueprint('api', __name__)

# =============================================================================
# MEDICINE ROUTES
# =============================================================================

@api_bp.route('/medicines', methods=['GET'])
def get_all_medicines():
    """Get all medicines with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        manufacturer = request.args.get('manufacturer')
        search = request.args.get('search')
        
        query = Medicine.query
        
        # Apply filters
        if category:
            query = query.filter(Medicine.category.ilike(f'%{category}%'))
        if manufacturer:
            query = query.filter(Medicine.manufacturer.ilike(f'%{manufacturer}%'))
        if search:
            query = query.filter(Medicine.name.ilike(f'%{search}%'))
        
        # Paginate results
        medicines = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'medicines': [medicine.to_dict() for medicine in medicines.items],
            'total': medicines.total,
            'pages': medicines.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
    """Get a specific medicine by ID"""
    try:
        medicine = Medicine.query.get_or_404(medicine_id)
        return jsonify(medicine.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Medicine not found'}), 404

@api_bp.route('/medicines', methods=['POST'])
def create_medicine():
    """Create a new medicine"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'batch_number', 'price', 'quantity', 'manufacturer', 'category']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new medicine
        medicine = Medicine(
            name=data['name'],
            batch_number=data['batch_number'],
            price=data['price'],
            quantity=data['quantity'],
            manufacturer=data['manufacturer'],
            category=data['category']
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
        
        # Update fields if provided
        if 'name' in data:
            medicine.name = data['name']
        if 'batch_number' in data:
            medicine.batch_number = data['batch_number']
        if 'price' in data:
            medicine.price = data['price']
        if 'quantity' in data:
            medicine.quantity = data['quantity']
        if 'manufacturer' in data:
            medicine.manufacturer = data['manufacturer']
        if 'category' in data:
            medicine.category = data['category']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Medicine updated successfully',
            'medicine': medicine.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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

@api_bp.route('/medicines/<int:medicine_id>/quantity', methods=['PATCH'])
def update_medicine_quantity(medicine_id):
    """Update medicine quantity (add or subtract stock)"""
    try:
        medicine = Medicine.query.get_or_404(medicine_id)
        data = request.get_json()
        
        if 'quantity' not in data:
            return jsonify({'error': 'Quantity is required'}), 400
        
        action = data.get('action', 'set')  # 'set', 'add', 'subtract'
        quantity = int(data['quantity'])
        
        if action == 'add':
            medicine.quantity += quantity
        elif action == 'subtract':
            if medicine.quantity < quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            medicine.quantity -= quantity
        else:  # set
            medicine.quantity = quantity
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quantity updated successfully',
            'medicine': medicine.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/medicines/low-stock', methods=['GET'])
def get_low_stock_medicines():
    """Get medicines with low stock (quantity <= threshold)"""
    try:
        threshold = request.args.get('threshold', 10, type=int)
        medicines = Medicine.query.filter(Medicine.quantity <= threshold).all()
        
        return jsonify({
            'low_stock_medicines': [medicine.to_dict() for medicine in medicines],
            'count': len(medicines)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================================================
# CATEGORY ROUTES
# =============================================================================

@api_bp.route('/categories', methods=['GET'])
def get_all_categories():
    """Get all medicine categories"""
    try:
        categories = MedicineCategory.query.all()
        return jsonify({
            'categories': [category.to_dict() for category in categories],
            'count': len(categories)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category by ID"""
    try:
        category = MedicineCategory.query.get_or_404(category_id)
        return jsonify(category.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Category not found'}), 404

@api_bp.route('/categories', methods=['POST'])
def create_category():
    """Create a new medicine category"""
    try:
        data = request.get_json()
        
        if 'name' not in data or not data['name']:
            return jsonify({'error': 'Category name is required'}), 400
        
        category = MedicineCategory(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Category with this name already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================================================
# MANUFACTURER ROUTES
# =============================================================================

@api_bp.route('/manufacturers', methods=['GET'])
def get_all_manufacturers():
    """Get all manufacturers"""
    try:
        manufacturers = Manufacturer.query.all()
        return jsonify({
            'manufacturers': [manufacturer.to_dict() for manufacturer in manufacturers],
            'count': len(manufacturers)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/manufacturers', methods=['POST'])
def create_manufacturer():
    """Create a new manufacturer"""
    try:
        data = request.get_json()
        
        if 'name' not in data or not data['name']:
            return jsonify({'error': 'Manufacturer name is required'}), 400
        
        manufacturer = Manufacturer(
            name=data['name'],
            contact_info=data.get('contact_info', ''),
            address=data.get('address', '')
        )
        
        db.session.add(manufacturer)
        db.session.commit()
        
        return jsonify({
            'message': 'Manufacturer created successfully',
            'manufacturer': manufacturer.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Manufacturer with this name already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================================================
# UTILITY ROUTES
# =============================================================================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'Chemist Store API is running'
    }), 200

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        total_medicines = Medicine.query.count()
        total_categories = MedicineCategory.query.count()
        total_manufacturers = Manufacturer.query.count()
        low_stock_count = Medicine.query.filter(Medicine.quantity <= 10).count()
        
        return jsonify({
            'total_medicines': total_medicines,
            'total_categories': total_categories,
            'total_manufacturers': total_manufacturers,
            'low_stock_items': low_stock_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500