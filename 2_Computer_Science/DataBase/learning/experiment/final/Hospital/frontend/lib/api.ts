interface User {
  id: number;
  is_admin: boolean;
  username: string;
  phone_number: string;
  password_hash?: string;
  bio?: string;
  created_at: string;
  updated_at: string;
}

interface Patient {
  id: number;
  user_id: number;
  name: string;
  gender: string;
  birthday: string;
  phone_number: string;
  created_at: string;
  updated_at: string;
}

interface Doctor {
  id: number;
  name: string;
  gender: string;
  email: string;
  phone_number: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

interface Department {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

interface Registration {
  id: number;
  patient_id: number;
  schedule_id: number;
  status: 'scheduled' | 'completed' | 'cancelled';
  notes?: string;
  created_at: string;
  updated_at: string;
}

interface Schedule {
  id: number;
  doctor_id: number;
  start_time: string;
  end_time: string;
  created_at: string;
  updated_at: string;
}

interface PaginatedResponse<T> {
  results: T[];
  more: boolean;
  count: number;
}

const BASE_URL = 'http://localhost:5000/api';

async function fetchWithErrorHandling(url: string, options: RequestInit = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || 'An error occurred while fetching the data.');
  }
  return response.json();
}

export const api = {
  
}