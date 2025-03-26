"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"
import { GenStaffCard } from "@/utils/genCard"

import { Staff_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

export default function StaffSearchResults() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const itemsPerPage = 24

  const currentPage = parseInt(searchParams.get("page") || "1")

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [totalPages, setTotalPages] = useState(0)
  const [staff, setStaff] = useState<Staff_Small[]>([])

  const [abortController, setAbortController] = useState<AbortController | null>(null)

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" })
    setStaff([])
    fetchStaff()
  }, [currentPage, searchParams])

  useEffect(() => {
    return () => {
      abortController?.abort()
    }
  }, [abortController])

  const fetchStaff = async () => {
    try {
      abortController?.abort()
      const newController = new AbortController()
      setAbortController(newController)

      setLoading(true)
      setError(null)
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.staff(params, newController.signal)
      if (response.count === 1) {
        router.push(`/s/${response.results[0].id.slice(1)}`);
        return;
      }
      setStaff(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      setError(`Failed to fetch staff: ${error as string}`)
    } finally {
      setLoading(false)
    }
  }

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/s?${params.toString()}`)
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

        {/* No staff found */}
        {!loading && !error && staff.length === 0 && (
          <motion.div
            key="notfound"
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-grow flex justify-center items-center">
            <NotFound message="No staff found" />
          </motion.div>
        )}

        {/* Staff Cards */}
        {staff.length > 0 && (
          <motion.div
            key={`staff-${currentPage}`}
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
            className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {staff.map((staff, index) => (
              <Link key={`card-${index}-${staff.id}`} href={`/s/${staff.id.slice(1)}`}>
                {GenStaffCard(staff)}
              </Link>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Keep the footer at the bottom of the page */}
      <div className="flex-grow"></div>

      {/* Pagination */}
      {staff.length > 0 && (
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