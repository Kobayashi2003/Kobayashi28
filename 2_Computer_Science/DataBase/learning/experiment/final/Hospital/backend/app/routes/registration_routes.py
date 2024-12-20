from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.registration_services import (
    get_registration_by_id, get_all_registrations,
    create_registration, update_registration, delete_registration,
    cancel_registration, complete_registration, search_registrations,
    get_all_registrations_owned_by_user, search_registrations_owned_by_user,
    is_registration_owned_by_user, get_registrations_by_patient,
    get_registrations_by_schedule, get_registrations_by_status,
)
from app.services.user_services import is_admin
from app.services.patient_services import is_patient_owned_by_user 
from app.schemas.registration_schemas import (
    registration_model, registration_create_model, 
    registration_update_model, paginated_registrations
)
from .pagination import pagination_parser, search_pagination_parser
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

from .user_routes import ns as user_ns
from .patient_routes import ns as patient_ns
from .schedule_routes import ns as schedule_ns
ns = Namespace('registrations', description='Registration operations')

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class RegistrationList(Resource):
    @ns.doc('list_registrations')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN RegistrationListResource.get")
    def get(self):
        """List all registrations"""
        args = pagination_parser.parse_args()
        registrations, count, more = get_all_registrations(**args)
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
        payload = ns.payload
        if (not is_patient_owned_by_user(patient_id=payload['patient_id'], user_id=current_user_id)
            and not is_admin(current_user_id)
            ):
            ns.abort(403, "You don't have permission to create a registration for another user")
        success, result = create_registration(**payload)
        if success:
            return result, 201
        ns.abort(400, result)

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
    @ns.marshal_with(registration_model)
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationResource.put")
    def put(self, id):
        """Update a registration given its identifier"""
        current_user_id = get_jwt_identity()
        if (not is_registration_owned_by_user(registration_id=id, user_id=current_user_id) 
            and not is_admin(current_user_id)
            ):
            ns.abort(403, "You don't have permission to update this registration")
        success, result = update_registration(id, **ns.payload)
        if not success:
            if result == "Registration not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return result

    @ns.doc('delete_registration')
    @ns.response(204, 'Registration deleted')
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationResource.delete")
    def delete(self, id):
        """Delete a registration given its identifier"""
        current_user_id = get_jwt_identity()
        if (not is_registration_owned_by_user(registration_id=id, user_id=current_user_id) 
            and not is_admin(current_user_id)
            ):
            ns.abort(403, "You don't have permission to update this registration")
        success, result = delete_registration(id)
        if not success:
            if result == "Registration not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return '', 204

