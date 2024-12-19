from flask_restx import fields
from app import api
from .pagination import create_pagination_model

registration_model = api.model('Registration', {
    'id': fields.Integer(readonly=True, description='The registration unique identifier'),
    'patient_id': fields.Integer(required=True, description='The patient ID'),
    'schedule_id': fields.Integer(required=True, description='The schedule ID'),
    'status': fields.String(required=True, description='The registration status', enum=['scheduled', 'completed', 'cancelled']),
    'notes': fields.String(description='Additional notes for the registration'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

registration_create_model = api.model('RegistrationCreate', {
    'patient_id': fields.Integer(required=True, description='The patient ID'),
    'schedule_id': fields.Integer(required=True, description='The schedule ID'),
    'notes': fields.String(description='Additional notes for the registration')
})

registration_update_model = api.model('RegistrationUpdate', {
    'status': fields.String(description='The registration status', enum=['scheduled', 'completed', 'cancelled']),
    'notes': fields.String(description='Additional notes for the registration')
})

paginated_registrations = create_pagination_model('Registrations', registration_model)