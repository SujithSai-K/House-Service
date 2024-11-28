from flask import Blueprint, jsonify, request
from . import login_manager
from flask_login import login_required, login_user, logout_user, current_user
from .models import User, Customer, Technician, Service
from functools import wraps
from datetime import date
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)


roles_permissions = {
    'admin': ['admin', 'customer', 'technician'],
    'customer': ['customer'],
    'technician': ['technician']
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
def login():
    data = request.json
    u_name = data.get('username')
    pswd = data.get('password')
    user = User.query.filter_by(username = u_name).first()
    if user and pswd == user.password:
        if user.role == 'technician':
            technician = Technician.query.filter_by(user_id=user.id).first()
            if technician.status == 'Suspended':
                return jsonify({"message":"Your account is suspended please contact admin"}),401
        login_user(user)
        access_token = create_access_token(identity={'username':u_name, 'role':user.role})
        return jsonify({'access_token':access_token, 'role':user.role, 'id':user.id}),200
    else:
        return jsonify({"message":"Invalid username or password"}),401

@auth.route('/add_admin',methods=['GET','POST'])
def add_user():
    if request.method=='POST':
        u_name = request.json['u_name']
        pswd = request.json['pswd']
        role = request.json['role']
        new_user = User(username=u_name, password=pswd, role=role)
        new_user.register()
        return "user added"

    return jsonify({"message":"Add Admin"})


@auth.route('/user_registration', methods = ['GET','POST'])
def user_registration():
    data = request.json
    u_name = data.get('username')
    user = User.query.filter_by(username = u_name).first()
    if not user:
        pswd = data.get('password')
        name = data.get('name')
        gender = data.get('gender')
        email = data.get('email')
        dob = data.get('dob')
        dob = date.fromisoformat(dob)
        phone = data.get('phone')
        address = data.get('address')
        try:
            new_user = User(username=u_name, password=pswd, role="customer")
            new_user.register()
            new_customer = Customer(name=name, email=email, gender=gender, dob=dob, phone=phone, address=address, user_id=new_user.id)
            new_customer.register()
        except Exception as e:
            return jsonify({"message":str(e)}),500
        return jsonify({"message":"registration Successful !!!"}),200
    else:
        return jsonify({"message":"username already exists"}),409


@auth.route('/technician_registration', methods = ['GET', 'POST'])
def technician_registration():
    services = Service.get_services()
    if request.method=='POST':
       data = request.json
       username = data.get('username')
       if User.query.filter_by(username = username).first():
           return jsonify({"message":"username already exists"}),409
       email = data.get('email')
       password = data.get('password')
       name = data.get('name')
       gender = data.get('gender')
       age = data.get('age')
       service_id = data.get('service_id')
       experience = data.get('experience')
       address = data.get('address')
       try:
           new_user = User(username=username, password=password, role="technician")
           new_user.register()
           new_technician = Technician(name=name,email = email, gender=gender, age=age, service_id=service_id, experience=experience, address=address, user_id=new_user.id)
           new_technician.register()

       except Exception as e:
           return jsonify({"message":str(e)}),500
       return jsonify({"message":"registration Successful !!!"}),200

    return jsonify(services)


@auth.route('/logout')
def logout():
    logout_user()
    return jsonify({"message":"logout successful!!"})


@auth.route('/test')
def test():
    return jsonify({"message":"test successful!!"})

def role_required(required_permission):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            identity = get_jwt_identity()
            role = identity.get("role")
            if role not in roles_permissions or required_permission not in roles_permissions[role]:
                return jsonify({"message": "Permission denied"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper