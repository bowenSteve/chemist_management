from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt
from datetime import timedelta
from flask_cors import CORS
from routes import api_bp,db


app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/chemistdb"



migrate = Migrate(app, db)
db.init_app(app)

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
