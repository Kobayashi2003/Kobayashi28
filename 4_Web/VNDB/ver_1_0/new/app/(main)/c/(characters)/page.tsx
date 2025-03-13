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
import { Character_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

function GenCharacterCard(character: Character_Small, sexualLevel: "safe" | "suggestive" | "explicit", violenceLevel: "tame" | "violent" | "brutal", cardType: "image" | "text") {
  if (cardType === "text") {
    return <TextCard title={character.name} className="h-full" />
  }
  const sexual = character.image?.sexual || 0
  const violence = character.image?.violence || 0
  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor="text-yellow-400" />
    }
    return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor="text-red-400" />
  } 
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor="text-red-400" />
  }
  return <ImageCard imageTitle={character.name} imageUrl={character.image?.url} imageDims={character.image?.dims} />
}

export default function CharacterSearchResults() {
  const searchParams = useSearchParams()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [cardType, setCardType] = useState<"image" | "text">("image")

  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const itemsPerPage = 24

  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const [characters, setCharacters] = useState<Character_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setCharacters([])
    fetchCharacters()
  }, [currentPage, searchParams])

  const fetchCharacters = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.character(params)

      response.results.forEach((character) => {
        const sexual = character.image?.sexual || 0
        const violence = character.image?.violence || 0

        const sexualFilter = sexualLevel === "safe" ? sexual <= 0.5 : sexualLevel === "suggestive" ? sexual <= 1 : true
        const violenceFilter = violenceLevel === "tame" ? violence <= 0.5 : violenceLevel === "violent" ? violence <= 1 : true

        if (!(sexualFilter && violenceFilter)) {
          character.image = undefined
        }
      })

      setCharacters(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      console.error("Failed to fetch characters:", error)
      setError("Failed to fetch characters. Please try again.")
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
        <div className="flex flex-wrap justify-start gap-4">
          {/* Card Type Selector */}
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
      {/* No characters found */}
      {!loading && !error && characters.length === 0 && (
        <div className="flex-grow flex justify-center items-center">
          <p className="text-gray-500">No characters found</p>
        </div>
      )}
      {/* Character Cards */}
      {characters.length > 0 && (
        <div className={ cardType === "image" ?
          `grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4` :
          `grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4`
        }>
          {characters.map((character) => (
            <Link key={character.id} href={`/c/${character.id.slice(1, -1)}`}>
              {GenCharacterCard(character, sexualLevel, violenceLevel, cardType)}
            </Link>
          ))}
        </div>
      )}

      {/* Keep the footer at the bottom of the page */}
      <div className="flex-grow"></div>

      {/* Pagination */}
      {characters.length > 0 && (
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