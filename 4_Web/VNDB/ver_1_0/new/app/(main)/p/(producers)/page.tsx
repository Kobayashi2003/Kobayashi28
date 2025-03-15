"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { TextCard } from "@/components/common/TextCard"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"
import { Producer_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

export default function ProducerSearchResults() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const currentPage = parseInt(searchParams.get("page") || "1")

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [totalPages, setTotalPages] = useState(0)
  const itemsPerPage = 24

  const [producers, setProducers] = useState<Producer_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setProducers([])
    fetchProducers()
  }, [currentPage, searchParams])

  const fetchProducers = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.producer(params)
      setProducers(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      console.error("Failed to fetch producers:", error)
      setError("Failed to fetch producers. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/p?${params.toString()}`)
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
      {/* No producers found */}
      {!loading && !error && producers.length === 0 && (
        <div className="flex-grow flex justify-center items-center">
          <NotFound message="No producers found" />
        </div>
      )}
      {/* Producer Cards */}
      {producers.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {producers.map((producer) => (
            <Link key={`card-${producer.id}`} href={`/p/${producer.id.slice(1, -1)}`}>
              <TextCard title={producer.name} />
            </Link>
          ))}
        </div>
      )}

      {/* Keep the footer at the bottom of the page */}
      <div className="flex-grow"></div>

      {/* Pagination */}
      {producers.length > 0 && (
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