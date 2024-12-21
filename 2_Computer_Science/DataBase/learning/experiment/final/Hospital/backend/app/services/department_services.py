from app import db
from app.models import Department
from app.utils.db_utils import safe_commit
from sqlalchemy import desc

def get_department_by_id(department_id):
    return Department.query.get(department_id)

def get_all_departments(page=1, per_page=10, sort='id', reverse=False):
    if not hasattr(Department, sort):
        raise ValueError(f"Invalid sort field: {sort}")
    
    query = Department.query
    order = desc(getattr(Department, sort)) if reverse else getattr(Department, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page

def create_department(name, description=None, **kwargs):
    new_department = Department(name=name, description=description)
    db.session.add(new_department)
    success, message = safe_commit()
    if success:
        return True, new_department
    return False, message

def update_department(department_id, name=None, description=None, **kwargs):
    department = Department.query.get(department_id)
    if not department:
        return False, "Department not found"

    if name:
        department.name = name
    if description is not None:
        department.description = description
    
    success, message = safe_commit()
    if success:
        return True, department
    return False, message

def delete_department(department_id):
    department = Department.query.get(department_id)
    if not department:
        return False, "Department not found"
    
    db.session.delete(department)
    db.session.flush()
    success, message = safe_commit()
    if success:
        return True, ''
    return False, message

def search_departments(query, page=1, per_page=10, sort='name', reverse=False):
    if not hasattr(Department, sort):
        raise ValueError(f"Invalid sort field: {sort}")

    search = f"%{query}%"
    query = Department.query.filter(
        (Department.name.ilike(search)) | 
        (Department.description.ilike(search))
    )
    order = desc(getattr(Department, sort)) if reverse else getattr(Department, sort)
    query = query.order_by(order)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, pagination.pages > page