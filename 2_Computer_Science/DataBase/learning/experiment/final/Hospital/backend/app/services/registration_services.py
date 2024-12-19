from app import db
from app.models import Registration, Schedule, Patient
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def get_registration_by_id(registration_id):
    return Registration.query.get(registration_id)

def get_registrations_by_user_id(user_id, page=1, per_page=10, sort='created_at', reverse=False):
    if not hasattr(Registration, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Registration.query.join(Patient).filter(Patient.user_id == user_id)
    order = desc(getattr(Registration, sort)) if reverse else getattr(Registration, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_all_registrations(page=1, per_page=10, sort='created_at', reverse=False):
    if not hasattr(Registration, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Registration.query
    order = desc(getattr(Registration, sort)) if reverse else getattr(Registration, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_registration(user_id, patient_id, schedule_id, notes=None):
    # Check if the patient exists
    patient = Patient.query.filter_by(id=patient_id, user_id=user_id)
    if not patient:
        return False, "Patient not found"

    # Check if the schedule exists and has available slots
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return False, "Schedule not found"
    
    if schedule.available_slots <= 0:
        return False, "No available slots for this schedule"

    # Check for existing registration
    existing_registration = Registration.query.filter_by(
        patient_id=patient_id,
        schedule_id=schedule_id,
        status='scheduled'
    ).first()
    
    if existing_registration:
        return False, "Patient already has a scheduled registration for this time slot"

    new_registration = Registration(
        patient_id=patient_id,
        schedule_id=schedule_id,
        notes=notes
    )
    db.session.add(new_registration)
    return safe_commit()

def update_registration(user_id, registration_id, status=None, notes=None):
    registration = Registration.query.join(Patient).filter(
        Registration.id == registration_id,
        Patient.user_id == user_id
    )
    if not registration:
        return False, "Registration not found"

    if status:
        registration.status = status
    if notes is not None:
        registration.notes = notes

    return safe_commit()

def cancel_registration(user_id, registration_id):
    return update_registration(user_id, registration_id, status='cancelled')

def complete_registration(user_id, registration_id):
    return update_registration(user_id, registration_id, status='completed')

def delete_registration(user_id, registration_id):
    registration = Registration.query.join(Patient).filter(
        Registration.id == registration_id,
        Patient.user_id == user_id
    )
    if not registration:
        return False, "Registration not found"
    
    db.session.delete(registration)
    return safe_commit()

def search_registrations(user_id, query, page=1, per_page=10, sort='created_at', reverse=False):
    if not hasattr(Registration, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    search = f"%{query}%"
    query = Registration.query.join(Registration.patient).join(Registration.schedule).filter(
        Patient.user_id == user_id,
        (Patient.name.ilike(search)) |
        (Registration.status.ilike(search)) |
        (Registration.notes.ilike(search))
    )
    order = desc(getattr(Registration, sort)) if reverse else getattr(Registration, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_registrations_by_patient(user_id, patient_id, page=1, per_page=10, sort='created_at', reverse=False):
    if not hasattr(Registration, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Registration.query.join(Patient).filter(
        Registration.patient_id == patient_id,
        Patient.user_id == user_id
    )
    order = desc(getattr(Registration, sort)) if reverse else getattr(Registration, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_registrations_by_schedule(user_id, schedule_id, page=1, per_page=10, sort='created_at', reverse=False):
    if not hasattr(Registration, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Registration.query.join(Patient).filter(
        Registration.schedule_id == schedule_id,
        Patient.user_id == user_id
    )
    order = desc(getattr(Registration, sort)) if reverse else getattr(Registration, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_registrations_by_status(user_id, status, page=1, per_page=10, sort='created_at', reverse=False):
    if status not in ['scheduled', 'completed', 'cancelled']:
        return False, "Invalid status"

    if not hasattr(Registration, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Registration.query.join(Patient).filter(
        Registration.status == status,
        Patient.user_id == user_id
    )
    order = desc(getattr(Registration, sort)) if reverse else getattr(Registration, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page