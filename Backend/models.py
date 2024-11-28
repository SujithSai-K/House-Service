from . import db, mail
from flask_login import UserMixin
from marshmallow import Schema, fields, validate
from datetime import datetime, date
from sqlalchemy import text
import sqlite3
from flask_mail import Message




try:
    conn = sqlite3.connect('instance/HouseServices.db',check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
except Exception as e:
    print(e)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

        
    def register(self):
        db.session.add(self)
        db.session.commit()
        
    def has_role(self, role):
        if self.role == role:
            return True
        return False




class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)

    def __init__(self, name, description, price, time_required):
        self.name = name
        self.description = description
        self.price = price
        self.time_required = time_required

    def register(self):
        db.session.add(self)
        db.session.commit()

    def get_services():
        cursor.execute('SELECT * FROM service')
        rows = cursor.fetchall()
        services = [dict(row) for row in rows]
        return services
    
    def get_service(id):
        cursor.execute('SELECT * FROM service WHERE id = ?', (id, ))
        row = cursor.fetchone()
        service = dict(row)
        return service
    
    def update(id, name, description, price, time_required):
        service = Service.query.get(id)
        service.name = name
        service.description = description
        service.price = price
        service.time_required = time_required
        db.session.commit()
    
    def delete(id):
        service = Service.query.get(id)
        db.session.delete(service)
        db.session.commit()
    
    def search(query):
        cursor.execute('SELECT * FROM service WHERE cast(id as text) LIKE ?', ('%'+query+'%',))
        rows = cursor.fetchall()
        services = [dict(row) for row in rows]
        return services




class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __init__(self, user_id, email, name, gender, age, service_id, experience, address):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.email = email
        self.age = age
        self.registration_date = datetime.now().date()
        self.service_id = service_id
        self.experience = experience
        self.address = address
        self.status = "Available"

    def register(self):
        db.session.add(self)
        db.session.commit()

    def get_technicians():
        try:
            cursor.execute('SELECT * FROM technician')
            rows = cursor.fetchall()
            technicians = [dict(row) for row in rows]
            return technicians
        except Exception as e:
            print(e)
        
    
    def get_technician(id):
        cursor.execute('SELECT t.*, s.name as service_name, u.username AS username, u.password AS password FROM technician t JOIN service s ON t.service_id = s.id JOIN user u ON t.user_id = u.id WHERE t.user_id = ?', (id, ))
        row = cursor.fetchone()
        technician = dict(row)
        return technician
    

    def get_technician_for_user(user_id, service_id):
        cursor.execute("""
                    SELECT t.*
                    FROM Technician t
                    WHERE t.id NOT IN (
                        SELECT sr.technician_id
                        FROM service_request sr
                        WHERE sr.customer_id = ? 
                        AND sr.status IN ('Requested', 'Assigned'))
                    AND t.service_id = ?
                    AND t.status = 'Available';
                    """,(user_id, service_id))
        rows = cursor.fetchall()
        technician = [dict(row) for row in rows]
        return technician


    def get_technician_by_service(id):
        cursor.execute('SELECT * FROM technician WHERE service_id = ?', (id,))
        rows = cursor.fetchall()
        technician = [dict(row) for row in rows]
        return technician
    
    def suspend(id):
        technician = Technician.query.get(id)
        technician.status = "Suspended"
        db.session.commit()

    def activate(id):
        technician = Technician.query.get(id)
        technician.status = "Available"
        db.session.commit()

    def search(id):
        cursor.execute('SELECT * FROM technician WHERE cast(id as text) like ?', ('%'+id+'%',))
        rows = cursor.fetchall()
        technician = [dict(row) for row in rows]
        return technician
    
    def search_cust(id, cust_id):
        cursor.execute("""SELECT t.*, s.name AS service_name
                FROM technician t
                JOIN service s ON t.service_id = s.id
                WHERE CAST(t.id AS TEXT) LIKE ?
                AND NOT EXISTS (
                    SELECT 1
                    FROM service_request sr
                    WHERE sr.technician_id = t.id
                    AND sr.customer_id = ?
                    AND sr.status IN ('Pending', 'Requested')
                )""", ('%'+id+'%',cust_id, ))
        rows = cursor.fetchall()
        technician = [dict(row) for row in rows]
        return technician 
    
    def get_summary():
        cursor.execute("""SELECT t.name, COUNT(sr.id) AS completed_count
                       FROM service_request sr JOIN technician t ON t.id = sr.technician_id
                       WHERE sr.status = 'Completed'
                       GROUP BY t.name
                       ORDER BY completed_count DESC
                       LIMIT 10""")
        rows = cursor.fetchall()
        technicianSummary = [dict(row) for row in rows]
        return technicianSummary
    
    def update(id,data):
        technician = Technician.query.filter_by(user_id=id).first()
        user = User.query.get(id)
        technician.name = data['name']
        technician.email = data['email']
        technician.gender = data['gender']
        technician.age = data['age']
        technician.service_id = data['service_id']
        technician.experience = data['experience']
        technician.address = data['address']
        user.username = data['username']
        user.password = data['password']
        db.session.commit()




