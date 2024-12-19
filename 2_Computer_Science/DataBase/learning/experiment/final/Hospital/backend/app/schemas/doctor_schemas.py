from flask_restx import fields
from app import api
from .pagination import create_pagination_model

doctor_model = api.model('Doctor', {
    'id': fields.Integer(readonly=True, description='The doctor unique identifier'),
    'name': fields.String(required=True, description='The doctor name'),
    'gender': fields.String(required=True, description='The doctor gender'),
    'email': fields.String(required=True, description='The doctor email'),
    'phone_number': fields.String(required=True, description='The doctor phone number'),
    'description': fields.String(description='The doctor description'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

doctor_create_model = api.model('DoctorCreate', {
    'name': fields.String(required=True, description='The doctor name'),
    'gender': fields.String(required=True, description='The doctor gender'),
    'email': fields.String(required=True, description='The doctor email'),
    'phone_number': fields.String(required=True, description='The doctor phone number'),
    'description': fields.String(description='The doctor description')
})

doctor_update_model = api.model('DoctorUpdate', {
    'name': fields.String(description='The doctor name'),
    'gender': fields.String(description='The doctor gender'),
    'email': fields.String(description='The doctor email'),
    'phone_number': fields.String(description='The doctor phone number'),
    'description': fields.String(description='The doctor description')
})

paginated_doctors = create_pagination_model('Doctors', doctor_model)