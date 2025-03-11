"use client"

import { useEffect, useState } from "react"
import { Loader2 } from "lucide-react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { TextCard } from "@/components/common/TextCard"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Trait_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

export default function TraitSearchResults() {
  const searchParams = useSearchParams()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const itemsPerPage = 24

  const [traits, setTraits] = useState<Trait_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setTraits([])
    fetchTraits()
  }, [currentPage])

  const fetchTraits = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.trait("", params)
      setTraits(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      console.error("Failed to fetch traits:", error)
      setError("Failed to fetch traits. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  return (
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">      
      {/* Loading */}
      {loading && (
        <div className="flex-grow flex justify-center items-center">
          <Loader2 className="w-10 h-10 animate-spin text-white" />
        </div>
      )}
      {/* Error */}
      {error && (
        <div className="flex-grow flex justify-center items-center">
          <p className="text-red-500">Error: {error}</p>
        </div>
      )}
      {/* No traits found */}
      {!loading && !error && traits.length === 0 && (
        <div className="flex-grow flex justify-center items-center">
          <p className="text-gray-500">No traits found</p>
        </div>
      )}
      {/* Trait Cards */}
      {traits.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {traits.map((trait) => (
            <Link key={trait.id} href={"#"}>
              <TextCard title={trait.group_name ? `${trait.group_name} - ${trait.name}` : trait.name} className="h-full" />
            </Link>
          ))}
        </div>
      )}

      {/* Keep the footer at the bottom of the page */}
      <div className="flex-grow"></div>

      {/* Pagination */}
      {traits.length > 0 && (
        <div className="flex justify-center items-center mt-4">
          <PaginationButtons
            totalPages={totalPages}
            currentPage={currentPage}
            onPageChange={handlePageChange}
          />
        </div>
      )}
    </main>
  )
}