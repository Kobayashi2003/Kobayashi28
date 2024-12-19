from flask_restx import fields
from app import api
from .pagination import create_pagination_model

department_model = api.model('Department', {
    'id': fields.Integer(readonly=True, description='The department unique identifier'),
    'name': fields.String(required=True, description='The department name'),
    'description': fields.String(description='The department description'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

department_create_model = api.model('DepartmentCreate', {
    'name': fields.String(required=True, description='The department name'),
    'description': fields.String(description='The department description')
})

department_update_model = api.model('DepartmentUpdate', {
    'name': fields.String(description='The department name'),
    'description': fields.String(description='The department description')
})

paginated_departments = create_pagination_model('Departments', department_model)