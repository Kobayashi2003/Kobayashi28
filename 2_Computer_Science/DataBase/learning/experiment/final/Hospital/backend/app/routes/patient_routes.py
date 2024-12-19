from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.patient_services import (
    get_patient_by_id, get_patients_by_user_id, get_all_patients,
    create_patient, update_patient, delete_patient, search_patients
)
from app.services.user_services import is_admin
from app.schemas.patient_schemas import (
    patient_model, patient_create_model, 
    patient_update_model, paginated_patients
)
from .pagination import pagination_parser, search_pagination_parser
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

ns = Namespace('patients', description='Patient operations')

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class PatientList(Resource):
    @ns.doc('list_patients')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_patients)
    @jwt_required()
    @error_handler(500, "ERROR IN PatientListResource.get")
    def get(self):
        """List all patients for the current user"""
        args = pagination_parser.parse_args()
        current_user_id = get_jwt_identity()
        patients, count, more = get_patients_by_user_id(current_user_id, **args)
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
        success, message = create_patient(current_user_id, **ns.payload)
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
    @jwt_required()
    @error_handler(500, "ERROR IN PatientResource.put")
    def put(self, id):
        """Update a patient given its identifier"""
        current_user_id = get_jwt_identity()
        success, message = update_patient(current_user_id, id, **ns.payload)
        if not success:
            if message == "Patient not found":
                ns.abort(404, message)
            else:
                ns.abort(400, message)
        return message

    @ns.doc('delete_patient')
    @ns.response(204, 'Patient deleted')
    @jwt_required()
    @error_handler(500, "ERROR IN PatientResource.delete")
    def delete(self, id):
        """Delete a patient given its identifier"""
        current_user_id = get_jwt_identity()
        success, message = delete_patient(current_user_id, id)
        if not success:
            if message == "Patient not found":
                ns.abort(404, message)
            else:
                ns.abort(400, message)
        return message, 204

@ns.route('/search')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class PatientSearch(Resource):
    @ns.doc('search_patients')
    @ns.expect(search_pagination_parser)
    @ns.marshal_list_with(paginated_patients)
    @jwt_required()
    @error_handler(500, "ERROR IN PatientSearch.post")
    def post(self):
        """Search for patients"""
        current_user_id = get_jwt_identity()
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        patients, count, more = search_patients(current_user_id, query, **args)
        return {'results': patients, 'count': count, 'more': more}

@ns.route('/all')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class AllPatients(Resource):
    @ns.doc('list_all_patients')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_patients)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN AllPatients.get")
    def get(self):
        """List all patients (admin only)"""
        args = pagination_parser.parse_args()
        patients, count, more = get_all_patients(**args)
        return {'results': patients, 'count': count, 'more': more}