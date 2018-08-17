#local imports
from flask import Flask

def create_app():   
    app = Flask(__name__)
    from .questions import questions as questions_blueprint
    app.register_blueprint(questions_blueprint)
    from .users import users as users_blueprints
    app.register_blueprint(users_blueprints)
    return app
    
app = create_app()
    