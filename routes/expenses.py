from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Expense

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.created_at.desc()).all()
    return jsonify([{
        'id': e.id,
        'label': e.label,
        'category': e.category,
        'amount': e.amount,
        'emoji': e.emoji,
        'color': e.color,
        'date': e.date,
        'created_at': str(e.created_at)
    } for e in expenses]), 200

@expenses_bp.route('/', methods=['POST'])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()
    data = request.get_json()

    expense = Expense(
        user_id=user_id,
        label=data.get('label'),
        category=data.get('category'),
        amount=data.get('amount'),
        emoji=data.get('emoji', '💸'),
        color=data.get('color', '#F0EEFF'),
        date=data.get('date', 'Today')
    )
    db.session.add(expense)
    db.session.commit()

    return jsonify({
        'id': expense.id,
        'label': expense.label,
        'category': expense.category,
        'amount': expense.amount,
        'emoji': expense.emoji,
        'color': expense.color,
        'date': expense.date
    }), 201

@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    if not expense:
        return jsonify({'error': 'Expense not found'}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted'}), 200
