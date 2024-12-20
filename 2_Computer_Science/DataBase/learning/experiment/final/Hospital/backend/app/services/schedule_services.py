from app import db
from app.models import Schedule
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def get_schedule_by_id(schedule_id):
    return Schedule.query.get(schedule_id)

def get_all_schedules(page=1, per_page=10, sort='id', reverse=False):
    if not hasattr(Schedule, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Schedule.query
    order = desc(getattr(Schedule, sort)) if reverse else getattr(Schedule, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_schedule(doctor_id, department_id, date, start_time, end_time, max_appointments):

    conflicting_schedule = Schedule.query.filter(
        Schedule.doctor_id == doctor_id,
        Schedule.date == date,
        ((Schedule.start_time <= start_time) & (Schedule.end_time > start_time)) |
        ((Schedule.start_time < end_time) & (Schedule.end_time >= end_time)) |
        ((Schedule.start_time >= start_time) & (Schedule.end_time <= end_time))
    ).first()

    if conflicting_schedule:
        return False, "Schedule conflict: The doctor already has an appointment during this time"

    new_schedule = Schedule(
        doctor_id=doctor_id,
        department_id=department_id,
        date=date,
        start_time=start_time,
        end_time=end_time,
        max_appointments=max_appointments
    )
    db.session.add(new_schedule)
    success, message = safe_commit()
    if success:
        return True, new_schedule
    return False, message

def update_schedule(schedule_id, doctor_id=None, department_id=None, date=None, start_time=None, end_time=None, max_appointments=None):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return False, "Schedule not found"

    if doctor_id is not None:
        schedule.doctor_id = doctor_id
    if department_id is not None:
        schedule.department_id = department_id
    if date:
        schedule.date = date
    if start_time:
        schedule.start_time = start_time
    if end_time:
        schedule.end_time = end_time
    if max_appointments:
        schedule.max_appointments = max_appointments
    
    success, message = safe_commit()
    if success:
        return True, schedule
    return False, message

def delete_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return False, "Schedule not found"
    
    db.session.delete(schedule)
    db.session.flush()
    success, message = safe_commit()
    if success:
        return True, ''
    return False, message

def search_schedules(query, page=1, per_page=10, sort='date', reverse=False):
    if not hasattr(Schedule, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    search = f"%{query}%"
    query = Schedule.query.join(Schedule.doctor).join(Schedule.department).filter(
        (Schedule.date.ilike(search)) |
        (Schedule.doctor.has(name=search)) |
        (Schedule.department.has(name=search))
    )
    order = desc(getattr(Schedule, sort)) if reverse else getattr(Schedule, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_schedules_by_doctor(doctor_id, page=1, per_page=10, sort='date', reverse=False):
    if not hasattr(Schedule, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Schedule.query.filter_by(doctor_id=doctor_id)
    order = desc(getattr(Schedule, sort)) if reverse else getattr(Schedule, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def get_schedules_by_department(department_id, page=1, per_page=10, sort='date', reverse=False):
    if not hasattr(Schedule, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    query = Schedule.query.filter_by(department_id=department_id)
    order = desc(getattr(Schedule, sort)) if reverse else getattr(Schedule, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page