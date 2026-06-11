from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    currency_code = db.Column(db.String(10), default='GBP')
    currency_symbol = db.Column(db.String(5), default='£')
    budget = db.Column(db.Float, default=1700)
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    emoji = db.Column(db.String(10), default='💸')
    color = db.Column(db.String(20), default='#F0EEFF')
    date = db.Column(db.String(50), default='Today')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
