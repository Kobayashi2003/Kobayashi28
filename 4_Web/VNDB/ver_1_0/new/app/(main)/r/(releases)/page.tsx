"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"
import { GenReleaseCard } from "@/utils/genCard"

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
      <AnimatePresence mode="wait">
        {/* Loading */}
        {loading && (
          <motion.div
            key="loading"
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-grow flex justify-center items-center">
            <Loading message="Loading..." />
          </motion.div>
        )}

        {/* Error */}
        {error && (
          <motion.div
            key="error"
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-grow flex justify-center items-center">
            <Error message="Error: {error}" />
          </motion.div>
        )}

        {/* No releases found */}
        {!loading && !error && releases.length === 0 && (
          <motion.div
            key="notfound"
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-grow flex justify-center items-center">
            <NotFound message="No releases found" />
          </motion.div>
        )}

        {/* Release Cards */}
        {releases.length > 0 && (
          <motion.div
            key={`releases-${currentPage}`}
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
            className="flex flex-col gap-2">
            {releases.map((release) => (
              <Link key={`card-${release.id}`} href={`/r/${release.id.slice(1)}`}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3, delay: 0.1 }}
                >
                  {GenReleaseCard(release)}
                </motion.div>
              </Link>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

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