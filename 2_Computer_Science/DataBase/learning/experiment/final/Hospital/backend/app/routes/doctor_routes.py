from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required 
from app.services.doctor_services import (
    get_docctor_by_id, get_all_doctors,
    create_doctor, update_doctor, delete_doctor, search_doctors
)
from app.schemas.doctor_schemas import (
    doctor_model, doctor_create_model, 
    doctor_update_model, paginated_doctors
)
from .pagination import pagination_parser, search_pagination_parser
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

ns = Namespace('doctors', description='Doctor operations')

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class DoctorList(Resource):
    @ns.doc('list_doctors')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_doctors)
    @jwt_required()
    @error_handler(500, "ERROR IN DoctorListResource.get")
    def get(self):
        """List all doctors"""
        args = pagination_parser.parse_args()
        doctors, count, more = get_all_doctors(**args)
        return {'results': doctors, 'count': count, 'more': more}

    @ns.doc('create_doctor')
    @ns.expect(doctor_create_model)
    @ns.marshal_with(doctor_model, code=201)
    @ns.response(201, "Doctor created successfully")
    @ns.response(403, 'Permission denied')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN DoctorList.post")
    def post(self):
        """Create a new doctor (Admin only)"""
        success, message = create_doctor(**ns.payload)
        if success:
            return message, 201
        ns.abort(400, message)

@ns.route('/<int:id>')
@ns.param('id', 'The doctor identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(404, 'Doctor not found')
@ns.response(500, 'Internal Server Error')
class DoctorResource(Resource):
    @ns.doc('get_doctor')
    @ns.marshal_with(doctor_model)
    @jwt_required()
    @error_handler(500, "ERROR IN DoctorResource.get")
    def get(self, id):
        """Fetch a doctor given its identifier"""
        doctor = get_docctor_by_id(id)
        if not doctor:
            ns.abort(404, "Doctor not found")
        return doctor

    @ns.doc('update_doctor')
    @ns.expect(doctor_update_model)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN DoctorResource.put")
    def put(self, id):
        """Update a doctor given its identifier (Admin only)"""
        success, message = update_doctor(id, **ns.payload)
        if not success:
            if message == "Doctor not found":
                ns.abort(404, message)
            else:
                ns.abort(400, message)
        return message

    @ns.doc('delete_doctor')
    @ns.response(204, 'Doctor deleted')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN DoctorResource.delete")
    def delete(self, id):
        """Delete a doctor given its identifier (Admin only)"""
        success, message = delete_doctor(id)
        if not success:
            if message == "Doctor not found":
                ns.abort(404, message)
            else:
                ns.abort(400, message)
        return message, 204

@ns.route('/search')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class DoctorSearch(Resource):
    @ns.doc('search_doctors')
    @ns.expect(search_pagination_parser)
    @ns.marshal_list_with(paginated_doctors)
    @jwt_required()
    @error_handler(500, "ERROR IN DoctorSearch.post")
    def post(self):
        """Search for doctors"""
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        doctors, count, more = search_doctors(query, **args)
        return {'results': doctors, 'count': count, 'more': more}