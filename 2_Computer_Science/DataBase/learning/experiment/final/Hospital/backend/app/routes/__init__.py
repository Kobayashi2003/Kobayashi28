from .user_routes import ns as user_ns
from .patient_routes import ns as patient_ns
from .doctor_routes import ns as doctor_ns
from .department_routes import ns as department_ns
from .affiliation_routes import ns as affiliation_ns
from .schedule_routes import ns as schedule_ns
from .registration_routes import ns as registration_ns

def register_namespaces(api):
    api.add_namespace(user_ns) 
    api.add_namespace(patient_ns) 
    api.add_namespace(doctor_ns) 
    api.add_namespace(department_ns) 
    api.add_namespace(affiliation_ns)
    api.add_namespace(schedule_ns)
    api.add_namespace(registration_ns)
