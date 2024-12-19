from app import db
from app.models import Doctor
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def get_docctor_by_id(doctor_id):
    return Doctor.query.get(doctor_id)

def get_all_doctors(page=1, per_page=10, sort='id', reverse=False):
    if not hasattr(Doctor, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Doctor.query
    order = desc(getattr(Doctor, sort)) if reverse else getattr(Doctor, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_doctor(name, gender, email, phone_number, description=None):
    new_doctor = Doctor(name=name, gender=gender, email=email, phone_number=phone_number, description=description)
    db.session.add(new_doctor)
    return safe_commit()

def update_doctor(doctor_id, name=None, gender=None, email=None, phone_number=None, description=None):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return False, "Doctor not found"

    if name:
        doctor.name = name
    if gender:
        doctor.gender = gender
    if email:
        doctor.email = email
    if phone_number:
        doctor.phone_number = phone_number
    if description is not None:
        doctor.description = description
    
    return safe_commit()

def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return False, "Doctor not found"
    
    db.session.delete(doctor)
    db.session.flush()
    return safe_commit()

def search_doctors(query, page=1, per_page=10, sort='name', reverse=False):
    if not hasattr(Doctor, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    search = f"%{query}%"
    query = Doctor.query.filter(
        (Doctor.name.ilike(search)) | 
        (Doctor.email.ilike(search)) | 
        (Doctor.phone_number.ilike(search))
    )
    order = desc(getattr(Doctor, sort)) if reverse else getattr(Doctor, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page