from flask import Blueprint, request, jsonify
from database import Session
from todo_db import User, Todo
from auth import basic_auth_required, admin_required

api_bp = Blueprint("api", __name__)


@api_bp.route("/register", methods=["POST"])
def register():
    session = Session()
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password required"}), 400

    existing = session.query(User).filter_by(username=data["username"]).first()
    if existing:
        return jsonify({"message": "Username already exists"}), 400

    
    new_user = User(username=data["username"])
    new_user.set_password(data["password"])

    session.add(new_user)
    session.commit()

    return jsonify({"message": "User registered"}), 201


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

    return ({"message": "Todo created"}), 201


@api_bp.route("/todo", methods=["GET"])
@basic_auth_required
def get_user_todos(current_user):
    session = Session()

    todos = session.query(Todo).filter_by(user_id=current_user.id).all()

    return jsonify([
        {"id": t.id, "task": t.task}
        for t in todos
    ]), 200


@api_bp.route("/admin/todos", methods=["GET"])
@admin_required
def get_all_todos(current_user):
    session = Session()

    todos = session.query(Todo).all()

    return jsonify([
        {
            "id": t.id,
            "task": t.task,
            "user_id": t.user_id
        }
        for t in todos
    ]), 200