"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"
import { GenTraitCard } from "@/utils/genCard"

import { Trait_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

export default function TraitSearchResults() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const itemsPerPage = 24

  const currentPage = parseInt(searchParams.get("page") || "1")

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [totalPages, setTotalPages] = useState(0)

  const [traits, setTraits] = useState<Trait_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setTraits([])
    fetchTraits()
  }, [currentPage, searchParams])

  const fetchTraits = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.trait(params)
      setTraits(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      console.error("Failed to fetch traits:", error)
      setError("Failed to fetch traits. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/i?${params.toString()}`)
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
            <Error message={`Error: ${error}`} />
          </motion.div>
        )}

        {/* No traits found */}
        {!loading && !error && traits.length === 0 && (
          <motion.div
            key="notfound"
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-grow flex justify-center items-center">
            <NotFound message="No traits found" />
          </motion.div>
        )}

        {/* Trait Cards */}
        {traits.length > 0 && (
          <motion.div
            key={`traits-${currentPage}`}
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {traits.map((trait) => (
              <Link key={`card-${trait.id}`} href={`/i/${trait.id.slice(1)}`}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3, delay: 0.1 }}
                >
                  {GenTraitCard(trait)}
                </motion.div>
              </Link>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

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