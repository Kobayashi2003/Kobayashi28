import { 
  VN, Release, Character, Producer, Staff, Tag, Trait,
  VN_Small, Release_Small, Character_Small, Producer_Small, 
  Staff_Small, Tag_Small, Trait_Small, User, Category, Mark,
  VNDBQueryParams, PaginatedResponse
} from "./types"
import { VNDB_BASE_URL, IMGSERVE_BASE_URL, USERSERVE_BASE_URL } from "./constants"

const getBaseUrl = (type: "vndb" | "imgserve" | "userserve") => {
  if (typeof window === "undefined") {
    switch (type) {
      case "vndb":
        return VNDB_BASE_URL
      case "imgserve":
        return IMGSERVE_BASE_URL
      case "userserve":
        return USERSERVE_BASE_URL
    }
  }
  switch (type) {
    case "vndb":
      return process.env.NEXT_PUBLIC_VNDB_BASE_URL || VNDB_BASE_URL
    case "imgserve":
      return process.env.NEXT_PUBLIC_IMGSERVE_BASE_URL || IMGSERVE_BASE_URL
    case "userserve":
      return process.env.NEXT_PUBLIC_USERSERVE_BASE_URL || USERSERVE_BASE_URL
  }
}

const fetchVNDB = async<T>(
  endpoint: string,
  params: VNDBQueryParams = {},
  processor?: (item: T) => T
): Promise<PaginatedResponse<T>> => {
  const queryString = new URLSearchParams(params as Record<string, string>).toString()
  const url = `${getBaseUrl("vndb")}/${endpoint}?${queryString}`
  const response = await fetch(url, { method: "GET", headers: {}, body: null })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  const data: PaginatedResponse<T> = await response.json()
  if (data.status === "ERROR") {
    throw new Error(`VNDB error! status: ${data.status}`)
  }
  if (data.status === "NOT_FOUND") {
    data.results = []
    data.more = false
    data.count = 0
  }
  return processor ? processVNDBResponse(data, processor) : data
}

const fetchUserserve = async<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE",
  body?: any,
): Promise<T> => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  const token = localStorage.getItem('access_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${getBaseUrl("userserve")}/${endpoint}`, { method, headers, body: JSON.stringify(body) })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  return await response.json()
}

function convertToImgserveUrl(url: string): string {
  const match = url.match(/^https?:\/\/[^\/]+\/(cv|sf|ch|cv\.t|sf\.t|ch\.t)\/\d+\/(\d+)\.jpg$/)
  if (!match) return url

  const [, type, id] = match
  return `${IMGSERVE_BASE_URL}/${type}/${id}`
}

function processVNImages(vn: VN): VN {
  return {
    ...vn,
    image: vn.image && {
      ...vn.image,
      url: convertToImgserveUrl(vn.image.url),
      thumbnail: convertToImgserveUrl(vn.image.thumbnail)
    },
    screenshots: vn.screenshots.map(screenshot => ({
      ...screenshot,
      url: convertToImgserveUrl(screenshot.url),
      thumbnail: convertToImgserveUrl(screenshot.thumbnail)
    })) 
  }
}

function processCharacterImages(character: Character): Character {
  return {
    ...character,
    image: character.image && {
      ...character.image,
      url: convertToImgserveUrl(character.image.url)
    }
  }
}

function processReleaseImages(release: Release): Release {
  return {
    ...release,
    images: release.images.map(image => ({
      ...image,
      url: convertToImgserveUrl(image.url),
      thumbnail: convertToImgserveUrl(image.thumbnail)
    }))
  }
}

function processSmallVNImages(vn: VN_Small): VN_Small {
  return {
    ...vn,
    image: vn.image && {
      ...vn.image,
      url: convertToImgserveUrl(vn.image.url),
      thumbnail: convertToImgserveUrl(vn.image.thumbnail)
    }
  }
}

function processSmallCharacterImages(character: Character_Small): Character_Small {
  return {
    ...character,
    image: character.image && {
      ...character.image,
      url: convertToImgserveUrl(character.image.url),
    }
  }
}

function processVNDBResponse<T>(
  response: PaginatedResponse<T>,
  processor: (item: T) => T
): PaginatedResponse<T> {
  return {
    ...response,
    results: response.results.map(processor)
  }
}

