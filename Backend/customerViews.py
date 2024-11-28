from flask import Blueprint, request, jsonify
from .auth import role_required
from flask_login import current_user
from .models import User, Technician, Customer, Service, ServiceRequest
from . import mail
from flask_mail import Message

customerViews = Blueprint('customerViews', __name__)

@customerViews.route('/<id>')
@role_required('customer')
def home(id):
    services = Service.get_services()
    service_requests = ServiceRequest.get_service_request_byCustomer(id)
    return jsonify({"services":services, "service_requests": service_requests})

@customerViews.route('/seeprofessional/<sid>/<cid>')
@role_required('customer')
def seeProfessional(sid, cid):
    professionals = Technician.get_technician_for_user(cid,sid)    
    return jsonify({"professionals":professionals})

@customerViews.route('/bookProfessional/<pid>/<uid>', methods=['POST'])
# @role_required('customer')
def bookProfessional(pid, uid):
    customer = Customer.query.filter_by(user_id=uid).first()
    professional = Technician.query.filter_by(id=pid).first()
    service = Service.query.filter_by(id=professional.service_id).first()
    msg = Message(
        subject="New Service Request",
        recipients=[professional.email],
        body=f"New Service Request from {customer.name} for {service.name} at {customer.address}"
    )
    # print(msg)
    try:
        service_request = ServiceRequest(customer_id=customer.user_id, technician_id=professional.id, service_id=service.id)
        service_request.register()
        mail.send(msg)
    except Exception as e:
        print(e)
        return jsonify({"message":str(e)}),500
    return jsonify({"message":"booked"})

@customerViews.route('/complete/<id>', methods=['POST'])
@role_required('customer')
def complete(id):
    remarks = request.json.get('remarks')
    # print(remarks,id)
    # return jsonify({"message":"request completed"}),200
    try:
        ServiceRequest.complete(id, remarks)
        return jsonify({"message":"request completed"}),200
    except Exception as e:
        return jsonify({"message":"request not completed"}),400
    
@customerViews.route('/cancel/<id>', methods=['POST'])
@role_required('customer')
def cancel(id):
    remarks = "Canceled by Customer"
    # print(remarks, id)
    # return jsonify({"message":"request completed"}),200
    try:
        ServiceRequest.reject(id, remarks)
        return jsonify({"message":"request cancelled"}),200
    except Exception as e:
        return jsonify({"message":"request not cancelled"}),400
    
@customerViews.route('/search', methods=['GET', 'POST'])
@role_required('customer')
def search():
    data = request.json
    query = data.get('query')
    searchBy = data.get('searchBy')
    id = data.get('id')
    if searchBy == 'Technician':
        technicians = Technician.search_cust(query, id)
        return jsonify({"technicians":technicians}),200
    elif searchBy == 'Service':
        services = Service.search(query)
        return jsonify({"services":services}),200
    elif searchBy == 'Service Request':
        service_requests = ServiceRequest.search_cust(query, id)
        return jsonify({"service_requests":service_requests}),200
    return jsonify({"message":"search not found"})

@customerViews.route('/summary/<id>', methods=['GET'])
@role_required('customer')
def summary(id):
    request_summary = ServiceRequest.get_request_summary_cust(id)
    if not request_summary:
        return jsonify({"message":"no data found"})
    # request_summary[0]['accepted_requests'] += request_summary[0]['completed_requests']
    return jsonify({"request_data":list(request_summary[0].values()),"request_labels":list(request_summary[0].keys())})

@customerViews.route('/profile/<id>', methods=['GET','POST'])
@role_required('customer')
def profile(id):
    user = Customer.get_customer(id)
    # print(user)
    return jsonify({"user":user})

@customerViews.route('/update/<id>', methods=['POST'])
@role_required('customer')
def update(id):
    data = request.json.get('data')
    # print(data)
    # return jsonify({"message":"user updated"}),200
    try:
        Customer.update(id, data)
        return jsonify({"message":"user updated"}),200
    except Exception as e:
        print(e)
        return jsonify({"message":"user not updated"}),400