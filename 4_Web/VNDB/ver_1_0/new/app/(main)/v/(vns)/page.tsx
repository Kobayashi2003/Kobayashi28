"use client"

import { useEffect, useState } from "react"
import { Loader2 } from "lucide-react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { ImageCard } from "@/components/common/ImageCard"
import { LevelSelecter } from "@/components/common/LevelSelecter"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { VN_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

export default function VNSearchResults() {
  const searchParams = useSearchParams()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const itemsPerPage = 24

  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const [vns, setVNs] = useState<VN_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setVNs([])
    fetchVNs()
  }, [currentPage, sexualLevel, violenceLevel])

  const fetchVNs = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.vn("", params)

      response.results.forEach((vn) => {
        const sexual = vn.image?.sexual || 0
        const violence = vn.image?.violence || 0

        const sexualFilter = sexualLevel === "safe" ? sexual <= 0.5 : sexualLevel === "suggestive" ? sexual <= 1 : true
        const violenceFilter = violenceLevel === "tame" ? violence <= 0.5 : violenceLevel === "violent" ? violence <= 1 : true

        if (!(sexualFilter && violenceFilter)) {
          vn.image = undefined
        }
      })

      setVNs(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      console.error("Failed to fetch VNs:", error)
      setError("Failed to fetch VNs. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleSexualLevelChange = (value: string) => {
    setSexualLevel(value as "safe" | "suggestive" | "explicit")
  }

  const handleViolenceLevelChange = (value: string) => {
    setViolenceLevel(value as "tame" | "violent" | "brutal")
  }

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  return (
    <main className="container mx-auto p-4 pb-8">
      <div className="flex items-center justify-end mb-4">
        <div className="flex gap-4">
          {/* Sexual Level Selector */}
          <LevelSelecter
            levelOptions={[
              { key: "sexual-level-save", label: "Safe", value: "safe", activeColor: "text-[#88ccff]" },
              { key: "sexual-level-suggestive", label: "Suggestive", value: "suggestive", activeColor: "text-[#ffcc66]" },
              { key: "sexual-level-explicit", label: "Explicit", value: "explicit", activeColor: "text-[#ff6666]" },
            ]}
            selectedValue={sexualLevel}
            onChange={handleSexualLevelChange}
          />
          {/* Divider */}
          <div className="h-8 w-px bg-gray-300 dark:bg-gray-700"></div>
          {/* Violence Level Selector */}
          <LevelSelecter
            levelOptions={[
              { key: "violence-level-tame", label: "Tame", value: "tame", activeColor: "text-[#88ccff]" },
              { key: "violence-level-violent", label: "Violent", value: "violent", activeColor: "text-[#ffcc66]" },
              { key: "violence-level-brutal", label: "Brutal", value: "brutal", activeColor: "text-[#ff6666]" },
            ]}
            selectedValue={violenceLevel}
            onChange={handleViolenceLevelChange}
          />
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex justify-center items-center mt-8">
          <Loader2 className="w-10 h-10 animate-spin text-white" />
        </div>
      )}
      {/* Error */}
      {error && (
        <div className="flex justify-center items-center mt-8">
          <p className="text-red-500">Error: {error}</p>
        </div>
      )}
      {/* No vns found */}
      {!loading && !error && vns.length === 0 && (
        <div className="flex justify-center items-center mt-8">
          <p className="text-gray-500">No VNs found</p>
        </div>
      )}
      {/* VN Cards */}
      {vns.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {vns.map((vn) => (
            <Link key={vn.id} href={"#"}>
              {/* <ImageCard imageTitle={vn.title} imageUrl={vn.image?.url} imageDims={vn.image?.dims} /> */}
              <ImageCard imageTitle={vn.title} imageUrl={vn.image?.thumbnail} imageDims={vn.image?.thumbnail_dims} />
            </Link>
          ))}
        </div>
      )}

      {/* Pagination */}
      {vns.length > 0 && (
        <div className="flex justify-center mt-4">
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