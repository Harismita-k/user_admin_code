from flask import Flask
from database import Base, engine
from todo_api import api_bp
from database import Session
app = Flask(__name__)

app.register_blueprint(api_bp)

Base.metadata.create_all(bind=engine)


@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()

if __name__ == "__main__":
    app.run(debug=True)