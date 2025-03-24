"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { CardTypeSelecter } from "@/components/common/CardTypeSelecter"
import { LevelSelecter } from "@/components/common/LevelSelecter"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"
import { ImageCard } from "@/components/common/ImageCard"
import { TextCard } from "@/components/common/TextCard"

import { VN_Small } from "@/lib/types"
import { api } from "@/lib/api"

export function GenVNCard(vn: VN_Small, sexualLevel: "safe" | "suggestive" | "explicit", violenceLevel: "tame" | "violent" | "brutal", cardType: "image" | "text") {
  if (cardType === "text") {
    return <TextCard title={vn.title} subTitle={`Release Date: ${vn.released}`} />
  }
  const sexual = vn.image?.sexual || 0
  const violence = vn.image?.violence || 0
  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      const yellow = sexual > 1 && violence > 1 ? `text-yellow-800` : `text-yellow-400`
      return <ImageCard imageTitle={vn.title} imageSubtitle={`Release Date: ${vn.released}`} imageUrl={""} imageDims={[0, 0]} textColor={yellow} />
    }
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={vn.title} imageSubtitle={`Release Date: ${vn.released}`} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={vn.title} imageSubtitle={`Release Date: ${vn.released}`} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  return <ImageCard imageTitle={vn.title} imageSubtitle={`Release Date: ${vn.released}`} imageUrl={vn.image?.thumbnail || vn.image?.url} imageDims={vn.image?.thumbnail_dims || vn.image?.dims} />
}

