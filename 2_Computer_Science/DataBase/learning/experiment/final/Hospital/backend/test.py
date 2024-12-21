import sys
import os
import random
from datetime import datetime, timedelta
from faker import Faker

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the create_app function
from app import create_app

# Create a Faker instance
fake = Faker()

# Create the Flask app
app = create_app()

# Get the db object from the app
db = app.extensions['sqlalchemy']

# Now import the models
from app.models import User, Patient, Doctor, Department, Schedule, Registration, affiliations

def create_users(num_users):
    users = []
    for _ in range(num_users):
        user = User(
            is_admin=fake.boolean(chance_of_getting_true=10),
            username=fake.user_name(),
            phone_number=fake.phone_number(),
            bio=fake.text(max_nb_chars=200)
        )
        user.set_password(fake.password())
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
    return users

def create_patients(users):
    patients = []
    for user in users:
        if not user.is_admin:
            patient = Patient(
                user_id=user.id,
                name=fake.name(),
                gender=random.choice(['male', 'female']),
                birthday=fake.date_of_birth(minimum_age=18, maximum_age=90),
                phone_number=fake.phone_number()
            )
            patients.append(patient)
    db.session.add_all(patients)
    db.session.commit()
    return patients

def create_doctors(num_doctors):
    doctors = []
    for _ in range(num_doctors):
        doctor = Doctor(
            name=fake.name(),
            gender=random.choice(['male', 'female']),
            email=fake.email(),
            phone_number=fake.phone_number(),
            description=fake.text(max_nb_chars=200)
        )
        doctors.append(doctor)
    db.session.add_all(doctors)
    db.session.commit()
    return doctors

def create_departments(num_departments):
    departments = []
    for _ in range(num_departments):
        department = Department(
            name=fake.unique.company(),
            description=fake.text(max_nb_chars=200)
        )
        departments.append(department)
    db.session.add_all(departments)
    db.session.commit()
    return departments

def create_affiliations(doctors, departments):
    for doctor in doctors:
        num_affiliations = random.randint(1, 3)
        affiliated_departments = random.sample(departments, num_affiliations)
        doctor.departments.extend(affiliated_departments)
    db.session.commit()

def create_schedules(doctors, departments):
    schedules = []
    for _ in range(100):  # Create 100 schedules
        doctor = random.choice(doctors)
        department = random.choice(doctor.departments)
        date = fake.date_between(start_date='today', end_date='+30d')
        start_time = fake.time_object()
        end_time = (datetime.combine(date, start_time) + timedelta(hours=random.randint(1, 4))).time()
        schedule = Schedule(
            doctor_id=doctor.id,
            department_id=department.id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            max_appointments=random.randint(5, 20)
        )
        schedules.append(schedule)
    db.session.add_all(schedules)
    db.session.commit()
    return schedules

def create_registrations(patients, schedules):
    registrations = []
    for schedule in schedules:
        num_registrations = random.randint(0, schedule.max_appointments)
        for _ in range(num_registrations):
            patient = random.choice(patients)
            registration = Registration(
                patient_id=patient.id,
                schedule_id=schedule.id,
                status=random.choice(['scheduled', 'completed', 'cancelled']),
                notes=fake.text(max_nb_chars=100) if random.choice([True, False]) else None
            )
            registrations.append(registration)
    db.session.add_all(registrations)
    db.session.commit()
    return registrations

def generate_test_data():
    print("Generating test data...")
    with app.app_context():
        users = create_users(50)
        patients = create_patients(users)
        doctors = create_doctors(20)
        departments = create_departments(10)
        create_affiliations(doctors, departments)
        schedules = create_schedules(doctors, departments)
        create_registrations(patients, schedules)
    print("Test data generation complete.")

if __name__ == "__main__":
    generate_test_data()