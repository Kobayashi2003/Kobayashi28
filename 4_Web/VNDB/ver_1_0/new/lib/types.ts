export interface PaginationParams {
  page?: number
  limit?: number
  sort?: string
  reverse?: boolean
}

export interface PaginatedResponse<T> {
  results: T[]
  status: string
  source: string
  more: boolean
  count: number
}


export interface VNDBQueryParams extends PaginationParams {
  from?: 'local' | 'remote'
  size?: 'small' | 'large'
  [key: string]: any
}

export interface MarksQueryParams extends PaginationParams {
  type: 'vn' | 'character' | 'producer' | 'staff'
  category_id: number
}


export interface VN {
  id: string
  title: string
  alttitle?: string
  titles: Array<{
    lang: string
    title: string
    latin?: string
    official: boolean
    main: boolean
  }>
  aliases: string[]
  olang: string
  devstatus: number
  released?: string
  languages: string[]
  platforms: string[]
  image?: {
    url: string
    dims: [number, number]
    thumbnail: string
    thumbnail_dims: [number, number]
    sexual: number
    violence: number
  }
  length?: number
  length_minutes?: number
  length_votes: number
  description?: string
  average?: number
  rating?: number
  votecount: number
  screenshots: Array<{
    url: string
    dims: [number, number]
    sexual: number
    violence: number
    thumbnail: string
    thumbnail_dims: [number, number]
    release: {
      id: string
      title: string
    }
  }>
  relations: Array<{
    id: string
    title: string
    relation: string
    relation_official: boolean
  }>
  tags: Array<{
    id: string
    name: string
    category: string
    rating: number
    spoiler: number
    lie: boolean
  }>
  developers: Array<{
    id: string
    name: string
    original?: string
  }>
  editions: Array<{
    eid: string
    lang?: string
    name: string
    official: boolean
  }>
  staff: Array<{
    id: string
    name: string
    original?: string
    eid?: number
    role: string
    note?: string
  }>
  va: Array<{
    note?: string
    staff: {
      id: string
      name: string
      original?: string
    }
    character: {
      id: string
      name: string
      original?: string
    }
  }>
  extlinks: Array<{
    url: string
    label: string
    name: string
    id: string
  }>
  characters: Array<{
    id: string
    name: string
    sex?: [string, string]
    vns: Array<{
      id: string
      role: string
      spoiler: number
    }>
  }>
  releases?: Array<{
    id: string
    title: string
    vns: Array<{
      id: string
      rtype: string
    }>
    producers?: Array<{
      id: string
      developer: boolean
      publisher: boolean
    }>
  }>
}

export interface Release {
  id: string
  title: string
  alttitle?: string
  languages: Array<{
    lang: string
    title?: string
    latin?: string
    mtl: boolean
    main: boolean
  }>
  platforms: string[]
  media: Array<{
    medium: string
    qty: number
  }>
  vns: Array<{
    id: string
    title: string
    rtype: string
  }>
  producers?: Array<{
    id: string
    developer: boolean
    publisher: boolean
  }>
  images: Array<{
    id: string
    type: string
    vn?: string
    languages?: string[]
    photo: boolean
    url: string
    dims: [number, number]
    sexual: number
    violence: number
    thumbnail: string
    thumbnail_dims: [number, number]
  }>
  released: string
  minage?: number
  patch: boolean
  freeware: boolean
  uncensored?: boolean
  official: boolean
  has_ero: boolean
  resolution?: string
  engine?: string
  voiced?: number
  notes?: string
  gtin?: string
  catalog?: string
  extlinks: Array<{
    url: string
    label: string
    name: string
    id: string
  }>
}

export interface Character {
  id: string
  name: string
  original?: string
  aliases: string[]
  description?: string
  image?: {
    url: string
    dims: [number, number]
    sexual: number
    violence: number
  }
  blood_type?: string
  height?: number
  weight?: number
  bust?: number
  waist?: number
  hips?: number
  cup?: string
  age?: number
  birthday?: string
  sex?: [string, string]
  vns: Array<{
    id: string
    role: string
    title: string
    release?: {
      id: string
      title: string
    }
  }>
  traits: Array<{
    id: string
    name: string
    group_id?: string
    group_name?: string
    spoiler: number
    lie: boolean
  }>
  seiyuu: Array<{
    id: string
    name: string
    original?: string
    note?: string
  }>
}

export interface Producer {
  id: string
  name: string
  original?: string
  aliases: string[]
  lang: string
  type: string
  description?: string
  extlinks: Array<{
    url: string
    label: string
    name:  string
    id: string
  }>
}

export interface Staff {
  id: string
  aid: string
  ismain: boolean
  name: string
  original?: string
  lang: string
  gender?: string
  description?: string
  extlinks: Array<{
    url: string
    label: string
    name: string
    id: string
  }>
  aliases: Array<{
    aid: string
    name: string
    latin?: string
    is_main: boolean
  }>
}

export interface Tag {
  id: string
  name: string
  aliases: string[]
  description: string
  category: string
  searchable: boolean
  applicable: boolean
  vn_count: number
}

export interface Trait {
  id: string
  name: string
  aliases: string[]
  description: string
  searchable: boolean
  applicable: boolean
  group_id?: string
  group_name?: string
  char_count: number
}

export interface User {
  id: number
  is_admin: boolean
  username: string
  created_at: string // ISO 8601 date string
  updated_at: string // ISO 8601 date string
}

export interface Category {
  id: number
  user_id: number
  category_name: string
  marks: Mark[]
  type: 'vn' | 'character' | 'producer' | 'staff'
  created_at: string // ISO 8601 date string
  updated_at: string // ISO 8601 date string
}

export interface Mark {
  id: number
  marked_at: string // ISO 8601 date string
}

export interface VN_Small {
  id: string
  title: string
  titles: Array<{
    lang: string
    title: string
    latin?: string
    official: boolean
    main: boolean 
  }>
  released: string
  image?: {
    url: string
    dims: [number, number]
    thumbnail: string
    thumbnail_dims: [number, number]
    sexual: number
    violence: number
  }
}

export interface Release_Small {
  id: string
  title: string
  released: string
  vns: Array<{
    id: string
    rtype: string
  }>
  producers: Array<{
    id: string
    developer: boolean
    publisher: boolean
  }>
}

export interface Character_Small {
  id: string
  name: string 
  original?: string
  sex?: [string, string]
  vns: Array<{
    id: string
    role: string
    spoiler: number
  }>
  image?: {
    url: string
    dims: [number, number]
    sexual: number
    violence: number
  }
}

export interface Producer_Small {
  id: string
  name: string 
  original?: string
}

export interface Staff_Small {
  id: string
  name: string
  original?: string
}

export interface Tag_Small {
  id: string 
  name: string
  category: string
}

export interface Trait_Small {
  id: string  
  name: string
  group_id?: string
  group_name?: string
}