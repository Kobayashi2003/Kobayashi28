from flask_restx import fields
from app import api
from .pagination import create_pagination_model

schedule_model = api.model('Schedule', {
    'id': fields.Integer(readonly=True, description='The schedule unique identifier'),
    'doctor_id': fields.Integer(required=True, description='The doctor ID'),
    'department_id': fields.Integer(required=True, description='The department ID'),
    'date': fields.Date(required=True, description='The schedule date'),
    'start_time': fields.String(required=True, description='The start time of the schedule'),
    'end_time': fields.String(required=True, description='The end time of the schedule'),
    'max_appointments': fields.Integer(required=True, description='Maximum number of appointments'),
    'available_slots': fields.Integer(readonly=True, description='Number of available appointment slots'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

schedule_create_model = api.model('ScheduleCreate', {
    'doctor_id': fields.Integer(required=True, description='The doctor ID'),
    'department_id': fields.Integer(required=True, description='The department ID'),
    'date': fields.Date(required=True, description='The schedule date'),
    'start_time': fields.String(required=True, description='The start time of the schedule'),
    'end_time': fields.String(required=True, description='The end time of the schedule'),
    'max_appointments': fields.Integer(required=True, description='Maximum number of appointments')
})

schedule_update_model = api.model('ScheduleUpdate', {
    'doctor_id': fields.Integer(description='The doctor ID'),
    'department_id': fields.Integer(description='The department ID'),
    'date': fields.Date(description='The schedule date'),
    'start_time': fields.String(description='The start time of the schedule'),
    'end_time': fields.String(description='The end time of the schedule'),
    'max_appointments': fields.Integer(description='Maximum number of appointments')
})

paginated_schedules = create_pagination_model('Schedules', schedule_model)