from flask_restx import fields
from app import api
from .pagination import create_pagination_model
from .doctor_schemas import doctor_model
from .department_schemas import department_model

affiliation_model = api.model('Affiliation', {
    'doctor': fields.Nested(doctor_model),
    'department': fields.Nested(department_model)
})

affiliation_create_model = api.model('AffiliationCreate', {
    'doctor_id': fields.Integer(required=True, description='The doctor ID'),
    'department_id': fields.Integer(required=True, description='The department ID')
})

paginated_affiliations = create_pagination_model('Affiliations', affiliation_model)