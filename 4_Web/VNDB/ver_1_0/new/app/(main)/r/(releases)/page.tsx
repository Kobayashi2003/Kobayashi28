"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { TextCard } from "@/components/common/TextCard"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"
import { Release_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

export default function ReleaseSearchResults() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const itemsPerPage = 24

  const currentPage = parseInt(searchParams.get("page") || "1")

  const [releases, setReleases] = useState<Release_Small[]>([])
  const [totalPages, setTotalPages] = useState(0)

  useEffect(() => {
    setLoading(true)
    setError(null)
    setReleases([])
    fetchReleases()
  }, [currentPage, searchParams])

  const fetchReleases = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.release(params)
      setReleases(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      console.error("Failed to fetch releases:", error)
      setError("Failed to fetch releases. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/r?${params.toString()}`)
  }

  const handlePageChange = (page: number) => {
    updateSearchParams("page", page.toString())
  }

  return (
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">
      {/* Loading */}
      {loading && (
        <div className="flex-grow flex justify-center items-center">
          <Loading message="Loading..." />
        </div>
      )}
      {/* Error */}
      {error && (
        <div className="flex-grow flex justify-center items-center">
          <Error message="Error: {error}" />
        </div>
      )}
      {/* No releases found */}
      {!loading && !error && releases.length === 0 && (
        <div className="flex-grow flex justify-center items-center">
          <NotFound message="No releases found" />
        </div>
      )}
      {/* Release Cards */}
      {releases.length > 0 && (
        <div className="flex flex-col gap-2">
          {releases.map((release) => (
            <Link key={`card-${release.id}`} href={`/r/${release.id.slice(1, -1)}`}>
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