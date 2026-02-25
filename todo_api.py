from flask import jsonify, request, Blueprint
from todo_db import Register
from db import Session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from typing import Dict, Tuple, Any
from todo_db import Todo

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register() -> Tuple[Dict[Any,str],int]:
    try:
        session = Session()

        data : dict = request.get_json()

        if not data.get("user_name"):
            return jsonify({"message":"username is mandatory"}), 400
        
        if not data.get("password"):
            return jsonify({"message": "password is mandatory"}), 400
        
        hashed_password = generate_password_hash(data["password"])

        result : Register = Register(
            user_name = data["user_name"],
            hash_password = hashed_password,
        )

        session.add(result)
        session.commit()
        session.refresh(result)

        session.close()
        return jsonify({"message": "User Registration Successfully"}), 201
    
    except Exception as e:
        return jsonify({"error":"unexpected error", "details":str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login() -> Tuple[Dict[Any,str],int]:
    try:
        session = Session()

        user_data = session.query(Register).all()

        data : dict = request.get_json()

        if not data["user_name"]:
            return jsonify({"error":"username is mandatory"}), 400
            
        if not data["password"]:
            return jsonify({"error":"password is mandatory"}), 400

        user = session.query(Register).filter_by(user_name=data["user_name"]).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if not check_password_hash(user.hash_password, data["password"]):
            return jsonify({"message": "Invalid password"}), 401
        
        session.commit()

        access_token :str = create_access_token(identity=str(user.id))

        session.close()

        return jsonify({
            "access_token" : access_token, 
        }), 200
    
    except Exception as e:
        return jsonify({"error":"unexpected error", "details":str(e)}), 500



todo_bp = Blueprint("todo_work", __name__)

@todo_bp.route("/", methods=["POST"])
@jwt_required()
def handle_todo():
    session = Session()
    try:
        data = request.get_json()  
        current_user = get_jwt_identity()

        if "work" in data:

            new_work = Todo(
                user_id=current_user,
                work=data["work"],                     
                is_completed=data.get("is_completed", False)
            )

            session.add(new_work)
            session.commit()
            session.refresh(new_work)

            return jsonify({
                "message": "Todo Added",
                "id": new_work.id,
                "work": new_work.work,
                "is_completed": new_work.is_completed,
                "date": str(new_work.date)
            }), 201
        

        elif data.get("view") == True:

            todos = session.query(Todo).filter(
                Todo.user_id == current_user
            ).all()

            result = []
            for todo in todos:
                result.append({
                    "id": todo.id,
                    "work": todo.work,
                    "is_completed": todo.is_completed,
                    "date": str(todo.date)
                })

            return jsonify(result), 200


        else:
            return jsonify({"error": "Invalid payload"}), 400

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

    finally:
        session.close()