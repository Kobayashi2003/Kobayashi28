import {
  VNDB_BASE_URL, IMGSERVE_BASE_URL, USERSERVE_BASE_URL
} from './constants';
import { 
  VisualNovelDataBaseQueryParams, VisualNovelDataBaseQueryResponse,
  VN, Release, Producer, Character, Staff, Tag, Trait, User, Category, Mark
} from './types';
import {
  processApiResponse, processVNImages, processReleaseImages, processCharacterImages
} from './process';


const isServer = typeof window === "undefined"

const getBaseUrl = (type: "vndb" | "imgserve" | "userserve") => {
  if (isServer) {
    switch (type) {
      case "vndb":
        return "http://localhost:5000"
      case "imgserve":
        return "http://localhost:5001"
      case "userserve":
        return "http://localhost:5002"
    }
  } else {
    switch (type) {
      case "vndb":
        return VNDB_BASE_URL
      case "imgserve":
        return IMGSERVE_BASE_URL
      case "userserve":
        return USERSERVE_BASE_URL
    }
  }
}

async function vndbQuery<T>(endpoint: string, params: VisualNovelDataBaseQueryParams = {}): Promise<VisualNovelDataBaseQueryResponse<T>> {
  const queryString = new URLSearchParams(params as Record<string, string>).toString();
  const response = await fetch(`${getBaseUrl("vndb")}/${endpoint}?${queryString}`);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

async function imgserveQuery(type: string, id: number): Promise<Blob> {
  const response = await fetch(`${getBaseUrl("imgserve")}/${type}/${id}`);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.blob();
}

async function userserveQuery<T>(endpoint: string, method: string = 'GET', body?: any): Promise<T> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  const token = localStorage.getItem('access_token');
  console.log(`TOKEN:${token}`)
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${getBaseUrl("userserve")}/${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

export const api = {

  vn: async (id?: string, params: VisualNovelDataBaseQueryParams = {}) => {
    const response = await vndbQuery<VN>(`v${id || ''}`, params);
    return processApiResponse(response, processVNImages);
  },

  release: async (id?: string, params: VisualNovelDataBaseQueryParams = {}) => {
    const response = await vndbQuery<Release>(`r${id || ''}`, params);
    return processApiResponse(response, processReleaseImages);
  },

  producer: (id?: string, params: VisualNovelDataBaseQueryParams = {}) => 
    vndbQuery<Producer>(`p${id || ''}`, params),

  character: async (id?: string, params: VisualNovelDataBaseQueryParams = {}) => {
    const response = await vndbQuery<Character>(`c${id || ''}`, params);
    return processApiResponse(response, processCharacterImages);
  },

  staff: (id?: string, params: VisualNovelDataBaseQueryParams = {}) => 
    vndbQuery<Staff>(`s${id || ''}`, params),

  tag: (id?: string, params: VisualNovelDataBaseQueryParams = {}) => 
    vndbQuery<Tag>(`g${id || ''}`, params),

  trait: (id?: string, params: VisualNovelDataBaseQueryParams = {}) => 
    vndbQuery<Trait>(`i${id || ''}`, params),

  image: (type: 'cv' | 'sf' | 'cv.t' | 'sf.t' | 'ch', id: number) => 
    imgserveQuery(type, id),

  login: (username: string, password: string) => 
    userserveQuery<{ access_token: string, username: string }>('login', 'POST', { username, password }),

  register: (username: string, password: string) => 
    userserveQuery<{ access_token: string, username: string }>('register', 'POST', { username, password }),

  getUser: (username: string) => 
    userserveQuery<User>(`u${username}`, 'GET'),

  updateUser: (old_username: string, new_username: string) => 
    userserveQuery<User>(`u${old_username}`, 'PUT', { username: new_username }),

  deleteUser: (username: string) => 
    userserveQuery<{ message: string }>(`u${username}`, 'DELETE'),

  changePassword: (username: string, oldPassword: string, newPassword: string) => 
    userserveQuery<{ message: string }>(`u${username}/change_password`, 'POST', { old_password: oldPassword, new_password: newPassword }),

  getCategories: (type: string) => 
    userserveQuery<Category[]>(`${type}/c`, 'GET'),

  createCategory: (type: string, categoryName: string) => 
    userserveQuery<Category>(`${type}/c`, 'POST', { category_name: categoryName }),

  getCategory: (type: string, categoryId: number) => 
    userserveQuery<Category>(`${type}/c${categoryId}`, 'GET'),

  updateCategory: (type: string, categoryId: number, categoryName: string) => 
    userserveQuery<Category>(`${type}/c${categoryId}`, 'PUT', { category_name: categoryName }),

  deleteCategory: (type: string, categoryId: number) => 
    userserveQuery<{ message: string }>(`${type}/c${categoryId}`, 'DELETE'),

  clearCategory: (type: string, categoryId: number) => 
    userserveQuery<{ message: string }>(`${type}/c${categoryId}/clear`, 'POST'),

  addMark: (type: string, categoryId: number, markId: number) => 
    userserveQuery<Category>(`${type}/c${categoryId}/m`, 'POST', { mark_id: markId }),

  removeMark: (type: string, categoryId: number, markId: number) => 
    userserveQuery<Category>(`${type}/c${categoryId}/m${markId}`, 'DELETE'),

  isMarked: (type: string, markId: number) =>
    userserveQuery<{categoryIds?:Array<number>}>(`${type}/m${markId}/c`, 'GET'),

  getMarks: async (
    type: string,
    categoryId: number,
    params: {
      page?: number
      limit?: number
      sort?: string
      reverse?: boolean
      count?: boolean
    } = {},
  ) => {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    }

    const token = localStorage.getItem("access_token")
    if (token) {
      headers["Authorization"] = `Bearer ${token}`
    }

    const queryParams = new URLSearchParams({
      ...params,
      page: params.page?.toString() || "1",
      limit: params.limit?.toString() || "100",
      sort: params.sort || "marked_at",
      reverse: params.reverse?.toString() || "true",
      count: params.count?.toString() || "true",
    })

    const response = await fetch(`${USERSERVE_BASE_URL}/${type}/c${categoryId}/m?${queryParams}`, {
      method: "GET",
      headers,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return (await response.json()) as {
      results: Mark[]
      more: boolean
      count?: number
    }
  },
};