from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.services.department_services import (
    get_department_by_id, get_all_departments,
    create_department, update_department, delete_department, search_departments
)
from app.schemas.department_schemas import (
    department_model, department_create_model,
    department_update_model, paginated_departments
)
from .pagination import pagination_parser, search_pagination_parser
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

ns = Namespace('departments', description='Department operations')

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class DepartmentList(Resource):
    @ns.doc('list_departments')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_departments)
    @jwt_required()
    @error_handler(500, "ERROR IN DepartmentListResource.get")
    def get(self):
        """List all departments"""
        args = pagination_parser.parse_args()
        departments, count, more = get_all_departments(**args)
        return {'results': departments, 'count': count, 'more': more}

    @ns.doc('create_department')
    @ns.expect(department_create_model)
    @ns.marshal_with(department_model, code=201)
    @ns.response(201, "Department created successfully")
    @ns.response(403, 'Permission denied')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN DepartmentList.post")
    def post(self):
        """Create a new department (Admin only)"""
        success, result = create_department(**ns.payload)
        if success:
            return result, 201
        ns.abort(400, result)

@ns.route('/<int:id>')
@ns.param('id', 'The department identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(404, 'Department not found')
@ns.response(500, 'Internal Server Error')
class DepartmentResource(Resource):
    @ns.doc('get_department')
    @ns.marshal_with(department_model)
    @jwt_required()
    @error_handler(500, "ERROR IN DepartmentResource.get")
    def get(self, id):
        """Fetch a department given its identifier"""
        department = get_department_by_id(id)
        if not department:
            ns.abort(404, "Department not found")
        return department

    @ns.doc('update_department')
    @ns.expect(department_update_model)
    @ns.marshal_with(department_model)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN DepartmentResource.put")
    def put(self, id):
        """Update a department given its identifier (Admin only)"""
        success, result = update_department(id, **ns.payload)
        if not success:
            if result == "Department not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return result

    @ns.doc('delete_department')
    @ns.response(204, 'Department deleted')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN DepartmentResource.delete")
    def delete(self, id):
        """Delete a department given its identifier (Admin only)"""
        success, result = delete_department(id)
        if not success:
            if result == "Department not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return '', 204

@ns.route('/search')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class DepartmentSearch(Resource):
    @ns.doc('search_departments')
    @ns.expect(search_pagination_parser)
    @ns.marshal_list_with(paginated_departments)
    @jwt_required()
    @error_handler(500, "ERROR IN DepartmentSearch.post")
    def post(self):
        """Search for departments"""
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        departments, count, more = search_departments(query, **args)
        return {'results': departments, 'count': count, 'more': more}