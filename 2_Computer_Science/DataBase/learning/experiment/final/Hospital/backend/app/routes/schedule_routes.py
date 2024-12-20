from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.services.schedule_services import (
    get_schedule_by_id, get_all_schedules, create_schedule,
    update_schedule, delete_schedule, search_schedules,
    get_schedules_by_doctor, get_schedules_by_department
)
from app.schemas.schedule_schemas import (
    schedule_model, schedule_create_model, 
    schedule_update_model, paginated_schedules
)
from .pagination import pagination_parser, search_pagination_parser
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

from .doctor_routes import ns as doctor_ns
from .department_routes import ns as department_ns
ns = Namespace('schedules', description='Schedule operations')

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class ScheduleList(Resource):
    @ns.doc('list_schedules')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_schedules)
    @jwt_required()
    @error_handler(500, "ERROR IN ScheduleListResource.get")
    def get(self):
        """List all schedules"""
        args = pagination_parser.parse_args()
        schedules, count, more = get_all_schedules(**args)
        return {'results': schedules, 'count': count, 'more': more}

    @ns.doc('create_schedule')
    @ns.expect(schedule_create_model)
    @ns.marshal_with(schedule_model, code=201)
    @ns.response(201, "Schedule created successfully")
    @ns.response(403, 'Permission denied')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN ScheduleList.post")
    def post(self):
        """Create a new schedule (Admin only)"""
        success, result = create_schedule(**ns.payload)
        if success:
            return result, 201
        ns.abort(400, result)

@ns.route('/<int:id>')
@ns.param('id', 'The schedule identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(404, 'Schedule not found')
@ns.response(500, 'Internal Server Error')
class ScheduleResource(Resource):
    @ns.doc('get_schedule')
    @ns.marshal_with(schedule_model)
    @jwt_required()
    @error_handler(500, "ERROR IN ScheduleResource.get")
    def get(self, id):
        """Fetch a schedule given its identifier"""
        schedule = get_schedule_by_id(id)
        if not schedule:
            ns.abort(404, "Schedule not found")
        return schedule

    @ns.doc('update_schedule')
    @ns.expect(schedule_update_model)
    @ns.marshal_with(schedule_model)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN ScheduleResource.put")
    def put(self, id):
        """Update a schedule given its identifier (Admin only)"""
        success, result = update_schedule(id, **ns.payload)
        if not success:
            if result == "Schedule not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return result

    @ns.doc('delete_schedule')
    @ns.response(204, 'Schedule deleted')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN ScheduleResource.delete")
    def delete(self, id):
        """Delete a schedule given its identifier (Admin only)"""
        success, result = delete_schedule(id)
        if not success:
            if result == "Schedule not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return '', 204

@ns.route('/search')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class ScheduleSearch(Resource):
    @ns.doc('search_schedules')
    @ns.expect(search_pagination_parser)
    @ns.marshal_list_with(paginated_schedules)
    @jwt_required()
    @error_handler(500, "ERROR IN ScheduleSearch.post")
    def post(self):
        """Search for schedules"""
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        schedules, count, more = search_schedules(query, **args)
        return {'results': schedules, 'count': count, 'more': more}

@doctor_ns.route('/<int:doctor_id>/schedules')
@doctor_ns.param('doctor_id', 'The doctor identifier')
@doctor_ns.response(400, 'Bad Request')
@doctor_ns.response(500, 'Internal Server Error')
class DoctorSchedules(Resource):
    @doctor_ns.doc('get_doctor_schedules')
    @doctor_ns.expect(pagination_parser)
    @doctor_ns.marshal_list_with(paginated_schedules)
    @jwt_required()
    @error_handler(500, "ERROR IN DoctorSchedules.get")
    def get(self, doctor_id):
        """Get schedules for a specific doctor"""
        args = pagination_parser.parse_args()
        schedules, count, more = get_schedules_by_doctor(doctor_id, **args)
        return {'results': schedules, 'count': count, 'more': more}

@department_ns.route('/<int:department_id>/schedules')
@department_ns.param('department_id', 'The department identifier')
@department_ns.response(400, 'Bad Request')
@department_ns.response(500, 'Internal Server Error')
class DepartmentSchedules(Resource):
    @department_ns.doc('get_department_schedules')
    @department_ns.expect(pagination_parser)
    @department_ns.marshal_list_with(paginated_schedules)
    @jwt_required()
    @error_handler(500, "ERROR IN DepartmentSchedules.get")
    def get(self, department_id):
        """Get schedules for a specific department"""
        args = pagination_parser.parse_args()
        schedules, count, more = get_schedules_by_department(department_id, **args)
        return {'results': schedules, 'count': count, 'more': more}