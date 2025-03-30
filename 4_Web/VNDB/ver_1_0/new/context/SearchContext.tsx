"use client"

import { createContext, useContext, useState, useEffect } from "react"

interface SearchContextType {
  searchFrom: string
  searchType: string
  sortBy: string
  sortOrder: string
  setSearchFrom: (from: string) => void
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
  const [searchFrom, setSearchFromTemp] = useState<string>("both")
  const [searchType, setSearchTypeTemp] = useState<string>("v")
  const [sortBy, setSortByTemp] = useState<string>("id")
  const [sortOrder, setSortOrderTemp] = useState<string>("asc")

  const setSearchFrom = (from: string) => {
    setSearchFromTemp(from)
    localStorage.setItem("searchFrom", from)
  }

  const setSearchType= (type: string) => {
    setSearchTypeTemp(type)
    localStorage.setItem("searchType", type)
  }

  const setSortBy = (by: string) => {
    setSortByTemp(by)
    localStorage.setItem(`sortBy-${searchType}-${searchFrom}`, by)
  }

  const setSortOrder = (order: string) => {
    setSortOrderTemp(order)
    // localStorage.setItem(`sortOrder-${searchType}-${searchFrom}`, order)
    localStorage.setItem(`sortOrder`, order)
  }

  useEffect(() => {
    const searchFrom = localStorage.getItem("searchFrom") || "both"
    const searchType = localStorage.getItem("searchType") || "v"
    const sortBy = localStorage.getItem(`sortBy-${searchType}-${searchFrom}`) || "id"
    // const sortOrder = localStorage.getItem(`sortOrder-${searchType}-${searchFrom}`) || "asc"
    const sortOrder = localStorage.getItem(`sortOrder`) || "asc"
    setSearchFromTemp(searchFrom)
    setSearchTypeTemp(searchType)
    setSortByTemp(sortBy)
    setSortOrderTemp(sortOrder)
  }, [])
  
  useEffect(() => {
    const sortBy = localStorage.getItem(`sortBy-${searchType}-${searchFrom}`) || "id"
    // const sortOrder = localStorage.getItem(`sortOrder-${searchType}-${searchFrom}`) || "asc"
    const sortOrder = localStorage.getItem(`sortOrder`) || "asc"
    setSortByTemp(sortBy)
    setSortOrderTemp(sortOrder)
  }, [searchFrom, searchType])

  return (
    <SearchContext.Provider value={{ searchFrom, searchType, sortBy, sortOrder, setSearchFrom, setSearchType, setSortBy, setSortOrder }}>
      {children}
    </SearchContext.Provider>
  )
}
