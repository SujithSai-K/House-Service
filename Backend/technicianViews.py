from flask import Blueprint,jsonify
from .auth import role_required
from .models import ServiceRequest, Technician, Service
from flask import request

technicianViews = Blueprint('technicianViews', __name__)

@technicianViews.route('/<id>')
@role_required('technician')
def home(id):
    technician = Technician.query.filter_by(user_id=id).first()
    service_requests = ServiceRequest.get_service_request_byTechnician(technician.id)
    cr=[]
    pr=[]
    for request in service_requests:
        if request['status'] == 'Completed' or request['status'] == 'Rejected':
            cr.append(request)
        else:
            pr.append(request)
    # return jsonify(message="hello"),200
    return jsonify({"pending_requests": pr, "completed_requests":cr}),200

@technicianViews.route('/acceptRequest/<id>', methods=['POST'])
@role_required('technician')
def acceptRequest(id):
    try:
        ServiceRequest.accept(id)
        return jsonify({"message":"request accepted"}),200
    except Exception as e:
        return jsonify({"message":"request not accepted"}),400
    
@technicianViews.route('/rejectRequest/<id>', methods=['POST'])
@role_required('technician')
def rejectRequest(id):
    try:
        ServiceRequest.reject(id,"rejected by technician")
        return jsonify({"message":"request rejected"}),200
    except Exception as e:
        return jsonify({"message":"request not rejected"}),400
    
@technicianViews.route('/search',methods=['GET','POST'])
@role_required('technician')
def search():
    data = request.json
    query = data.get('query')
    searchBy = data.get('searchBy')
    id = data.get('id')
    # print(query, searchBy, id)
    if searchBy == 'Service Request':
        service_requests = ServiceRequest.search_tech(query, id)
        return jsonify({"service_requests":service_requests}),200
    return jsonify({"message":"search not found"})

@technicianViews.route('/summary/<id>',methods=['GET'])
@role_required('technician')
def summary(id):
    tech_summary = Technician.get_summary()
    tech_data =[]
    tech_labels = []
    requests = ServiceRequest.get_request_summary(id)
    
    if not tech_summary or not requests:
        return jsonify({"message":"no data found"})
    for tech in tech_summary:
        tech_labels.append(tech['name'])
        tech_data.append(tech['completed_count'])
    requests[0]['accepted_requests']+=requests[0]['completed_requests']
    return jsonify({"request_data":list(requests[0].values()),"request_labels":list(requests[0].keys()),"tech_labels":tech_labels,"tech_data":tech_data})

@technicianViews.route('/profile/<id>', methods=['GET'])
@role_required('technician')
def profile(id):
    services = Service.get_services()
    tech = Technician.get_technician(id)
    return jsonify({"services":services, "tech":tech}),200

@technicianViews.route('/update/<id>', methods=['POST'])
@role_required('technician')
def update(id):
    data = request.json.get('data')
    # print(data)
    try:
        Technician.update(id, data)
        return jsonify({"message":"user updated"}),200
    except Exception as e:
        print(e)
        return jsonify({"message":"user not updated"}),400