"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useSearchContext } from "@/context/SearchContext"

import { cn } from "@/lib/utils"
import { SearchBar } from "@/components/input/SearchBar"
import { FromSwitch } from "@/components/selector/FromSwitch"
import { TypeSelector1 } from "@/components/selector/TypeSelector1"
import { OrderSwitch } from "@/components/selector/OrderSwitch"
import { FilterButton } from "@/components/button/FilterButton"
import { SettingsButton } from "@/components/button/SettingsButton"
import { SubmitButton } from "@/components/button/SubmitButton"
import { FiltersDialog } from "@/components/dialog/FiltersDialog"
import { SortByDialog } from "@/components/dialog/SortByDialog"


interface SearchHeaderProps {
  className?: string
}

const TypeMap = {
  "vn": "v",
  "release": "r",
  "character": "c",
  "producer": "p",
  "staff": "s",
  "tag": "g",
  "trait": "i",
}

export function SearchHeader({ className }: SearchHeaderProps) {

  const { searchFrom, searchType, sortBy, sortOrder,
    setSearchFrom, setSearchType, setSortBy, setSortOrder } = useSearchContext()

  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

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
    router.push(`/${TypeMap[searchType as keyof typeof TypeMap]}?${searchParams.toString()}`)
    setLoading(false)
  }

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
        setOrder={(order) => {
          setSortOrder(order)
          handleSubmit()
        }}
        disabled={loading}
      />
      <SettingsButton
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
        setSortBy={(sortBy: string) => {
          setSortBy(sortBy)
          handleSubmit()
        }}
      />
    </div>
  )
}
