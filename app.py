import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/spendtrack'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'spendtrack-secret-key-2024'

    db.init_app(app)
    jwt.init_app(app)

    from routes.auth import auth_bp
    from routes.expenses import expenses_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(expenses_bp, url_prefix='/expenses')

    with app.app_context():
        db.create_all()
        print('✅ Database tables created!')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