@ns.route('/<int:id>/cancel')
@ns.param('id', 'The registration identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(404, 'Registration not found')
@ns.response(500, 'Internal Server Error')
class CancelRegistration(Resource):
    @ns.doc('cancel_registration')
    @jwt_required()
    @error_handler(500, "ERROR IN CancelRegistration.put")
    def put(self, id):
        """Cancel a registration"""
        current_user_id = get_jwt_identity()
        if (not is_registration_owned_by_user(registration_id=id, user_id=current_user_id) 
            and not is_admin(current_user_id)
            ):
            ns.abort(403, "You don't have permission to update this registration")
        success, result = cancel_registration(id)
        if not success:
            ns.abort(404, result)
        return result

@ns.route('/<int:id>/complete')
@ns.param('id', 'The registration identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(404, 'Registration not found')
@ns.response(500, 'Internal Server Error')
class CompleteRegistration(Resource):
    @ns.doc('complete_registration')
    @jwt_required()
    @error_handler(500, "ERROR IN CompleteRegistration.put")
    def put(self, id):
        """Complete a registration"""
        current_user_id = get_jwt_identity()
        if (not is_registration_owned_by_user(registration_id=id, user_id=current_user_id) 
            and not is_admin(current_user_id)
            ):
            ns.abort(403, "You don't have permission to update this registration")
        success, result = complete_registration(id)
        if not success:
            ns.abort(404, result)
        return result

@ns.route('/search')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class RegistrationSearch(Resource):
    @ns.doc('search_registrations')
    @ns.expect(search_pagination_parser)
    @ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @error_handler(500, "ERROR IN RegistrationSearch.post")
    def post(self):
        """Search for registrations"""
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        registrations, count, more = search_registrations(query, **args)
        return {'results': registrations, 'count': count, 'more': more}

@patient_ns.route('/<int:patient_id>/registrations')
@patient_ns.param('patient_id', 'The patient identifier')
@patient_ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@patient_ns.response(500, 'Internal Server Error')
class PatientRegistrations(Resource):
    @patient_ns.doc('get_patient_registrations')
    @patient_ns.expect(pagination_parser)
    @patient_ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN PatientRegistrations.get")
    def get(self, patient_id):
        """Get registrations for a specific patient"""
        args = pagination_parser.parse_args()
        registrations, count, more = get_registrations_by_patient(patient_id, **args)
        return {'results': registrations, 'count': count, 'more': more}

@schedule_ns.route('/<int:schedule_id>/registrations')
@schedule_ns.param('schedule_id', 'The schedule identifier')
@schedule_ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@schedule_ns.response(500, 'Internal Server Error')
class ScheduleRegistrations(Resource):
    @schedule_ns.doc('get_schedule_registrations')
    @schedule_ns.expect(pagination_parser)
    @schedule_ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN ScheduleRegistrations.get")
    def get(self, schedule_id):
        """Get registrations for a specific schedule"""
        args = pagination_parser.parse_args()
        registrations, count, more = get_registrations_by_schedule(schedule_id, **args)
        return {'results': registrations, 'count': count, 'more': more}

@ns.route('/status/<string:status>')
@ns.param('status', 'The registration status')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class StatusRegistrations(Resource):
    @ns.doc('get_status_registrations')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN StatusRegistrations.get")
    def get(self, status):
        """Get registrations by status"""
        args = pagination_parser.parse_args()
        registrations, count, more = get_registrations_by_status(status, **args)
        return {'results': registrations, 'count': count, 'more': more}

@user_ns.route('/<int:id>/registrations')
@ns.param('id', 'The User identifier')
@user_ns.response(400, 'Bad Request')
@user_ns.response(403, 'Permission denied')
@user_ns.response(500, 'Internal Server Error')
class UserRegistrations(Resource):
    @user_ns.doc('list_user_registrations')
    @user_ns.expect(pagination_parser)
    @user_ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @error_handler(500, "ERROR IN UserRegistrations.get")
    def get(self, id):
        """List all registrations owned by a specific user"""
        current_user_id = get_jwt_identity()
        if current_user_id != id and not is_admin(current_user_id):
            user_ns.abort(403, "You don't have permission to view these registrations")
        
        args = pagination_parser.parse_args()
        registrations, count, more = get_all_registrations_owned_by_user(id, **args)
        return {'results': registrations, 'count': count, 'more': more}

@user_ns.route('/<int:id>/registrations/search')
@ns.param('id', 'The User identifier')
@user_ns.response(400, 'Bad Request')
@user_ns.response(403, 'Permission denied')
@user_ns.response(500, 'Internal Server Error')
class UserRegistrationsSearch(Resource):
    @user_ns.doc('search_user_registrations')
    @user_ns.expect(search_pagination_parser)
    @user_ns.marshal_list_with(paginated_registrations)
    @jwt_required()
    @error_handler(500, "ERROR IN UserRegistrationsSearch.post")
    def post(self, id):
        """Search registrations owned by a specific user"""
        current_user_id = get_jwt_identity()
        if current_user_id != id and not is_admin(current_user_id):
            user_ns.abort(403, "You don't have permission to search these registrations")
        
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        registrations, count, more = search_registrations_owned_by_user(id, query, **args)
        return {'results': registrations, 'count': count, 'more': more}