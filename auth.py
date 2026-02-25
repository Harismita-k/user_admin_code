from flask import request, Response, jsonify
from functools import wraps
from database import session
from todo_db import User


def authenticate():
    return Response(
        "Authentication Required",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )


def check_auth(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return authenticate()

        user = check_auth(auth.username, auth.password)
        if not user:
            return authenticate()

        return f(user, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return authenticate()

        user = check_auth(auth.username, auth.password)
        if not user:
            return authenticate()

        if not user.is_admin:
            return jsonify({"message": "Admin access required"}), 403

        return f(user, *args, **kwargs)

    return decorated