export default function Home() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const itemsPerPage = 24

  const currentYear = new Date().getFullYear()
  const yearsSelectable = [
    { value: "00", label: "ALL" },
    ...Array.from({ length: 37 }, (_, i) => ({
      value: (currentYear - 35 + i).toString(),
      label: (currentYear - 35 + i).toString()
    }))
  ]
  const monthsSelectable = [
    { value: "00", label: "ALL" },
    { value: "01", label: "JAN" },
    { value: "02", label: "FEB" },
    { value: "03", label: "MAR" },
    { value: "04", label: "APR" },
    { value: "05", label: "MAY" },
    { value: "06", label: "JUN" },
    { value: "07", label: "JUL" },
    { value: "08", label: "AUG" },
    { value: "09", label: "SEP" },
    { value: "10", label: "OCT" },
    { value: "11", label: "NOV" },
    { value: "12", label: "DEC" }
  ]

  const currentPage = searchParams.get("page") ? Number.parseInt(searchParams.get("page") as string) : 1
  const selectedYear = searchParams.get("year") || `${new Date().getFullYear().toString()}`
  const selectedMonth = searchParams.get("month") || `${(new Date().getMonth() + 1).toString().padStart(2, '0')}`

  const cardType = searchParams.get("card") as "image" | "text" || "image"
  const sexualLevel = searchParams.get("sexual") as "safe" | "suggestive" | "explicit" || "safe"
  const violenceLevel = searchParams.get("violence") as "tame" | "violent" | "brutal" || "tame"

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [totalPages, setTotalPages] = useState(0)
  const [vns, setVNs] = useState<VN_Small[]>([])

  const [abortController, setAbortController] = useState<AbortController | null>(null)

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" })
    setVNs([])
    fetchVNs()
  }, [selectedYear, selectedMonth, currentPage])

  useEffect(() => {
    return () => {
      abortController?.abort()
    }
  }, [abortController])

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/?${params.toString()}`)
  }

  const updateMultipleSearchParams = (params: Record<string, string>) => {
    const newParams = new URLSearchParams(searchParams)
    Object.entries(params).forEach(([key, value]) => {
      newParams.set(key, value)
    })
    router.push(`/?${newParams.toString()}`)
  }

  const fetchVNs = async () => {
    try {
      abortController?.abort()
      const newController = new AbortController()
      setAbortController(newController)

      setLoading(true)
      setError(null)
      if (selectedYear === "00") {
        const response = await api.small.vn({
          olang: "ja",
          sort: "released",
          reverse: true,
          page: currentPage,
          limit: itemsPerPage,
        }, newController.signal)
        setVNs(response.results)
        setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
      } else if (selectedYear !== "00" && selectedMonth === "00") {
        const startYearStr1 = `${selectedYear}-01-01`
        const endYearStr1 = `${selectedYear}-12-31`

        const startYearStr2 = `${selectedYear}`
        const endYearStr2 = `${String(Number.parseInt(selectedYear) + 1)}`

        const response = await api.small.vn({
          released: `(>=${startYearStr1}+<=${endYearStr1}),(>=${startYearStr2}+<${endYearStr2})`,
          olang: "ja",
          sort: "released",
          reverse: true,
          page: currentPage,
          limit: itemsPerPage,
        }, newController.signal)
        setVNs(response.results)
        setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
      } else if (selectedYear !== "00" && selectedMonth !== "00") {
        const startDateStr1 = `${selectedYear}-${selectedMonth}-01`
        const startDateStr2 = `${selectedYear}-${selectedMonth}-01`

        const lastDay = new Date(Number.parseInt(selectedYear), Number.parseInt(selectedMonth), 0).getDate()
        const endDateStr1 = `${selectedYear}-${selectedMonth}-${lastDay}`

        const nextMonth = Number.parseInt(selectedMonth) === 12 ? "01" : String(Number.parseInt(selectedMonth) + 1).padStart(2, "0")
        const nextMonthYear = Number.parseInt(selectedMonth) === 12 ? String(Number.parseInt(selectedYear) + 1) : selectedYear
        const endDateStr2 = `${nextMonthYear}-${nextMonth}-01`

        const response = await api.small.vn({
          released: `(>=${startDateStr1}+<=${endDateStr1}),(>=${startDateStr2}+<${endDateStr2})`,
          olang: "ja",
          sort: "released",
          reverse: true,
          page: currentPage,
          limit: itemsPerPage,
        }, newController.signal)
        setVNs(response.results)
        setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
      }
    } catch (error) {
      console.error("Failed to fetch VNs:", error)
      setError("Failed to fetch VNs. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleYearChange = (value: string) => {
    updateMultipleSearchParams({ year: value, page: "1" })
  }

  const handleMonthChange = (value: string) => {
    updateMultipleSearchParams({ month: value, page: "1" })
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
      <div className="overflow-x-auto flex flex-col sm:flex-row items-end sm:items-center justify-center sm:justify-between mb-4 gap-4">
        <div className="flex flex-wrap justify-end sm:justify-start gap-2">
          {/* Card Type Selector */}
          <CardTypeSelecter
            selected={cardType}
            onSelect={handleCardTypeChange}
          />
          <div className="flex flex-wrap justify-start gap-2">
            {/* Year Selector */}
            <Select value={selectedYear} onValueChange={handleYearChange}>
              <SelectTrigger className="bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white font-bold">
                <SelectValue placeholder="Year" />
              </SelectTrigger>
              <SelectContent className="bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white font-bold">
                {yearsSelectable.map((year) => (
                  <SelectItem key={year.value} value={year.value}>{year.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            {/* Month Selector */}
            <Select value={selectedMonth} onValueChange={handleMonthChange}>
              <SelectTrigger className={`bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white font-bold ${selectedYear === "00" ? "hidden" : ""}`}>
                <SelectValue placeholder="Month" />
              </SelectTrigger>
              <SelectContent className={`bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white font-bold ${selectedYear === "00" ? "hidden" : ""}`}>
                {monthsSelectable.map((month) => (
                  <SelectItem key={month.value} value={month.value}>{month.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="flex flex-wrap justify-end gap-2">
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

        {/* Not Found */}
        {!loading && !error && vns.length === 0 && (
          <motion.div
            key="notfound"
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-grow flex justify-center items-center"
          >
            <NotFound message="No VNs found" />
          </motion.div>
        )}

        {/* VN Cards */}
        {vns.length > 0 && (
          <motion.div
            key={`cards-${currentPage}-${cardType}-${selectedYear}-${selectedMonth}`}
            initial={{ filter: "blur(20px)", opacity: 0 }}
            animate={{ filter: "blur(0px)", opacity: 1 }}
            exit={{ filter: "blur(20px)", opacity: 0 }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
            className={cardType === "image" ?
              "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4" :
              "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
            }
          >
            {vns.map((vn) => (
              <Link key={`card-${vn.id}`} href={`/v/${vn.id.slice(1)}`}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3, delay: 0.1 }}
                >
                  {GenVNCard(vn, sexualLevel, violenceLevel, cardType)}
                </motion.div>
              </Link>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Keep the footer at the bottom of the page */}
      <div className="flex-grow"></div>

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