export const api = {
  vn: (id?: string, params: VNDBQueryParams = {}) => {
    params.size = "large"; return fetchVNDB<VN>(`v/${id}`, params, processVNImages) },

  release: (id?: string, params: VNDBQueryParams = {}) => {
    params.size = "large"; return fetchVNDB<Release>(`r/${id}`, params, processReleaseImages) },

  producer: (id?: string, params: VNDBQueryParams = {}) => {
    params.size = "large"; return fetchVNDB<Producer>(`p/${id}`, params) },

  character: (id?: string, params: VNDBQueryParams = {}) => {
    params.size = "large"; return fetchVNDB<Character>(`c/${id}`, params, processCharacterImages) },

  staff: (id?: string, params: VNDBQueryParams = {}) => {
    params.size = "large"; return fetchVNDB<Staff>(`s/${id}`, params) },

  tag: (id?: string, params: VNDBQueryParams = {}) => {
    params.size = "large"; return fetchVNDB<Tag>(`g/${id}`, params) },

  trait: (id?: string, params: VNDBQueryParams = {}) => {
    params.size = "large"; return fetchVNDB<Trait>(`i/${id}`, params) },

  small: {
    vn: (id?: string, params: VNDBQueryParams = {}) => {
      params.size = "small"; return fetchVNDB<VN_Small>(`v/${id}`, params, processSmallVNImages) },

    release: (id?: string, params: VNDBQueryParams = {}) => {
      params.size = "small"; return fetchVNDB<Release_Small>(`r/${id}`, params) },

    character: (id?: string, params: VNDBQueryParams = {}) => {
      params.size = "small"; return fetchVNDB<Character_Small>(`c/${id}`, params, processSmallCharacterImages) },

    producer: (id?: string, params: VNDBQueryParams = {}) => {
      params.size = "small"; return fetchVNDB<Producer_Small>(`p/${id}`, params) },

    staff: (id?: string, params: VNDBQueryParams = {}) => {
      params.size = "small"; return fetchVNDB<Staff_Small>(`s/${id}`, params) },

    tag: (id?: string, params: VNDBQueryParams = {}) => {
      params.size = "small"; return fetchVNDB<Tag_Small>(`g/${id}`, params) },

    trait: (id?: string, params: VNDBQueryParams = {}) => {
      params.size = "small"; return fetchVNDB<Trait_Small>(`i/${id}`, params) },
  },

  user:{
    login: async (username: string, password: string) => {
      return await fetchUserserve<{ access_token: string, username: string }>("login", "POST", { username, password }) },

    register: async (username: string, password: string) => {
      return await fetchUserserve<{ access_token: string, username: string }>("register", "POST", { username, password }) },

    get: async (username: string) => {
      return await fetchUserserve<User>(`u${username}`, "GET") },

    changeUsername: async (old_username: string, new_username: string) => {
      return await fetchUserserve<User>(`u${old_username}`, "PUT", { username: new_username }) },

    changePassword: async (username: string, oldPassword: string, newPassword: string) => {
      return await fetchUserserve<User>(`u${username}/change_password`, "POST", { old_password: oldPassword, new_password: newPassword }) },
  },

  category:{
    get: async (type: string) => {
      return await fetchUserserve<Category[]>(`${type}/c`, "GET") },

    create: async (type: string, categoryName: string) => {
      return await fetchUserserve<Category>(`${type}/c`, "POST", { category_name: categoryName }) },

    update: async (type: string, categoryId: number, newCategoryName: string) => {
      return await fetchUserserve<Category>(`${type}/c${categoryId}`, "PUT", { category_name: newCategoryName }) },
    
    delete: async (type: string, categoryId: number) => {
      return await fetchUserserve<{ message: string }>(`${type}/c${categoryId}`, "DELETE") },

    addMark: async (type: string, categoryId: number, markId: number) => {
      return await fetchUserserve<Category>(`${type}/c${categoryId}/m`, "POST", { mark_id: markId }) },

    removeMark: async (type: string, categoryId: number, markId: number) => {
      return await fetchUserserve<Category>(`${type}/c${categoryId}/m/${markId}`, "DELETE") },

    clearMarks: async (type: string, categoryId: number) => {
      return await fetchUserserve<{ message: string }>(`${type}/c${categoryId}/m`, "DELETE") },

    getMarks: async (type: string, categoryId: number) => {
      return await fetchUserserve<{ results: Mark[] }>(`${type}/c${categoryId}/m`, "GET") },
  },

  mark: {
    isMarked: async (type: string, markId: number) => {
      return await fetchUserserve<{ categoryIds: number[] }>(`${type}/m/${markId}`, "POST") }
  }
}