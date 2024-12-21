from app import db
from app.models import Doctor, Department 
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def add_doctor_to_department(doctor_id, department_id):
    doctor = Doctor.query.get(doctor_id)
    department = Department.query.get(department_id)
    if not doctor or not department:
        return False, "Doctor or Department not found"
    
    if department not in doctor.departments:
        doctor.departments.append(department)
        return safe_commit()
    return True, "Affiliation already exists"

def remove_doctor_from_department(doctor_id, department_id):
    doctor = Doctor.query.get(doctor_id)
    department = Department.query.get(department_id)
    if not doctor or not department:
        return False, "Doctor or Department not found"
    
    if department in doctor.departments:
        doctor.departments.remove(department)
        return safe_commit()
    return True, "Affiliation does not exist"

def get_doctors_by_department(department_id, page=1, per_page=10, sort='id', reverse=False):
    department = Department.query.get(department_id)
    if not department:
        return [], 0, False

    if not hasattr(Doctor, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Doctor.query.join(Doctor.departments).filter(Department.id == department_id)
    order = desc(getattr(Doctor, sort)) if reverse else getattr(Doctor, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_departments_by_doctor(doctor_id, page=1, per_page=10, sort='id', reverse=False):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return [], 0, False

    if not hasattr(Department, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Department.query.join(Department.doctors).filter(Doctor.id == doctor_id)
    order = desc(getattr(Department, sort)) if reverse else getattr(Department, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_all_affiliations(page=1, per_page=10):
    query = db.session.query(Doctor, Department).join(Doctor.departments)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    affiliations = [(doctor, department) for doctor, department in pagination.items]
    return affiliations, pagination.total, pagination.pages > page