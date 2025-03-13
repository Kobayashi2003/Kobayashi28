"use client"

import { createContext, useContext, useState, useEffect } from "react"

interface SearchContextType {
  searchType: string
  sortBy: string
  sortOrder: string
  setSearchType: (type: string) => void
  setSortBy: (by: string) => void
  setSortOrder: (order: string) => void
}

const SearchContext = createContext<SearchContextType | undefined>(undefined)

export function useSearchContext() {
  const context = useContext(SearchContext)
  if (context === undefined) {
    throw new Error("useSearchContext must be used within a SearchProvider")
  }
  return context
}

export function SearchProvider({ children }: { children: React.ReactNode}) {
  const [searchType, setSearchTypeTemp] = useState<string>("vn")
  const [sortBy, setSortByTemp] = useState<string>("id")
  const [sortOrder, setSortOrderTemp] = useState<string>("asc")

  const setSearchType= (type: string) => {
    setSearchTypeTemp(type)
    localStorage.setItem("searchType", type)
    const sortBy = localStorage.getItem(`sortBy-${type}`)
    const sortOrder = localStorage.getItem(`sortOrder-${type}`)
    if (sortBy) setSortByTemp(sortBy)
    if (sortOrder) setSortOrderTemp(sortOrder)
  }

  const setSortBy = (by: string) => {
    setSortByTemp(by)
    localStorage.setItem(`sortBy-${searchType}`, by)
  }

  const setSortOrder = (order: string) => {
    setSortOrderTemp(order)
    localStorage.setItem(`sortOrder-${searchType}`, order)
  }
  
  useEffect(() => {
    const searchType = localStorage.getItem("searchType")
    const sortBy = localStorage.getItem(`sortBy-${searchType}`)
    const sortOrder = localStorage.getItem(`sortOrder-${searchType}`)
    if (searchType) setSearchTypeTemp(searchType)
    if (sortBy) setSortByTemp(sortBy)
    if (sortOrder) setSortOrderTemp(sortOrder)
  }, [])

  return (
    <SearchContext.Provider value={{ searchType, sortBy, sortOrder, setSearchType, setSortBy, setSortOrder }}>
      {children}
    </SearchContext.Provider>
  )
}
