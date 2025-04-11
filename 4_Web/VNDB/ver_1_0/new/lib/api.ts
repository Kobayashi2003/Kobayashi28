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
        return process.env.NEXT_PUBLIC_VNDB_BASE_URL || VNDB_BASE_URL
      case "imgserve":
        return process.env.NEXT_PUBLIC_IMGSERVE_BASE_URL || IMGSERVE_BASE_URL
      case "userserve":
        return process.env.NEXT_PUBLIC_USERSERVE_BASE_URL || USERSERVE_BASE_URL
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

const fetchVNDB = async<T>(
  endpoint: string,
  params: VNDBQueryParams = {},
  processor?: (item: T) => T,
  abortSignal?: AbortSignal
): Promise<PaginatedResponse<T>> => {
  const queryString = new URLSearchParams(params as Record<string, string>).toString()
  const url = `${getBaseUrl("vndb")}/${endpoint}?${queryString}`
  const response = await fetch(url, { method: "GET", headers: {}, body: null, signal: abortSignal })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  const data: PaginatedResponse<T> = await response.json()
  if (data.status === "ERROR") {
    throw new Error(`VNDB error! ${data.results}`)
  }
  if (data.status === "NOT_FOUND") {
    data.results = []
    data.more = false
    data.count = 0
  }
  return processor ? processVNDBResponse(data, processor) : data
}

const fetchVNDBById = async<T>(
  endpoint: string,
  params: VNDBQueryParams = {},
  processor?: (item: T) => T,
  abortSignal?: AbortSignal
): Promise<T> => {
  const queryString = new URLSearchParams(params as Record<string, string>).toString()
  const url = `${getBaseUrl("vndb")}/${endpoint}?${queryString}`
  const response = await fetch(url, { method: "GET", headers: {}, body: null, signal: abortSignal })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  const data: PaginatedResponse<T> = await response.json()
  if (data.status === "ERROR" || data.status === "NOT_FOUND") {
    throw new Error(`VNDB error! status: ${data.status}`)
  }
  const result: T = data.results[0]
  if (!result) {
    throw new Error(`VNDB error! status: ${data.status}`)
  }
  return processor ? processor(result) : result
}

const fetchUserserve = async<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE",
  body?: any,
  abortSignal?: AbortSignal
): Promise<T> => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  const token = localStorage.getItem('access_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${getBaseUrl("userserve")}/${endpoint}`, { method, headers, body: JSON.stringify(body), signal: abortSignal })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  return await response.json()
}

