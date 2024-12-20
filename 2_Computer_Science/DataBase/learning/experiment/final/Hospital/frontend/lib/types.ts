export interface User {
  id: number;
  is_admin: boolean;
  username: string;
  phone_number: string;
  password_hash?: string;
  bio?: string;
  created_at: string;
  updated_at: string;
}

export interface Patient {
  id: number;
  user_id: number;
  name: string;
  gender: string;
  birthday: string;
  phone_number: string;
  created_at: string;
  updated_at: string;
}

export interface Doctor {
  id: number;
  name: string;
  gender: string;
  email: string;
  phone_number: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Department {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Registration {
  id: number;
  patient_id: number;
  schedule_id: number;
  status: 'scheduled' | 'completed' | 'cancelled';
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Schedule {
  id: number;
  doctor_id: number;
  start_time: string;
  end_time: string;
  created_at: string;
  updated_at: string;
}

export interface Affiliation {
  doctor: Doctor;
  department: Department;
}

export interface PaginatedResponse<T> {
  results: T[];
  more: boolean;
  count: number;
}