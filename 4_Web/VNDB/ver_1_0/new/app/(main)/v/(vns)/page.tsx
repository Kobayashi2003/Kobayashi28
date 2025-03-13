"use client"

import { useEffect, useState } from "react"
import { Loader2 } from "lucide-react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { TextCard } from "@/components/common/TextCard"
import { ImageCard } from "@/components/common/ImageCard"
import { CardTypeSelecter } from "@/components/common/CardTypeSelecter"
import { LevelSelecter } from "@/components/common/LevelSelecter"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { VN_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

function GenVNCard(vn: VN_Small, sexualLevel: "safe" | "suggestive" | "explicit", violenceLevel: "tame" | "violent" | "brutal", cardType: "image" | "text") {
  if (cardType === "text") {
    return <TextCard title={vn.title} />
  }
  const sexual = vn.image?.sexual || 0
  const violence = vn.image?.violence || 0
  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor="text-yellow-400" />
    }
    return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor="text-red-400" />
  } 
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor="text-red-400" />
  }
  return <ImageCard imageTitle={vn.title} imageUrl={vn.image?.thumbnail || vn.image?.url} imageDims={vn.image?.thumbnail_dims || vn.image?.dims} />
}

export default function VNSearchResults() {
  const searchParams = useSearchParams()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [cardType, setCardType] = useState<"image" | "text">("image")

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
  }, [currentPage, searchParams])

  const fetchVNs = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.vn(params)

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
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">
      <div className="flex flex-wrap overflow-x-auto items-center justify-between mb-4">
        {/* Card Type Selector */}
        <div className="flex flex-wrap justify-start gap-4">
          <CardTypeSelecter
            selected={cardType}
            onSelect={setCardType}
          />
        </div>
        <div className="flex flex-wrap justify-end gap-4">
          {/* Sexual Level Selector */}
          <LevelSelecter
            levelOptions={[
              { key: "sexual-level-save", label: "Safe", labelSmall: "🟢SA", value: "safe", activeColor: "text-[#88ccff]" },
              { key: "sexual-level-suggestive", label: "Suggestive", labelSmall: "🟡SU", value: "suggestive", activeColor: "text-[#ffcc66]" },
              { key: "sexual-level-explicit", label: "Explicit", labelSmall: "🔴EX", value: "explicit", activeColor: "text-[#ff6666]" },
            ]}
            selectedValue={sexualLevel}
            onChange={handleSexualLevelChange}
          />
          {/* Divider */}
          <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block"></div>
          {/* Violence Level Selector */}
          <LevelSelecter
            levelOptions={[
              { key: "violence-level-tame", label: "Tame", labelSmall: "🟢TA", value: "tame", activeColor: "text-[#88ccff]" },
              { key: "violence-level-violent", label: "Violent", labelSmall: "🟡VI", value: "violent", activeColor: "text-[#ffcc66]" },
              { key: "violence-level-brutal", label: "Brutal", labelSmall: "🔴BR", value: "brutal", activeColor: "text-[#ff6666]" },
            ]}
            selectedValue={violenceLevel}
            onChange={handleViolenceLevelChange}
          />
        </div>
      </div>

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
      {/* No vns found */}
      {!loading && !error && vns.length === 0 && (
        <div className="flex-grow flex justify-center items-center">
          <p className="text-gray-500">No VNs found</p>
        </div>
      )}
      {/* VN Cards */}
      {vns.length > 0 && (
        <div className={ cardType === "image" ?
          `grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4` :
          `grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4`
        }>
          {vns.map((vn) => (
            <Link key={vn.id} href={`/v/${vn.id.slice(1, -1)}`}>
              {GenVNCard(vn, sexualLevel, violenceLevel, cardType)}
            </Link>
          ))}
        </div>
      )}

      {/* Keep the footer at the bottom of the page */}
      <div className="flex-grow"></div>

      {/* Pagination */}
      {vns.length > 0 && (
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