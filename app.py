from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="Templates", static_folder="Statics")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/disk/Blog_app_db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    database.init_app(app)
    
    from routes import register_routes
    register_routes(app)
    
    migrate = Migrate(app, database)
    
    return app
    
    
    