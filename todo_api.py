from flask import Blueprint, request, jsonify
from database import Session
from todo_db import User, Todo
from auth import basic_auth_required

api_bp = Blueprint("api", __name__)



@api_bp.route("/register", methods=["POST"])
def register():
    session = Session()
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password required"}), 400

    existing = session.query(User).filter_by(username=data["username"]).first()
    if existing:
        session.close()
        return jsonify({"message": "Username already exists"}), 400

    is_admin = True if data["username"] == "admin" else False

    new_user = User(
        username=data["username"],
        is_admin=is_admin
    )
    new_user.set_password(data["password"])

    session.add(new_user)
    session.commit()
    session.close()

    return jsonify({"message": "User registered"}), 201



@api_bp.route("/login", methods=["POST"])
def login():
    session = Session()
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password required"}), 400

    user = session.query(User).filter_by(username=data["username"]).first()

    if not user:
        session.close()
        return jsonify({"message": "User not found"}), 404

    if not user.check_password(data["password"]):
        session.close()
        return jsonify({"message": "Invalid password"}), 401

    session.close()

    return jsonify({
        "message": "Login successful",
        "role": "admin" if user.is_admin else "user"
    }), 200


@api_bp.route("/todo", methods=["POST"])
@basic_auth_required
def create_todo(current_user):
    session = Session()
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"message": "Task required"}), 400

    todo = Todo(task=data["task"], user_id=current_user.id)

    session.add(todo)
    session.commit()
    session.close()

    return jsonify({"message": "Todo created"}), 201



@api_bp.route("/todo", methods=["GET"])
@basic_auth_required
def get_todos(current_user):
    session = Session()

    if current_user.is_admin:
        todos = session.query(Todo).all()
    else:
        todos = session.query(Todo).filter_by(user_id=current_user.id).all()

    result = [
        {
            "id": t.id,
            "task": t.task,
            "user_id": t.user_id
        }
        for t in todos
    ]

    session.close()
    return jsonify(result), 200