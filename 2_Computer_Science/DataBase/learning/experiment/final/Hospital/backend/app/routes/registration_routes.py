from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.registration_services import (
    get_registration_by_id, get_registrations_by_user_id, get_all_registrations,
    create_registration, update_registration, delete_registration,
    search_registrations, get_registrations_by_patient,
    get_registrations_by_schedule, get_registrations_by_status,
    cancel_registration, complete_registration
)
from app.services.user_services import is_admin
from app.schemas.registration_schemas import (
    registration_model, registration_create_model, 
    registration_update_model, paginated_registrations
)
from .pagination import pagination_parser, search_pagination_parser
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

from .patient_routes import ns as patient_ns
from .schedule_routes import ns as schedule_ns
ns = Namespace('registrations', description='Registration operations')

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class RegistrationList(Resource):
    @ns.doc('list_registrations')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationListResource.get")
    def get(self):
        """List all registrations for the current user"""
        args = pagination_parser.parse_args()
        current_user_id = get_jwt_identity()
        registrations, count, more = get_registrations_by_user_id(current_user_id, **args)
        return {'results': registrations, 'count': count, 'more': more}

    @ns.doc('create_registration')
    @ns.expect(registration_create_model)
    @ns.marshal_with(registration_model, code=201)
    @ns.response(201, "Registration created successfully")
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationList.post")
    def post(self):
        """Create a new registration"""
        current_user_id = get_jwt_identity()
        success, message = create_registration(current_user_id, **ns.payload)
        if success:
            return message, 201
        ns.abort(400, message)

@ns.route('/<int:id>')
@ns.param('id', 'The registration identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(404, 'Registration not found')
@ns.response(500, 'Internal Server Error')
class RegistrationResource(Resource):
    @ns.doc('get_registration')
    @ns.marshal_with(registration_model)
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationResource.get")
    def get(self, id):
        """Fetch a registration given its identifier"""
        current_user_id = get_jwt_identity()
        registration = get_registration_by_id(id)
        if not registration:
            ns.abort(404, "Registration not found")
        if registration.patient.user_id != current_user_id and not is_admin(current_user_id):
            ns.abort(403, "You don't have permission to view this registration") 
        return registration

    @ns.doc('update_registration')
    @ns.expect(registration_update_model)
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationResource.put")
    def put(self, id):
        """Update a registration given its identifier"""
        current_user_id = get_jwt_identity()
        success, message = update_registration(current_user_id, id, **ns.payload)
        if not success:
            if message == "Registration not found":
                ns.abort(404, message)
            else:
                ns.abort(400, message)
        return message

    @ns.doc('delete_registration')
    @ns.response(204, 'Registration deleted')
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationResource.delete")
    def delete(self, id):
        """Delete a registration given its identifier"""
        current_user_id = get_jwt_identity()
        success, message = delete_registration(current_user_id, id)
        if not success:
            if message == "Registration not found":
                ns.abort(404, message)
            else:
                ns.abort(400, message)
        return message, 204

@ns.route('/search')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class RegistrationSearch(Resource):
    @ns.doc('search_registrations')
    @ns.expect(search_pagination_parser)
    @ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationSearch.post")
    def post(self):
        """Search for registrations"""
        current_user_id = get_jwt_identity()
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        registrations, count, more = search_registrations(current_user_id, query, **args)
        return {'results': registrations, 'count': count, 'more': more}

@patient_ns.route('/<int:patient_id>/registrations')
@patient_ns.param('patient_id', 'The patient identifier')
@patient_ns.response(400, 'Bad Request')
@patient_ns.response(500, 'Internal Server Error')
class PatientRegistrations(Resource):
    @patient_ns.doc('get_patient_registrations')
    @patient_ns.expect(pagination_parser)
    @patient_ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @error_handler(500, "ERROR IN PatientRegistrations.get")
    def get(self, patient_id):
        """Get registrations for a specific patient"""
        current_user_id = get_jwt_identity()
        args = pagination_parser.parse_args()
        registrations, count, more = get_registrations_by_patient(current_user_id, patient_id, **args)
        return {'results': registrations, 'count': count, 'more': more}

@schedule_ns.route('/<int:schedule_id>/registrations')
@schedule_ns.param('schedule_id', 'The schedule identifier')
@schedule_ns.response(400, 'Bad Request')
@schedule_ns.response(500, 'Internal Server Error')
class ScheduleRegistrations(Resource):
    @schedule_ns.doc('get_schedule_registrations')
    @schedule_ns.expect(pagination_parser)
    @schedule_ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @error_handler(500, "ERROR IN ScheduleRegistrations.get")
    def get(self, schedule_id):
        """Get registrations for a specific schedule"""
        current_user_id = get_jwt_identity()
        args = pagination_parser.parse_args()
        registrations, count, more = get_registrations_by_schedule(current_user_id, schedule_id, **args)
        return {'results': registrations, 'count': count, 'more': more}

@ns.route('/status/<string:status>')
@ns.param('status', 'The registration status')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class StatusRegistrations(Resource):
    @ns.doc('get_status_registrations')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @error_handler(500, "ERROR IN StatusRegistrations.get")
    def get(self, status):
        """Get registrations by status"""
        current_user_id = get_jwt_identity()
        args = pagination_parser.parse_args()
        registrations, count, more = get_registrations_by_status(current_user_id, status, **args)
        return {'results': registrations, 'count': count, 'more': more}

@ns.route('/<int:id>/cancel')
@ns.param('id', 'The registration identifier')
@ns.response(400, 'Bad Request')
@ns.response(404, 'Registration not found')
@ns.response(500, 'Internal Server Error')
class CancelRegistration(Resource):
    @ns.doc('cancel_registration')
    @jwt_required()
    @error_handler(500, "ERROR IN CancelRegistration.put")
    def put(self, id):
        """Cancel a registration"""
        current_user_id = get_jwt_identity()
        success, message = cancel_registration(current_user_id, id)
        if not success:
            ns.abort(404, message)
        return message

@ns.route('/<int:id>/complete')
@ns.param('id', 'The registration identifier')
@ns.response(400, 'Bad Request')
@ns.response(404, 'Registration not found')
@ns.response(500, 'Internal Server Error')
class CompleteRegistration(Resource):
    @ns.doc('complete_registration')
    @jwt_required()
    @error_handler(500, "ERROR IN CompleteRegistration.put")
    def put(self, id):
        """Complete a registration"""
        current_user_id = get_jwt_identity()
        success, message = complete_registration(current_user_id, id)
        if not success:
            ns.abort(404, message)
        return message

@ns.route('/all')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class AllRegistrations(Resource):
    @ns.doc('list_all_registrations')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN AllRegistrations.get")
    def get(self):
        """List all registrations (admin only)"""
        args = pagination_parser.parse_args()
        registrations, count, more = get_all_registrations(**args)
        return {'results': registrations, 'count': count, 'more': more}