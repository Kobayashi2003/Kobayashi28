from app import db
from sqlalchemy import Integer, String, Boolean, Text, Enum, Time, Date, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

affiliations = db.Table('affiliations',
    Column('doctor_id', Integer, ForeignKey('doctors.id', ondelete='CASCADE'), primary_key=True),
    Column('department_id', Integer, ForeignKey('departments.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, default=datetime.now(timezone.utc))
)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    patients = relationship('Patient', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    __tablename__ = 'patients'  
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    gender = Column(Enum('male', 'female', name='gender_type'), nullable=False)
    birthday = Column(Date, nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    registrations = relationship('Registration', backref='patient', lazy='dynamic', cascade='all, delete-orphan')

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    gender = Column(Enum('male', 'female', name='gender_type'), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    departments = relationship('Department', secondary=affiliations, back_populates='doctors')
    schedules = relationship('Schedule', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')

class Department(db.Model):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    doctors = relationship('Doctor', secondary=affiliations, back_populates='departments')
    schedules = relationship('Schedule', backref='department', lazy='dynamic', cascade='all, delete-orphan')

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete='CASCADE'))
    department_id = Column(Integer, ForeignKey('departments.id', ondelete='CASCADE'))
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    max_appointments = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    registrations = relationship('Registration', backref='schedule', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def available_slots(self):
        taken_slots = self.registrations.count()
        return max(0, self.max_appointments - taken_slots)

class Registration(db.Model):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum('scheduled', 'completed', 'cancelled', name='registration_status'), default='scheduled', nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

MODEL_MAP = {
    'user': User,
    'patient': Patient,
    'doctor': Doctor,
    'department': Department,
    'schedule': Schedule,
    'registration': Registration
}