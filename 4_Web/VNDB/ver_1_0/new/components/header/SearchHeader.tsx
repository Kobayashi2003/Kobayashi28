"use client"

import { useState, useEffect } from "react"
import { useRouter, usePathname } from "next/navigation"
import { useSearchContext } from "@/context/SearchContext"

import { cn } from "@/lib/utils"
import { SearchBar } from "@/components/input/SearchBar"
import { FromSwitch } from "@/components/selector/FromSwitch"
import { TypeSelector1 } from "@/components/selector/TypeSelector1"
import { OrderSwitch } from "@/components/selector/OrderSwitch"
import { FilterButton } from "@/components/button/FilterButton"
import { Settings2Button } from "@/components/button/Settings2Button"
import { SubmitButton } from "@/components/button/SubmitButton"
import { FiltersDialog } from "@/components/dialog/FiltersDialog"
import { SortByDialog } from "@/components/dialog/SortByDialog"


interface SearchHeaderProps {
  className?: string
}

export function SearchHeader({ className }: SearchHeaderProps) {

  const pathname = usePathname()
  const isSearching = (
    pathname.match(/^\/[vrcpsgi](\?|$)/) !== null
  )

  const { searchFrom, searchType, sortBy, sortOrder,
    setSearchFrom, setSearchType, setSortBy, setSortOrder } = useSearchContext()

  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const [searchQuery, setSearchQuery] = useState("")
  const [filtersParams, setFiltersParams] = useState<Record<string, string>>({})
  const [filtersDialogOpen, setFiltersDialogOpen] = useState(false)
  const [sortByDialogOpen, setSortByDialogOpen] = useState(false)

  const handleSubmit = (e?: React.FormEvent<HTMLFormElement>) => {
    if (e) e.preventDefault()
    setLoading(true)
    const searchParams = new URLSearchParams(filtersParams)
    if (searchFrom === "local") searchParams.set("from", "local")
    if (searchFrom === "remote") searchParams.set("from", "remote")
    if (searchQuery !== "") searchParams.set("search", searchQuery)
    if (sortBy !== "") searchParams.set("sort", sortBy)
    if (sortOrder !== "") searchParams.set("reverse", (sortOrder === "desc") ? "True" : "False")
    router.push(`/${searchType}?${searchParams.toString()}`)
    setLoading(false)
  }

  // useEffect(() => {
  //   if (isSearching) handleSubmit()
  // }, [sortOrder])

  return (
    <div className={cn("flex flex-row justify-center items-center gap-2", className)}>
      <FromSwitch
        selected={searchFrom}
        setSelected={setSearchFrom}
        disabled={loading}
      />
      <TypeSelector1
        selected={searchType}
        onSelect={setSearchType}
        disabled={loading}
      />
      <FilterButton
        onClick={() => setFiltersDialogOpen(true)}
        disabled={loading}
      />
      <form onSubmit={handleSubmit}>
        <SearchBar
          input={searchQuery}
          setInput={setSearchQuery}
          placeholder="Search..."
          disabled={loading}
        />
      </form>
      <SubmitButton
        handleSubmit={handleSubmit}
        disabled={loading}
      />
      <OrderSwitch
        order={sortOrder}
        setOrder={setSortOrder}
        disabled={loading}
      />
      <Settings2Button
        onClick={() => setSortByDialogOpen(true)}
        disabled={loading}
      />
      <FiltersDialog
        open={filtersDialogOpen}
        setOpen={setFiltersDialogOpen}
        type={searchType}
        setFilters={setFiltersParams}
      />
      <SortByDialog
        open={sortByDialogOpen}
        setOpen={setSortByDialogOpen}
        type={searchType}
        from={searchFrom}
        sortBy={sortBy}
        setSortBy={setSortBy}
      />
    </div>
  )
}
