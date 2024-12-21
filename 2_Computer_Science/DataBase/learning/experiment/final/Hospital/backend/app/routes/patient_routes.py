from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity as _get_jwt_identity
from app.services.patient_services import (
    get_patient_by_id, get_all_patients, create_patient, 
    update_patient, delete_patient, search_patients,
    get_all_patients_owned_by_user, search_patients_owned_by_user, 
    is_patient_owned_by_user
)
from app.services.user_services import is_admin
from app.schemas.patient_schemas import (
    patient_model, patient_create_model, 
    patient_update_model, paginated_patients
)
from .pagination import pagination_parser, search_pagination_parser
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

from .user_routes import ns as user_ns
ns = Namespace('patients', description='Patient operations')

get_jwt_identity = lambda : int(_get_jwt_identity())

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class PatientList(Resource):
    @ns.doc('list_patients')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_patients)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN PatientListResource.get")
    def get(self):
        """List all patients"""
        args = pagination_parser.parse_args()
        patients, count, more = get_all_patients(**args)
        return {'results': patients, 'count': count, 'more': more}

    @ns.doc('create_patient')
    @ns.expect(patient_create_model)
    @ns.marshal_with(patient_model, code=201)
    @ns.response(201, "Patient created successfully")
    @jwt_required()
    @error_handler(500, "ERROR IN PatientList.post")
    def post(self):
        """Create a new patient"""
        current_user_id = get_jwt_identity()
        payload = ns.payload
        if 'user_id' in payload and payload['user_id'] != current_user_id and not is_admin(current_user_id):
            ns.abort(403, "You don't have permission to create a patient for another user")
        payload['user_id'] = current_user_id if 'user_id' not in payload else payload['user_id']
        success, message = create_patient(**payload)
        if success:
            return message, 201
        ns.abort(400, message)

@ns.route('/<int:id>')
@ns.param('id', 'The patient identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(404, 'Patient not found')
@ns.response(500, 'Internal Server Error')
class PatientResource(Resource):
    @ns.doc('get_patient')
    @ns.marshal_with(patient_model)
    @jwt_required()
    @error_handler(500, "ERROR IN PatientResource.get")
    def get(self, id):
        """Fetch a patient given its identifier"""
        current_user_id = get_jwt_identity()
        patient = get_patient_by_id(id)
        if not patient:
            ns.abort(404, "Patient not found")
        if patient.user_id != current_user_id and not is_admin(current_user_id):
            ns.abort(403, "You don't have permission to view this patient")
        return patient

    @ns.doc('update_patient')
    @ns.expect(patient_update_model)
    @ns.marshal_with(patient_model)
    @jwt_required()
    @error_handler(500, "ERROR IN PatientResource.put")
    def put(self, id):
        """Update a patient given its identifier"""
        current_user_id = get_jwt_identity()
        if (not is_patient_owned_by_user(patient_id=id, user_id=current_user_id)
            and not is_admin(current_user_id)
            ):
            ns.abort(403, "You don't have permission to update this patient")
        success, result = update_patient(id, **ns.payload)
        if not success:
            if result == "Patient not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return result

    @ns.doc('delete_patient')
    @ns.response(204, 'Patient deleted')
    @jwt_required()
    @error_handler(500, "ERROR IN PatientResource.delete")
    def delete(self, id):
        """Delete a patient given its identifier"""
        current_user_id = get_jwt_identity()
        if (not is_patient_owned_by_user(patient_id=id, user_id=current_user_id)
            and not is_admin(current_user_id)
            ):
            ns.abort(403, "You don't have permission to update this patient")
        success, result = delete_patient(id)
        if not success:
            if result == "Patient not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return '', 204

@ns.route('/search')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class PatientSearch(Resource):
    @ns.doc('search_patients')
    @ns.expect(search_pagination_parser)
    @ns.marshal_list_with(paginated_patients)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN PatientSearch.post")
    def post(self):
        """Search for patients"""
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        patients, count, more = search_patients(query, **args)
        return {'results': patients, 'count': count, 'more': more}

@user_ns.route('/<int:id>/patients')
@ns.param('id', 'The User identifier')
@user_ns.response(400, 'Bad Request')
@user_ns.response(403, 'Permission denied')
@user_ns.response(500, 'Internal Server Error')
class UserPatients(Resource):
    @user_ns.doc('list_user_patients')
    @user_ns.expect(pagination_parser)
    @user_ns.marshal_list_with(paginated_patients)
    @jwt_required()
    @error_handler(500, "ERROR IN UserPatients.get")
    def get(self, id):
        """List all patients owned by a specific user"""
        current_user_id = get_jwt_identity()
        if current_user_id != id and not is_admin(current_user_id):
            user_ns.abort(403, "You don't have permission to view these patients")
        
        args = pagination_parser.parse_args()
        patients, count, more = get_all_patients_owned_by_user(id, **args)
        return {'results': patients, 'count': count, 'more': more}

@user_ns.route('/<int:id>/patients/search')
@ns.param('id', 'The User identifier')
@user_ns.response(400, 'Bad Request')
@user_ns.response(403, 'Permission denied')
@user_ns.response(500, 'Internal Server Error')
class UserPatientsSearch(Resource):
    @user_ns.doc('search_user_patients')
    @user_ns.expect(search_pagination_parser)
    @user_ns.marshal_list_with(paginated_patients)
    @jwt_required()
    @error_handler(500, "ERROR IN UserPatientsSearch.post")
    def post(self, id):
        """Search patients owned by a specific user"""
        current_user_id = get_jwt_identity()
        if current_user_id != id and not is_admin(current_user_id):
            user_ns.abort(403, "You don't have permission to search these patients")
        
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        patients, count, more = search_patients_owned_by_user(id, query, **args)
        return {'results': patients, 'count': count, 'more': more}