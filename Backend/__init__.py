from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
db_name = "HouseServices.db"
login_manager = LoginManager()
jwt = JWTManager()
mail = Mail()

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '22F3001035'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''
    app.config['MAIL_DEFAULT_SENDER'] = ''

    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    jwt.init_app(app)
    mail.init_app(app)

    from .adminViews import adminViews
    from .customerViews import customerViews
    from .technicianViews import technicianViews
    from .auth import auth 
    from .models import User, Technician, Customer, Service, ServiceRequest

    app.register_blueprint(adminViews, url_prefix='/admin')
    app.register_blueprint(customerViews, url_prefix='/customer')
    app.register_blueprint(technicianViews, url_prefix='/technician')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()



    return app
