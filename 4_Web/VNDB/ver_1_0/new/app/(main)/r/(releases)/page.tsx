"use client"

import { useEffect, useState } from "react"
import { Loader2 } from "lucide-react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { TextCard } from "@/components/common/TextCard"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Release_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

export default function ReleaseSearchResults() {
  const searchParams = useSearchParams()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const itemsPerPage = 24

  const [releases, setReleases] = useState<Release_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setReleases([])
    fetchReleases()
  }, [currentPage])

  const fetchReleases = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.release("", params)
      setReleases(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      console.error("Failed to fetch releases:", error)
      setError("Failed to fetch releases. Please try again.")
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
      {/* No releases found */}
      {!loading && !error && releases.length === 0 && (
        <div className="flex-grow flex justify-center items-center">
          <p className="text-gray-500">No releases found</p>
        </div>
      )}
      {/* Release Cards */}
      {releases.length > 0 && (
        <div className="flex flex-col gap-2">
          {releases.map((release) => (
            <Link key={release.id} href={"#"}>
              <TextCard title={release.title} />
            </Link>
          ))}
        </div>
      )}

      {/* Keep the footer at the bottom of the page */}
      <div className="flex-grow"></div>

      {/* Pagination */}
      {releases.length > 0 && (
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