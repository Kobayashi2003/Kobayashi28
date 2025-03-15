"use client"

import { useEffect, useState, useMemo } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { TextCard } from "@/components/common/TextCard"
import { ImageCard } from "@/components/common/ImageCard"
import { CardTypeSelecter } from "@/components/common/CardTypeSelecter"
import { LevelSelecter } from "@/components/common/LevelSelecter"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"
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
      const yellow = sexual > 1 && violence > 1 ? `text-yellow-800` : `text-yellow-400`
      return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={yellow} />
    }
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  return <ImageCard imageTitle={vn.title} imageUrl={vn.image?.thumbnail || vn.image?.url} imageDims={vn.image?.thumbnail_dims || vn.image?.dims} />
}

export default function VNSearchResults() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const filteredParams = useMemo(() => {
    const params = new URLSearchParams(searchParams)
    params.delete("card")
    params.delete("sexual")
    params.delete("violence")
    return params.toString()
  }, [searchParams])

  const itemsPerPage = 24

  const currentPage = parseInt(searchParams.get("page") || "1")
  const cardType = searchParams.get("card") as "image" | "text" || "image"
  const sexualLevel = searchParams.get("sexual") as "safe" | "suggestive" | "explicit" || "safe"
  const violenceLevel = searchParams.get("violence") as "tame" | "violent" | "brutal" || "tame"

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [totalPages, setTotalPages] = useState(0)
  const [vns, setVNs] = useState<VN_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setVNs([])
    fetchVNs()
  }, [currentPage, filteredParams])

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/v?${params.toString()}`)
  }

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
    updateSearchParams("sexual", value)
  }

  const handleViolenceLevelChange = (value: string) => {
    updateSearchParams("violence", value)
  }

  const handlePageChange = (page: number) => {
    updateSearchParams("page", page.toString())
  }

  const handleCardTypeChange = (value: string) => {
    updateSearchParams("card", value)
  }

  return (
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">
      <div className="flex flex-wrap overflow-x-auto items-center justify-between mb-4">
        {/* Card Type Selector */}
        <div className="flex flex-wrap justify-start gap-4">
          <CardTypeSelecter
            selected={cardType}
            onSelect={handleCardTypeChange}
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
          <Loading message="Loading..." />
        </div>
      )}
      {/* Error */}
      {error && (
        <div className="flex-grow flex justify-center items-center">
          <Error message="Error: {error}" />
        </div>
      )}
      {/* No vns found */}
      {!loading && !error && vns.length === 0 && (
        <div className="flex-grow flex justify-center items-center">
          <NotFound message="No VNs found" />
        </div>
      )}
      {/* VN Cards */}
      {vns.length > 0 && (
        <div className={cardType === "image" ?
          `grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4` :
          `grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4`
        }>
          {vns.map((vn) => (
            <Link key={vn.id} href={`/v/${vn.id.slice(1)}`}>
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