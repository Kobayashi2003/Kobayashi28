"use client"

import { useState, useEffect } from "react"
import { useRouter, usePathname } from "next/navigation"
import { Settings2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

import { SearchFilters } from "./search-filters"
import { SortOptions } from "./sort-options"
import type { SearchType } from "@/lib/types"

interface AdvancedSearchProps {
  searchType: SearchType
}

export function AdvancedSearch({ searchType }: AdvancedSearchProps) {
  const router = useRouter()
  const pathname = usePathname()
  const [isOpen, setIsOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [params, setParams] = useState<Record<string, string>>({})
  const [sortBy, setSortBy] = useState("id")
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc")

  useEffect(() => {
    setIsLoading(false)
  }, [pathname])

  useEffect(() => {
    setSortBy("id")
  }, [searchType])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsOpen(false)
    setIsLoading(true)

    const searchParams = new URLSearchParams({
      ...params,
      sort: sortBy,
      order: sortOrder,
    } as Record<string, string>)

    router.push(`/search/${searchType}?${searchParams.toString()}`)
    setIsLoading(false)
  }

  return (
    <>
      <Button
        type="button"
        variant="outline"
        className="bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20 text-white"
        onClick={() => setIsOpen(true)}
      >
        <Settings2 className="h-4 w-4"/>
      </Button>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="bg-[#0A1929] text-white border-white/10 max-w-2xl max-h-[80vh]">
          <DialogHeader>
            <DialogTitle className="text-xl">Advanced Search</DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="flex flex-col h-full">
            <Tabs defaultValue="filters" className="flex-1">

              <TabsList className="w-full grid grid-cols-2 bg-[#0F2942]/50 p-1 rounded-lg">
                <TabsTrigger value="filters" className="data-[state=active]:bg-[#0F2942] rounded-md transition-colors">
                  Filters
                </TabsTrigger>
                <TabsTrigger value="sort" className="data-[state=active]:bg-[#0F2942] rounded-md transition-colors">
                  Sort
                </TabsTrigger>
              </TabsList>

              <TabsContent value="filters" className="mt-4 flex-1">
                <ScrollArea className="h-[50vh] pr-4">
                  <SearchFilters searchType={searchType} onChange={setParams} />
                </ScrollArea>
              </TabsContent>

              <TabsContent value="sort" className="mt-4 flex-1">
                <ScrollArea className="h-[50vh] pr-4">
                  <SortOptions
                    searchType={searchType}
                    sortBy={sortBy}
                    sortOrder={sortOrder}
                    onSortByChange={setSortBy}
                    onSortOrderChange={setSortOrder}
                  />
                </ScrollArea>
              </TabsContent>

            </Tabs>

            <div className="mt-6 px-4">
              <Button type="submit" disabled={isLoading} className="w-full bg-[#0F2942] hover:bg-[#1A3A5A]">
                {isLoading ? "Searching..." : "Search"}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </>
  )
}