function convertToImgserveUrl(url: string): string {
  const match = url.match(/^https?:\/\/[^\/]+\/(cv|sf|ch|cv\.t|sf\.t|ch\.t)\/\d+\/(\d+)\.jpg$/)
  if (!match) return url

  const [, type, id] = match
  return `${getBaseUrl("imgserve")}/img/${type}/${id}`
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
  vn: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
    params.size = "large"; return fetchVNDB<VN>(`v`, params, processVNImages, abortSignal)
  },

  release: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
    params.size = "large"; return fetchVNDB<Release>(`r`, params, processReleaseImages, abortSignal)
  },

  producer: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
    params.size = "large"; return fetchVNDB<Producer>(`p`, params, undefined, abortSignal)
  },

  character: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
    params.size = "large"; return fetchVNDB<Character>(`c`, params, processCharacterImages, abortSignal)
  },

  staff: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
    params.size = "large"; return fetchVNDB<Staff>(`s`, params, undefined, abortSignal)
  },

  tag: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
    params.size = "large"; return fetchVNDB<Tag>(`g`, params, undefined, abortSignal)
  },

  trait: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
    params.size = "large"; return fetchVNDB<Trait>(`i`, params, undefined, abortSignal)
  },

  by_id: {
    vn: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "large"; return fetchVNDBById<VN>(`v${id}`, params, processVNImages, abortSignal)
    },

    release: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "large"; return fetchVNDBById<Release>(`r${id}`, params, processReleaseImages, abortSignal)
    },

    character: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "large"; return fetchVNDBById<Character>(`c${id}`, params, processCharacterImages, abortSignal)
    },

    producer: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "large"; return fetchVNDBById<Producer>(`p${id}`, params, undefined, abortSignal)
    },

    staff: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "large"; return fetchVNDBById<Staff>(`s${id}`, params, undefined, abortSignal)
    },

    tag: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "large"; return fetchVNDBById<Tag>(`g${id}`, params, undefined, abortSignal)
    },

    trait: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "large"; return fetchVNDBById<Trait>(`i${id}`, params, undefined, abortSignal)
    }
  },

  small: {
    vn: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "small"; return fetchVNDB<VN_Small>(`v`, params, processSmallVNImages, abortSignal)
    },

    release: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "small"; return fetchVNDB<Release_Small>(`r`, params, undefined, abortSignal)
    },

    character: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "small"; return fetchVNDB<Character_Small>(`c`, params, processSmallCharacterImages, abortSignal)
    },

    producer: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "small"; return fetchVNDB<Producer_Small>(`p`, params, undefined, abortSignal)
    },

    staff: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "small"; return fetchVNDB<Staff_Small>(`s`, params, undefined, abortSignal)
    },

    tag: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "small"; return fetchVNDB<Tag_Small>(`g`, params, undefined, abortSignal)
    },

    trait: (params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
      params.size = "small"; return fetchVNDB<Trait_Small>(`i`, params, undefined, abortSignal)
    },

    by_id: {
      vn: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
        params.size = "small"; return fetchVNDBById<VN_Small>(`v${id}`, params, processSmallVNImages, abortSignal)
      },

      release: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
        params.size = "small"; return fetchVNDBById<Release_Small>(`r${id}`, params, undefined, abortSignal)
      },

      character: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
        params.size = "small"; return fetchVNDBById<Character_Small>(`c${id}`, params, processSmallCharacterImages, abortSignal)
      },

      producer: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
        params.size = "small"; return fetchVNDBById<Producer_Small>(`p${id}`, params, undefined, abortSignal)
      },

      staff: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
        params.size = "small"; return fetchVNDBById<Staff_Small>(`s${id}`, params, undefined, abortSignal)
      },

      tag: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
        params.size = "small"; return fetchVNDBById<Tag_Small>(`g${id}`, params, undefined, abortSignal)
      },

      trait: (id: number, params: VNDBQueryParams = {}, abortSignal?: AbortSignal) => {
        params.size = "small"; return fetchVNDBById<Trait_Small>(`i${id}`, params, undefined, abortSignal)
      }
    }
  },

  user: {
    login: async (username: string, password: string, abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ access_token: string, username: string }>("login", "POST", { username, password }, abortSignal)
    },

    register: async (username: string, password: string, abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ access_token: string, username: string }>("register", "POST", { username, password }, abortSignal)
    },

    get: async (username: string, abortSignal?: AbortSignal) => {
      return await fetchUserserve<User>(`u${username}`, "GET", undefined, abortSignal)
    },

    changeUsername: async (old_username: string, new_username: string, abortSignal?: AbortSignal) => {
      return await fetchUserserve<User>(`u${old_username}`, "PUT", { username: new_username }, abortSignal)
    },

    changePassword: async (username: string, oldPassword: string, newPassword: string, abortSignal?: AbortSignal) => {
      return await fetchUserserve<User>(`u${username}/change_password`, "POST", { old_password: oldPassword, new_password: newPassword }, abortSignal)
    },
  },

  category: {
    get: async (type: string, abortSignal?: AbortSignal) => {
      return await fetchUserserve<Category[]>(`${type}/c`, "GET", undefined, abortSignal)
    },

    create: async (type: string, categoryName: string, abortSignal?: AbortSignal) => {
      return await fetchUserserve<Category>(`${type}/c`, "POST", { category_name: categoryName }, abortSignal)
    },

    update: async (type: string, categoryId: number, newCategoryName: string, abortSignal?: AbortSignal) => {
      return await fetchUserserve<Category>(`${type}/c${categoryId}`, "PUT", { category_name: newCategoryName }, abortSignal)
    },

    delete: async (type: string, categoryId: number, abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ message: string }>(`${type}/c${categoryId}`, "DELETE", undefined, abortSignal)
    },

    containsMark: async (type: string, categoryId: number, markId: number, abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ containsMark: boolean }>(`${type}/c${categoryId}/m${markId}`, "GET", undefined, abortSignal)
    },

    addMark: async (type: string, categoryId: number, markId: number, abortSignal?: AbortSignal) => {
      return await fetchUserserve<Category>(`${type}/c${categoryId}/m`, "POST", { mark_id: markId }, abortSignal)
    },

    removeMark: async (type: string, categoryId: number, markId: number, abortSignal?: AbortSignal) => {
      return await fetchUserserve<Category>(`${type}/c${categoryId}/m${markId}`, "DELETE", undefined, abortSignal)
    },

    clearMarks: async (type: string, categoryId: number, abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ message: string }>(`${type}/c${categoryId}/m`, "DELETE", undefined, abortSignal)
    },

    getMarks: async (type: string, categoryId: number, abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ results: Mark[] }>(`${type}/c${categoryId}/m`, "GET", undefined, abortSignal)
    },
  },

  mark: {
    isMarked: async (type: string, markId: number, abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ isMarked: boolean }>(`${type}/m${markId}/is_marked`, "GET", undefined, abortSignal)
    },

    areMarked: async (type: string, markIds: number[], abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ isMarked: { [key: number]: boolean } }>(`${type}/m/is_marked`, "POST", { mark_ids: markIds }, abortSignal)
    },

    getCategoriesByMark: async (type: string, markId: number, abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ categoryIds: number[] }>(`${type}/m${markId}/c`, "GET", undefined, abortSignal)
    },

    getCategoriesByMarks: async (type: string, markIds: number[], abortSignal?: AbortSignal) => {
      return await fetchUserserve<{ categoryIds: { [key: number]: number[] } }>(`${type}/m/c`, "POST", { mark_ids: markIds }, abortSignal)
    }
  }
}