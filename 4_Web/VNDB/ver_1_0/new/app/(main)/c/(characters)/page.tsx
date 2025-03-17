"use client"

import { useEffect, useState, useMemo } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { CardTypeSelecter } from "@/components/common/CardTypeSelecter"
import { LevelSelecter } from "@/components/common/LevelSelecter"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"
import { GenCharacterCard } from "@/utils/genCard"

import { Character_Small, VNDBQueryParams } from "@/lib/types"
import { api } from "@/lib/api"

export default function CharacterSearchResults() {
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
  const [characters, setCharacters] = useState<Character_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setCharacters([])
    fetchCharacters()
  }, [currentPage, filteredParams])

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/c?${params.toString()}`)
  }

  const fetchCharacters = async () => {
    try {
      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }
      const response = await api.small.character(params)
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
        <div className="flex flex-wrap justify-start gap-4">
          {/* Card Type Selector */}
          <CardTypeSelecter
            selected={cardType}
            onSelect={handleCardTypeChange}
          />
        </div>
        <div className="flex flex-wrap justify-end gap-4">
          {/* Sexual Level Selector */}
          <LevelSelecter
            levelOptions={[
              { key: "sexual-level-safe", label: "Safe", labelSmall: "🟢SA", value: "safe",
                activeColor: "text-[#88ccff]", defaultClassName: "hover:text-[#88ccff]/70" },
              { key: "sexual-level-suggestive", label: "Suggestive", labelSmall: "🟡SU", value: "suggestive",
                activeColor: "text-[#ffcc66]", defaultClassName: "hover:text-[#ffcc66]/70" },
              { key: "sexual-level-explicit", label: "Explicit", labelSmall: "🔴EX", value: "explicit",
                activeColor: "text-[#ff6666]", defaultClassName: "hover:text-[#ff6666]/70" },
            ]}
            selectedValue={sexualLevel}
            onChange={handleSexualLevelChange}
            className="font-serif italic"
          />
          {/* Divider */}
          <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block"></div>
          {/* Violence Level Selector */}
          <LevelSelecter
            levelOptions={[
              { key: "violence-level-tame", label: "Tame", labelSmall: "🟢TA", value: "tame",
                activeColor: "text-[#88ccff]", defaultClassName: "hover:text-[#88ccff]/70" },
              { key: "violence-level-violent", label: "Violent", labelSmall: "🟡VI", value: "violent",
                activeColor: "text-[#ffcc66]", defaultClassName: "hover:text-[#ffcc66]/70" },
              { key: "violence-level-brutal", label: "Brutal", labelSmall: "🔴BR", value: "brutal",
                activeColor: "text-[#ff6666]", defaultClassName: "hover:text-[#ff6666]/70" },
            ]}
            selectedValue={violenceLevel}
            onChange={handleViolenceLevelChange}
            className="font-serif italic"
          />
        </div>
      </div>

      <AnimatePresence mode="wait">
        {/* Loading */}
        {loading && (
          <motion.div
            key="loading"
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-grow flex justify-center items-center"
          >
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
            className="flex-grow flex justify-center items-center"
          >
            <Error message={`Error: ${error}`} />
          </motion.div>
        )}

        {/* No characters found */}
        {!loading && !error && characters.length === 0 && (
          <motion.div
            key="notfound"
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-grow flex justify-center items-center"
          >
            <NotFound message="No characters found" />
          </motion.div>
        )}

        {/* Character Cards */}
        {characters.length > 0 && (
          <motion.div
            key={`characters-${currentPage}-${cardType}`}
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
            className={cardType === "image" ?
              `grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4` :
              `grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4`
            }>
            {characters.map((character) => (
              <Link key={`card-${character.id}`} href={`/c/${character.id.slice(1, -1)}`}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3, delay: 0.1 }}
                >
                  {GenCharacterCard(character, sexualLevel, violenceLevel, cardType)}
                </motion.div>
              </Link>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

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