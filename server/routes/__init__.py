from flask import Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

api_bp = Blueprint('api', __name__)

@api_bp.route('/test', methods=['GET'])
def test():
    return jsonify(message="Hello, World!")