from flask_restx import fields
from app import api
from .pagination import create_pagination_model

patient_model = api.model('Patient', {
    'id': fields.Integer(readonly=True, description='The patient unique identifier'),
    'user_id': fields.Integer(required=True, description='The user ID associated with this patient'),
    'name': fields.String(required=True, description='The patient name'),
    'gender': fields.String(required=True, description='The patient gender'),
    'birthday': fields.Date(required=True, description='The patient birthday'),
    'phone_number': fields.String(required=True, description='The patient phone number'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

patient_create_model = api.model('PatientCreate', {
    'user_id': fields.Integer(description='The user ID associated with this patient'),
    'name': fields.String(required=True, description='The patient name'),
    'gender': fields.String(required=True, description='The patient gender'),
    'birthday': fields.Date(required=True, description='The patient birthday'),
    'phone_number': fields.String(required=True, description='The patient phone number')
})

patient_update_model = api.model('PatientUpdate', {
    'name': fields.String(description='The patient name'),
    'gender': fields.String(description='The patient gender'),
    'birthday': fields.Date(description='The patient birthday'),
    'phone_number': fields.String(description='The patient phone number')
})

paginated_patients = create_pagination_model('Patients', patient_model)