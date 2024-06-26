from .config import config_dict
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from typing import Literal

# instantiate the extensions
db = SQLAlchemy()


def create_app(config_name: Literal["default","testing","production","development"]="default") -> Flask:
    """ create a flask app instance """
    app = Flask(__name__,static_url_path="/static")

    # App Configuration
    app.config.from_object(config_dict[config_name])

    # initalize extensions 
    db.init_app(app)

    # Allow cors
    CORS(app)
    CORS(app, resources={
        r"/*":{
        "origins":"*",
        }
    })

    # register blueprints
    from app.routes.chat import chat_router_pb, message_router_pb,root_router_pb,prompt_router_pb
    app.register_blueprint(root_router_pb)
    app.register_blueprint(chat_router_pb)
    app.register_blueprint(message_router_pb)
    app.register_blueprint(prompt_router_pb)

    return app





