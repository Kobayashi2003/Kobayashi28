from app import db
from app.models import Patient
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def get_patient_by_id(patiend_id):
    return Patient.query.get(patiend_id)

def get_patients_by_user_id(user_id, page=1, per_page=10, sort='created_at', reverse=False):
    if not hasattr(Patient, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Patient.query.filter_by(user_id=user_id)
    order = desc(getattr(Patient, sort)) if reverse else getattr(Patient, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_all_patients(page=1, per_page=10, sort='id', reverse=False):
    if not hasattr(Patient, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Patient.query
    order = desc(getattr(Patient, sort)) if reverse else getattr(Patient, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_patient(user_id, name, gender, birthday, phone_number):
    new_patient = Patient(user_id=user_id, name=name, gender=gender, birthday=birthday, phone_number=phone_number)
    db.session.add(new_patient)
    return safe_commit()

def update_patient(user_id, patient_id, name=None, gender=None, birthday=None, phone_number=None):
    patient = Patient.query.filter_by(id=patient_id, user_id=user_id).first()
    if not patient:
        return False, "Patient not found"

    if name:
        patient.name = name
    if gender:
        patient.gender = gender
    if birthday:
        patient.birthday = birthday
    if phone_number:
        patient.phone_number = phone_number

    return safe_commit()

def delete_patient(user_id, patient_id):
    patient = Patient.query.filter_by(id=patient_id, user_id=user_id).first()
    if not patient:
        return False, "Patient not found"

    db.session.delete(patient)
    db.session.flush()
    return safe_commit()

def search_patients(user_id, query, page=1, per_page=10, sort='created_at', reverse=False):
    if not hasattr(Patient, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    search = f"%{query}%"
    query = Patient.query.filter(
        Patient.user_id == user_id,
        (Patient.name.ilike(search)) | (Patient.phone_number.ilike(search))
    )
    order = desc(getattr(Patient, sort)) if reverse else getattr(Patient, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page