class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, name, email, gender, dob, phone, address):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.gender = gender
        self.dob = dob
        self.phone = phone
        self.address = address

    def register(self):
        db.session.add(self)
        db.session.commit()

    def search(id):
        cursor.execute('SELECT * FROM customer WHERE cast(id as text) like ?', ('%'+id+'%', ))
        rows = cursor.fetchall()
        customer = [dict(row) for row in rows]
        return customer
    
    def get_customers():
        cursor.execute('SELECT * FROM customer')
        rows = cursor.fetchall()
        customers = [dict(row) for row in rows]
        return customers
    
    def get_customer(id):
        cursor.execute('SELECT c.*, u.username, u.password FROM customer c JOIN user u ON c.user_id = u.id WHERE u.id=?', (id,))
        row = cursor.fetchone()
        customer = dict(row)
        return customer
    
    def update(id, data):
        customer = Customer.query.filter_by(user_id=id).first()
        user = User.query.get(id)
        customer.name = data['name']
        customer.gender = data['gender']
        customer.email = data['email']
        customer.dob = date.fromisoformat(data['dob'])
        customer.phone = data['phone']
        customer.address = data['address']
        user.username = data['username']
        user.password = data['password']
        db.session.commit()




class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=True)
    request_date = db.Column(db.Date, nullable=False)
    completion_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.Text, nullable=True)

    def __init__(self, customer_id, service_id, technician_id):
        self.customer_id = customer_id
        self.service_id = service_id
        self.technician_id = technician_id
        self.request_date = datetime.now().date()
        self.completion_date = None
        self.status = "Requested"
        self.remarks = None

    def register(self):
        db.session.add(self)
        db.session.commit()

    def get_service_requests():
        cursor.execute('SELECT sr.*, s.name AS service_name FROM service_request sr JOIN service s ON sr.service_id = s.id')
        rows = cursor.fetchall()
        service_requests = [dict(row) for row in rows]
        return service_requests
    
    def get_service_request_byCustomer(id):
        cursor.execute('SELECT * FROM service_request WHERE customer_id = ?', (id,))
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request
    
    def get_service_request_byTechnician(id):
        cursor.execute("""SELECT c.name, c.address, c.phone, sr.id,sr.status,sr.remarks
                       FROM service_request sr
                       JOIN customer c ON sr.customer_id = c.user_id
                       WHERE sr.technician_id = ?;""",(id,))
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request
    
    def accept(id):
        service_request = ServiceRequest.query.get(id)
        service_request.status = "Assigned"
        customer = Customer.query.filter_by(user_id=service_request.customer_id).first()
        msg = Message(
        subject="Service Request Accepted",
        recipients=[customer.email],
        body=f"Your service request of id:{service_request.id} has been accepted by technician."
        )
        mail.send(msg)
        db.session.commit()

    def reject(id, remarks):
        service_request = ServiceRequest.query.get(id)
        service_request.status = "Rejected"
        service_request.remarks = remarks
        customer = Customer.query.filter_by(user_id=service_request.customer_id).first()
        msg = Message(
        subject="Service Request Cancled",
        recipients=[customer.email],
        body=f"Your service request of id:{service_request.id} has been canceled({remarks})"
        )
        mail.send(msg)
        db.session.commit()

    def complete(id,remarks):
        service_request = ServiceRequest.query.get(id)
        service_request.status = "Completed"
        service_request.remarks = remarks
        service_request.completion_date = datetime.now().date()
        db.session.commit()

    def search(id):
        cursor.execute('SELECT * FROM service_request WHERE cast(id as text) LIKE ?', ('%'+id+'%', ))
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request
    
    def search_cust(id,cust_id):
        cursor.execute('SELECT * FROM service_request WHERE cast(id as text) LIKE ? AND customer_id = ?', ('%'+id+'%', cust_id,))
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request
    
    def search_tech(id,tech_id):
        cursor.execute('SELECT sr.* FROM service_request sr JOIN technician t ON sr.technician_id = t.id WHERE cast(sr.id as text) LIKE ? AND t.user_id = ?', ('%'+id+'%', tech_id,))
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request
    
    def get_service_summary():
        cursor.execute("""SELECT s.name, COUNT(sr.id) AS booking_count
                       FROM service_request sr
                       JOIN service s ON sr.service_id = s.id
                       WHERE request_date >= DATE('now','-1 month') AND status = 'Completed'
                       GROUP BY service_id
                       ORDER BY booking_count DESC""")
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request
    
    def get_request_summarys():
        cursor.execute("""SELECT COUNT(sr.id) AS total_requests,
                       SUM(CASE WHEN sr.status = 'Assigned' THEN 1 ELSE 0 END) AS accepted_requests,
                       SUM(CASE WHEN sr.status = 'Completed' THEN 1 ELSE 0 END) AS completed_requests
                       FROM service_request sr""")
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request
    
    def get_request_summary(id):
        cursor.execute("""SELECT COUNT(sr.id) AS total_requests,
                       SUM(CASE WHEN sr.status = 'Assigned' THEN 1 ELSE 0 END) AS accepted_requests,
                       SUM(CASE WHEN sr.status = 'Completed' THEN 1 ELSE 0 END) AS completed_requests
                       FROM service_request sr, technician t
                       WHERE sr.technician_id = t.id AND t.user_id = ?""",(id,))
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request
    
    def get_request_summary_cust(id):
        cursor.execute("""SELECT COUNT(sr.id) AS total_requests,
                       SUM(CASE WHEN sr.status = 'Assigned' THEN 1 ELSE 0 END) AS accepted_requests,
                       SUM(CASE WHEN sr.status = 'Completed' THEN 1 ELSE 0 END) AS completed_requests
                       FROM service_request sr
                       WHERE sr.customer_id = ?""",(id,))
        rows = cursor.fetchall()
        service_request = [dict(row) for row in rows]
        return service_request