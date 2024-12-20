import { User, Patient, Doctor, Department, Registration, Schedule, Affiliation, PaginatedResponse } from './types';

const BASE_URL = 'http://localhost:5000';

async function fetchWithErrorHandling(url: string, options: RequestInit = {}): Promise<any | null> {
  const response = await fetch(url, options);
  if (!response.ok) {
    const errorMessage = `HTTP error! status: ${response.status}`;
    throw new Error(errorMessage);
  }
  
  try {
    return await response.json();
  } catch {
    return null;
  }
}

export const api = {

  // --------------------------------------
  // User related functions
  login: async (username: string, password: string): Promise<{ access_token: string; user: User }> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
  },

  register: async (userData: { username: string; phone_number: string; password: string; bio?: string }): Promise<User> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
  },

  getCurrentUser: async (token: string): Promise<User> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
  },

  updateCurrentUser: async (userData: Partial<User>, token: string): Promise<User> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/me`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(userData),
    });
  },

  deleteCurrentUser: async (token: string): Promise<void> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/me`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` },
    });
  },

  changeCurrentUserPassword: async (oldPassword: string, newPassword: string, token: string): Promise<{ message: string }> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/me/change_password`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
    });
  },

  grantAdminPrivileges: async (userId: number, adminPassword: string, token: string): Promise<{ message: string }> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/grant_admin`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ user_id: userId, admin_password: adminPassword }),
    });
  },

  revokeAdminPrivileges: async (userId: number, adminPassword: string, token: string): Promise<{ message: string }> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/revoke_admin`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ user_id: userId, admin_password: adminPassword }),
    });
  },

  getUser: async (userId: number, token: string): Promise<User> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/${userId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  createAdmin: async (userData: { username: string; phone_number: string; password: string; bio?: string }, token: string): Promise<User> => {
    return fetchWithErrorHandling(`${BASE_URL}/users`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(userData),
    });
  },

  updateUser: async (userId: number, userData: Partial<User>, token: string): Promise<User> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(userData),
    });
  },

  deleteUser: async (userId: number, token: string): Promise<void> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/${userId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  changeUserPassword: async (userId: number, oldPassword: string, newPassword: string, token: string): Promise<{ message: string }> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/${userId}/change_password`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
    });
  },

  getUsers: async (page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<User>> => {
    return fetchWithErrorHandling(`${BASE_URL}/users?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  searchUsers: async (query: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<User>> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/search`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, page, per_page: perPage, sort, reverse }),
    });
  },

  // --------------------------------------
  // Patient related functions
  getPatient: async (patientId: number, token: string): Promise<Patient> => {
    return fetchWithErrorHandling(`${BASE_URL}/patients/${patientId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  createPatient: async (patientData: Omit<Patient, 'id' | 'user_id' | 'created_at' | 'updated_at'>, token: string): Promise<Patient> => {
    return fetchWithErrorHandling(`${BASE_URL}/patients`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(patientData),
    });
  },

  updatePatient: async (patientId: number, patientData: Partial<Patient>, token: string): Promise<Patient> => {
    return fetchWithErrorHandling(`${BASE_URL}/patients/${patientId}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(patientData),
    });
  },

  deletePatient: async (patientId: number, token: string): Promise<void> => {
    return fetchWithErrorHandling(`${BASE_URL}/patients/${patientId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  searchPatients: async (query: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Patient>> => {
    return fetchWithErrorHandling(`${BASE_URL}/patients/search`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, page, per_page: perPage, sort, reverse }),
    });
  },

  getPatients: async (page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Patient>> => {
    return fetchWithErrorHandling(`${BASE_URL}/patients/all?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getUserPatients: async (userId: number, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Patient>> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/${userId}/patients?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  searchUserPatients: async (userId: number, query: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Patient>> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/${userId}/patients/search`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, page, per_page: perPage, sort, reverse }),
    });
  },

  // --------------------------------------
  // Doctor related functions
  getDoctor: async (doctorId: number, token: string): Promise<Doctor> => {
    return fetchWithErrorHandling(`${BASE_URL}/doctors/${doctorId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  createDoctor: async (doctorData: Omit<Doctor, 'id' | 'created_at' | 'updated_at'>, token: string): Promise<Doctor> => {
    return fetchWithErrorHandling(`${BASE_URL}/doctors`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(doctorData),
    });
  },

  updateDoctor: async (doctorId: number, doctorData: Partial<Doctor>, token: string): Promise<Doctor> => {
    return fetchWithErrorHandling(`${BASE_URL}/doctors/${doctorId}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(doctorData),
    });
  },

  deleteDoctor: async (doctorId: number, token: string): Promise<void> => {
    return fetchWithErrorHandling(`${BASE_URL}/doctors/${doctorId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getDoctors: async (page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Doctor>> => {
    return fetchWithErrorHandling(`${BASE_URL}/doctors?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  searchDoctors: async (query: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Doctor>> => {
    return fetchWithErrorHandling(`${BASE_URL}/doctors/search`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, page, per_page: perPage, sort, reverse }),
    });
  },

  // --------------------------------------
  // Department related functions
  getDepartment: async (departmentId: number, token: string): Promise<Department> => {
    return fetchWithErrorHandling(`${BASE_URL}/departments/${departmentId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  createDepartment: async (departmentData: Omit<Department, 'id' | 'created_at' | 'updated_at'>, token: string): Promise<Department> => {
    return fetchWithErrorHandling(`${BASE_URL}/departments`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(departmentData),
    });
  },

  updateDepartment: async (departmentId: number, departmentData: Partial<Department>, token: string): Promise<Department> => {
    return fetchWithErrorHandling(`${BASE_URL}/departments/${departmentId}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(departmentData),
    });
  },

  deleteDepartment: async (departmentId: number, token: string): Promise<void> => {
    return fetchWithErrorHandling(`${BASE_URL}/departments/${departmentId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getDepartments: async (page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Department>> => {
    return fetchWithErrorHandling(`${BASE_URL}/departments?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  searchDepartments: async (query: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Department>> => {
    return fetchWithErrorHandling(`${BASE_URL}/departments/search`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, page, per_page: perPage, sort, reverse }),
    });
  },

  // --------------------------------------
  // Registration related functions
  getRegistration: async (registrationId: number, token: string): Promise<Registration> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations/${registrationId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  createRegistration: async (registrationData: Omit<Registration, 'id' | 'status' | 'created_at' | 'updated_at'>, token: string): Promise<Registration> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(registrationData),
    });
  },

  updateRegistration: async (registrationId: number, registrationData: Partial<Registration>, token: string): Promise<Registration> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations/${registrationId}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(registrationData),
    });
  },

  deleteRegistration: async (registrationId: number, token: string): Promise<void> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations/${registrationId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getRegistrations: async (page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Registration>> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  searchRegistrations: async (query: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Registration>> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations/search`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, page, per_page: perPage, sort, reverse }),
    });
  },

  getUserRegistrations: async (userId: number, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Registration>> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/${userId}/registrations?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  searchUserRegistrations: async (userId: number, query: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Registration>> => {
    return fetchWithErrorHandling(`${BASE_URL}/users/${userId}/registrations/search`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, page, per_page: perPage, sort, reverse }),
    });
  },

  getRegistrationsByPatient: async (patientId: number, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Registration>> => {
    return fetchWithErrorHandling(`${BASE_URL}/patients/${patientId}/registrations?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getRegistrationsBySchedule: async (scheduleId: number, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Registration>> => {
    return fetchWithErrorHandling(`${BASE_URL}/schedules/${scheduleId}/registrations?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getRegistrationsByStatus: async (status: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Registration>> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations/status/${status}?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  cancelRegistration: async (registrationId: number, token: string): Promise<{ message: string }> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations/${registrationId}/cancel`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  completeRegistration: async (registrationId: number, token: string): Promise<{ message: string }> => {
    return fetchWithErrorHandling(`${BASE_URL}/registrations/${registrationId}/complete`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  // --------------------------------------
  // Schedule related functions
  getSchedule: async (scheduleId: number, token: string): Promise<Schedule> => {
    return fetchWithErrorHandling(`${BASE_URL}/schedules/${scheduleId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  createSchedule: async (scheduleData: Omit<Schedule, 'id' | 'available_slots' | 'created_at' | 'updated_at'>, token: string): Promise<Schedule> => {
    return fetchWithErrorHandling(`${BASE_URL}/schedules`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(scheduleData),
    });
  },

  updateSchedule: async (scheduleId: number, scheduleData: Partial<Schedule>, token: string): Promise<Schedule> => {
    return fetchWithErrorHandling(`${BASE_URL}/schedules/${scheduleId}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(scheduleData),
    });
  },

  deleteSchedule: async (scheduleId: number, token: string): Promise<void> => {
    return fetchWithErrorHandling(`${BASE_URL}/schedules/${scheduleId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getSchedules: async (page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Schedule>> => {
    return fetchWithErrorHandling(`${BASE_URL}/schedules?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  searchSchedules: async (query: string, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Schedule>> => {
    return fetchWithErrorHandling(`${BASE_URL}/schedules/search`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, page, per_page: perPage, sort, reverse }),
    });
  },

  getSchedulesByDoctor: async (doctorId: number, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Schedule>> => {
    return fetchWithErrorHandling(`${BASE_URL}/doctors/${doctorId}/schedules?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getSchedulesByDepartment: async (departmentId: number, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Schedule>> => {
    return fetchWithErrorHandling(`${BASE_URL}/departments/${departmentId}/schedules?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  // --------------------------------------
  // Affiliation related functions
  createAffiliation: async (affiliationData: { doctor_id: number; department_id: number }, token: string): Promise<{ message: string }> => {
    return fetchWithErrorHandling(`${BASE_URL}/affiliations`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(affiliationData),
    });
  },

  deleteAffiliation: async (doctorId: number, departmentId: number, token: string): Promise<void> => {
    return fetchWithErrorHandling(`${BASE_URL}/affiliations/${doctorId}/${departmentId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getAffiliations: async (page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Affiliation>> => {
    return fetchWithErrorHandling(`${BASE_URL}/affiliations?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getDepartmentsByDoctor: async (doctorId: number, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Department>> => {
    return fetchWithErrorHandling(`${BASE_URL}/doctors/${doctorId}/departments?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

  getDoctorsByDepartment: async (departmentId: number, page: number = 1, perPage: number = 10, sort: string = 'id', reverse: boolean = false, token: string): Promise<PaginatedResponse<Doctor>> => {
    return fetchWithErrorHandling(`${BASE_URL}/departments/${departmentId}/doctors?page=${page}&per_page=${perPage}&sort=${sort}&reverse=${reverse}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  }
}