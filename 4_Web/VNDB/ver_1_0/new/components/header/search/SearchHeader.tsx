"use client"

import { useState } from "react"
import { useRouter } from "next/navigation";
import { useSearchContext } from "@/context/SearchContext"
import { SearchTypeSelector } from "./SearchTypeSelector"
import { SearchSortSelector } from "./SearchSortSelector"
// import { SearchBar } from "./SearchBar"
import { SearchFilters } from "./SearchFilters"
import { SearchSubmitButton } from "./SearchSubmitButton"

import { SearchBar } from "@/components/input/SearchBar"

interface SearchHeaderProps {
  className?: string
}

function getSearchTypeShort(searchType: string) {
  switch (searchType) {
    case "vn":
      return "v"
    case "release":
      return "r"
    case "character":
      return "c"
    case "producer":
      return "p"
    case "staff":
      return "s"
    case "tag":
      return "g"
    case "trait":
      return "i"
    default:
      return "v"
  }
}

export function SearchHeader({ className }: SearchHeaderProps) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const { searchType, sortBy, sortOrder, setSearchType, setSortBy, setSortOrder } = useSearchContext()
  const [searchQuery, setSearchQuery] = useState("")
  const [searchFilters, setSearchFilters] = useState<Record<string, string>>({})

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    setIsLoading(true)
    const searchParams = new URLSearchParams(searchFilters)
    if (searchQuery !== "") searchParams.set("search", searchQuery)
    if (sortBy !== "") searchParams.set("sort", sortBy)
    if (sortOrder !== "") searchParams.set("reverse", (sortOrder === "desc") ? "True" : "False")
    router.push(`/${getSearchTypeShort(searchType)}?${searchParams.toString()}`)
    setIsLoading(false)
  }

  return (
    <div className={`flex flex-row justify-center items-center gap-1 ${className}`}>
      <SearchTypeSelector searchType={searchType} onSearchTypeChange={setSearchType} />
      <SearchSortSelector searchType={searchType} sortBy={sortBy} sortOrder={sortOrder} setSortBy={setSortBy} setSortOrder={setSortOrder} />
      <form onSubmit={handleSubmit}>
        {/* <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} /> */}
        <SearchBar input={searchQuery} setInput={setSearchQuery} placeholder="Search..." />
      </form>
      <SearchFilters SearchType={searchType} setSearchFilters={setSearchFilters} />
      <SearchSubmitButton isLoading={isLoading} handleSubmit={handleSubmit} />
    </div>
  )
}
