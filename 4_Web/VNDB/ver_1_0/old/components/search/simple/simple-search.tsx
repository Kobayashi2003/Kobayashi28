"use client"

import { useState, useEffect } from "react"
import { useRouter, usePathname } from "next/navigation"
import { SearchIcon, SlidersHorizontal, ArrowRight, Loader2 } from "lucide-react"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

import type { SearchType } from "@/lib/types"

interface SimpleSearchProps {
  searchType: SearchType
}

interface SortOption {
  value: string
  label: string
}

const sortOptions: Record<SearchType, SortOption[]> = {
  vn: [
    { value: "id", label: "Id" },
    { value: "title", label: "Title" },
    { value: "released", label: "Release Date" }
  ],
  release: [
    { value: "id", label: "Id" },
    { value: "title", label: "Title" },
    { value: "released", label: "Release Date" },
  ],
  character: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name" },
  ],
  producer: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name" },
  ],
  staff: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name" },
  ],
  tag: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name"},
  ],
  trait: [
    { value: "id", label: "Id"},
    { value: "name", label: "Name"},
    { value: "group_id", label: "Group Id"},
    { value: "group_name", label: "Group Name"},
  ]
}

interface SimpleSearchParams {
  search?: string
  sort?: string
  order?: "asc" | "desc"
}

export function SimpleSearch({ searchType }: SimpleSearchProps) {
  const router = useRouter()
  const pathname = usePathname()
  const [searchQuery, setSearchQuery] = useState("")
  const [sortBy, setSortBy] = useState("id")
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc")
  const [isLoading, setIsLoading] = useState(false)
  const [isSortOpen, setIsSortOpen] = useState(false)

  useEffect(() => {
    setIsLoading(false)
  }, [pathname])

  useEffect(() => {
    setSortBy("id")
  }, [searchType])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    const params: SimpleSearchParams = {}
    if (searchQuery) params.search = searchQuery
    if (sortBy) params.sort = sortBy
    if (sortOrder) params.order = sortOrder

    const searchParams = new URLSearchParams(params as Record<string, string>)
    router.push(`/search/${searchType}?${searchParams.toString()}`)
    setIsLoading(false)
  }

  return (
    <form onSubmit={handleSubmit} className="flex-1 flex gap-2">

      <Button
        type="button"
        variant="outline"
        size="icon"
        className="bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
        onClick={() => setIsSortOpen(true)}
      >
        <SlidersHorizontal className="h-4 w-4 text-white" />
      </Button>

      <div className="relative flex-1">
        <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-white/60" />
        <Input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search..."
          className="pl-9 bg-[#0F2942]/80 border-white/10 text-white placeholder:text-white/60"
        />
      </div>

      <Button type="submit" disabled={isLoading} className="bg-[#0F2942] hover:bg-[#1A3A5A] text-white">
        {/* {isLoading ? "Searching..." : "Search"} */}
        {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
      </Button>

      <Dialog open={isSortOpen} onOpenChange={setIsSortOpen}>
        <DialogContent className="bg-[#0F2942] text-white border-white/10">
          <DialogHeader>
            <DialogTitle>Sort Options</DialogTitle>
          </DialogHeader>

          <div className="space-y-6 pt-4">
            <div className="space-y-4">
              <Label>Sort By</Label>
              <RadioGroup value={sortBy} onValueChange={setSortBy}>
                {sortOptions[searchType].map((option) => (
                  <div key={option.value} className="flex items-center space-x-2">
                    <RadioGroupItem value={option.value} id={option.value} />
                    <Label htmlFor={option.value}>{option.label}</Label>
                  </div>
                ))}
              </RadioGroup>

              <div className="mt-4">
                <Label>Order</Label>
                <RadioGroup
                  value={sortOrder}
                  onValueChange={(value: "asc" | "desc") => setSortOrder(value)}
                  className="mt-2"
                >
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="asc" id="asc" />
                    <Label htmlFor="asc">Ascending</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="desc" id="desc" />
                    <Label htmlFor="desc">Descending</Label>
                  </div>
                </RadioGroup>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </form>
  )
}