from app import app, db
from flask import request, jsonify
from models import User

# GET /users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users]), 200

# POST /users
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        required_fields = ['username', 'email']
        for field in required_fields:
            if field not in data: 
                return jsonify({"error":f"{field} is required"}), 400

        new_user = User(username=data['username'], email=data['email'], password_hash="1234")
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500
    
# PATCH /users/<id>
@app.route('/api/users/<int:id>', methods=['PATCH'])
def update_user(id):
    try:
        data = request.get_json()
        user = User.query.get(id)
        if not user:
            return jsonify({"error":"User not found"}), 404

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password_hash' in data:
            user.password_hash = data['password_hash']

        db.session.commit()
        return jsonify(user.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500
    
# DELETE /users/<id>
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error":"User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500
    
