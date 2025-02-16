"use client"

import { useState } from "react"

import type { SearchType } from "@/lib/types"
import { TypeSelect } from "./type-select"
import { SimpleSearch } from "./simple/simple-search"
import { AdvancedSearch } from "./advanced/advanced-search"

export function SearchHeader() {
  const [searchType, setSearchType] = useState<SearchType>("vn")

  return (
    <div className="w-full max-w-2xl mx-auto flex gap-2">
      <TypeSelect value={searchType} onValueChange={setSearchType} />
      <SimpleSearch searchType={searchType} />
      <AdvancedSearch searchType={searchType} />
    </div>
  )
}