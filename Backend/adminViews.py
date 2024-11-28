from flask import Blueprint, jsonify
from .auth import role_required
from flask import request
from .models import User, Technician, Customer, Service, ServiceRequest
# from flask_jwt_extended import jwt_required, get_jwt_identity

adminViews = Blueprint('adminViews', __name__)

@adminViews.route('/')
@role_required('admin')
def home():
    services = Service.get_services()
    technicians = Technician.get_technicians()
    service_requests = ServiceRequest.get_service_requests()
    return jsonify({"services":services, "technicians":technicians, "service_requests":service_requests})

@adminViews.route('/newService', methods=['POST'])
@role_required('admin')
def newService():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    time = data.get('time')
    try:
        service = Service(name=name, description=description, price=price, time_required=time)
        service.register()
        return jsonify({"message":"service added"}),200
    except:
        return jsonify({"message":"service not added"}),400
    
@adminViews.route('/editServices/<id>', methods=['GET','POST'])
@role_required('admin')
def editService(id):
    service = Service.get_service(id)
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        time = data.get('time_required')
        try:
            Service.update(id=id, name=name, description=description, price=price, time_required=time)
            return jsonify({"message":"service updated"}),200
        except Exception as e:
            return jsonify({"message":"service not updated"}),400
    return jsonify({"service":service})

@adminViews.route('/deleteService/<id>',methods=['DELETE'])
@role_required('admin')
def deleteService(id):
    try:
        Service.delete(id)
        return jsonify({"message":"service deleted"}),200
    except Exception as e:
        return jsonify({"message":"service not deleted"}),400
    
@adminViews.route('/suspendTechnician/<id>',methods=['POST'])
@role_required('admin')
def suspendTechnician(id):
    try:
        Technician.suspend(id)
        return jsonify({"message":"technician suspended"}),200
    except Exception as e:
        return jsonify({"message":"technician not suspended"}),400
    
@adminViews.route('/activateTechnician/<id>',methods=['POST'])
@role_required('admin')
def activateTechnician(id):
    try:
        Technician.activate(id)
        return jsonify({"message":"technician activated"}),200
    except Exception as e:
        return jsonify({"message":"technician not activated"}),400
    
@adminViews.route('/search', methods=['GET', 'POST'])
@role_required('admin')
def search():
    data = request.json
    query = data.get('query')
    searchBy = data.get('searchBy')
    if searchBy == 'Technician':
        technicians = Technician.search(query)
        return jsonify({"technicians":technicians}),200
    elif searchBy == 'Service':
        services = Service.search(query)
        return jsonify({"services":services}),200
    elif searchBy == 'Service Request':
        service_requests = ServiceRequest.search(query)
        return jsonify({"service_requests":service_requests}),200
    elif searchBy == 'customer':
        customers = Customer.search(query)
        return jsonify({"customers":customers}),200
    return jsonify({"message":"search not found"})

@adminViews.route('/addRequest', methods=['GET','POST'])
@role_required('admin')
def addRequest():
    users = Customer.get_customers()
    technicians = Technician.get_technicians()
    services = Service.get_services()

    return jsonify({"users":users, "technicians":technicians, "services":services})

@adminViews.route('/summary',methods=['GET'])
@role_required('admin')
def summary():
    service_summary = ServiceRequest.get_service_summary()
    request_summary = ServiceRequest.get_request_summarys()
    serviceLables = []
    serviceData = []
    if not service_summary or not request_summary:
        return jsonify({"message":"no data found"})
    for service in service_summary:
        serviceLables.append(service['name'])
        serviceData.append(service['booking_count'])
    request_summary[0]['accepted_requests'] += request_summary[0]['completed_requests']
    return jsonify({"service_lables":serviceLables, "service_data":serviceData, "tech_data":list(request_summary[0].values()), "tech_lables":list(request_summary[0].keys()) })