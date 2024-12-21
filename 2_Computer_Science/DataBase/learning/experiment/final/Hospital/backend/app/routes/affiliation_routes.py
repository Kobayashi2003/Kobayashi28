from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.services.affiliation_services import (
    add_doctor_to_department, remove_doctor_from_department, get_all_affiliations,
    get_departments_by_doctor, get_doctors_by_department 
)
from app.schemas.affiliation_schemas import affiliation_create_model, paginated_affiliations
from app.schemas.doctor_schemas import paginated_doctors
from app.schemas.department_schemas import paginated_departments
from .pagination import pagination_parser 
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

from .doctor_routes import ns as doctor_ns
from .department_routes import ns as department_ns
ns = Namespace('affiliations', description='Doctor-Department affiliation operations')

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class AffiliationList(Resource):
    @ns.doc('list_affiliations')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_affiliations)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN AffiliationListResource.get")
    def get(self):
        """List all doctor-department affiliations (Admin only)"""
        args = pagination_parser.parse_args()
        affiliations, count, more = get_all_affiliations(**args)
        return {'results': affiliations, 'count': count, 'more': more}

    @ns.doc('create_affiliation')
    @ns.expect(affiliation_create_model)
    @ns.response(201, 'Affiliation created successfully')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN AffiliationList.post")
    def post(self):
        """Create a new doctor-department affiliation (Admin only)"""
        success, message = add_doctor_to_department(**ns.payload)
        if success:
            return {'message': message}, 201
        ns.abort(400, message)

@ns.route('/<int:doctor_id>/<int:department_id>')
@ns.param('doctor_id', 'The doctor identifier')
@ns.param('department_id', 'The department identifier')
@ns.response(400, 'Bad Request')
@ns.response(404, 'Affiliation not found')
@ns.response(500, 'Internal Server Error')
class AffiliationResource(Resource):
    @ns.doc('delete_affiliation')
    @ns.response(204, 'Affiliation deleted')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN AffiliationResource.delete")
    def delete(self, doctor_id, department_id):
        """Remove a doctor-department affiliation (Admin only)"""
        success, message = remove_doctor_from_department(doctor_id, department_id)
        if not success:
            ns.abort(404, message)
        return '', 204

@doctor_ns.route('/<int:id>/departments')
@doctor_ns.param('id', 'The doctor identifier')
@doctor_ns.response(400, 'Bad Request')
@doctor_ns.response(404, 'Doctor not found')
@doctor_ns.response(500, 'Internal Server Error')
class DoctorDepartments(Resource):
    @doctor_ns.doc('get_doctor_departments')
    @doctor_ns.expect(pagination_parser)
    @doctor_ns.marshal_list_with(paginated_departments)
    @jwt_required()
    @error_handler(500, "ERROR IN DoctorDepartments.get")
    def get(self, id):
        """Get departments affiliated with a specific doctor"""
        args = pagination_parser.parse_args()
        departments, count, more = get_departments_by_doctor(id, **args)
        return {'results': departments, 'count': count, 'more': more}

@department_ns.route('/<int:id>/doctors')
@department_ns.param('id', 'The department identifier')
@department_ns.response(400, 'Bad Request')
@department_ns.response(404, 'Department not found')
@department_ns.response(500, 'Internal Server Error')
class DepartmentDoctors(Resource):
    @department_ns.doc('get_department_doctors')
    @department_ns.expect(pagination_parser)
    @department_ns.marshal_list_with(paginated_doctors)
    @jwt_required()
    @error_handler(500, "ERROR IN DepartmentDoctors.get")
    def get(self, id):
        """Get doctors affiliated with a specific department"""
        args = pagination_parser.parse_args()
        doctors, count, more = get_doctors_by_department(id, **args)
        return {'results': doctors, 'count': count, 'more': more}