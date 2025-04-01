"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import { useUrlParams } from "@/hooks/useUrlParams"
import { motion, AnimatePresence } from "motion/react"

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

import { SexualLevelSelector } from "@/components/selector/SexualLevelSelector"
import { ViolenceLevelSelector } from "@/components/selector/ViolenceLevelSelector"
import { CardTypeSwitch } from "@/components/selector/CardTypeSwtich"
import { PaginationButtons } from "@/components/button/PaginationButtons"

import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"

import { VNsCardsGrid } from "@/components/card/CardsGrid"

import { VN_Small } from "@/lib/types"
import { api } from "@/lib/api"

export default function Home() {
  const searchParams = useSearchParams()
  const { updateKey, updateMultipleKeys } = useUrlParams()

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

  const [vnsState, setVnsState] = useState({
    loading: false,
    error: null as string | null,
    notFound: false
  })

  const [totalPages, setTotalPages] = useState(0)
  const [vns, setVNs] = useState<VN_Small[]>([])

  const [cardType, setCardType] = useState<"image" | "text">("image")
  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const [abortController, setAbortController] = useState<AbortController | null>(null)

  const fetchVNs = async () => {
    try {
      abortController?.abort()
      const newController = new AbortController()
      setAbortController(newController)

      setVnsState({
        loading: true,
        error: null,
        notFound: false
      })

      let released = ""
      if (selectedYear === "00") {
        released = ""
      } else if (selectedYear !== "00" && selectedMonth === "00") {
        const startYearStr1 = `${selectedYear}-01-01`
        const endYearStr1 = `${selectedYear}-12-31`

        const startYearStr2 = `${selectedYear}`
        const endYearStr2 = `${String(Number.parseInt(selectedYear) + 1)}`

        released = `(>=${startYearStr1}+<=${endYearStr1}),(>=${startYearStr2}+<${endYearStr2})`
      } else if (selectedYear !== "00" && selectedMonth !== "00") {
        const startDateStr1 = `${selectedYear}-${selectedMonth}-01`
        const startDateStr2 = `${selectedYear}-${selectedMonth}-01`

        const lastDay = new Date(Number.parseInt(selectedYear), Number.parseInt(selectedMonth), 0).getDate()
        const endDateStr1 = `${selectedYear}-${selectedMonth}-${lastDay}`

        const nextMonth = Number.parseInt(selectedMonth) === 12 ? "01" : String(Number.parseInt(selectedMonth) + 1).padStart(2, "0")
        const nextMonthYear = Number.parseInt(selectedMonth) === 12 ? String(Number.parseInt(selectedYear) + 1) : selectedYear
        const endDateStr2 = `${nextMonthYear}-${nextMonth}-01`

        released = `(>=${startDateStr1}+<=${endDateStr1}),(>=${startDateStr2}+<${endDateStr2})`
      }

      const response = await api.small.vn({
        released: released,
        olang: "ja",
        sort: "released",
        reverse: true,
        page: currentPage,
        limit: itemsPerPage,
      }, newController.signal)

      setVNs(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
      if (response.results.length === 0) {
        setVnsState({
          loading: false,
          error: null,
          notFound: true
        })
      } else {
        setVnsState({
          loading: false,
          error: null,
          notFound: false
        })
      }
    } catch (error) {
      setVnsState({
        loading: false,
        error: "Failed to fetch VNs. Please try again.",
        notFound: false
      })
    }
  }

  const handleYearChange = (value: string) => {
    updateMultipleKeys({ year: value, page: "1" })
  }

  const handleMonthChange = (value: string) => {
    updateMultipleKeys({ month: value, page: "1" })
  }

  const handlePageChange = (page: number) => {
    updateKey("page", page.toString())
  }

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

  const fadeInAnimation = {
    initial: { filter: "blur(20px)", opacity: 0 },
    animate: { filter: "blur(0px)", opacity: 1 },
    exit: { filter: "blur(20px)", opacity: 0 },
    transition: { duration: 0.4, ease: "easeInOut" }
  }
  const statusStyle = "flex-grow flex justify-center items-center"

  return (
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">
      <div className="overflow-x-auto flex flex-col sm:flex-row items-end sm:items-center justify-center sm:justify-between mb-4 gap-4">
        <div className="flex flex-wrap justify-end sm:justify-start gap-2">
          {/* Card Type Selector */}
          <CardTypeSwitch
            cardType={cardType}
            setCardType={setCardType}
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
          <SexualLevelSelector
            sexualLevel={sexualLevel}
            setSexualLevel={(value: string) => setSexualLevel(value as "safe" | "suggestive" | "explicit")}
          />
          {/* Divider */}
          <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block" />
          {/* Violence Level Selector */}
          <ViolenceLevelSelector
            violenceLevel={violenceLevel}
            setViolenceLevel={(value: string) => setViolenceLevel(value as "tame" | "violent" | "brutal")}
          />
        </div>
      </div>
      <AnimatePresence mode="wait">
        {/* Loading */}
        {vnsState.loading && (
          <motion.div
            key="loading"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <Loading message="Loading..." />
          </motion.div>
        )}
        {/* Error */}
        {vnsState.error && (
          <motion.div
            key="error"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <Error message={`Error: ${vnsState.error}`} />
          </motion.div>
        )}
        {/* Not Found */}
        {vnsState.notFound && (
          <motion.div
            key="notfound"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <NotFound message="No VNs found" />
          </motion.div>
        )}
        {/* VN Cards */}
        {!vnsState.loading && !vnsState.error && !vnsState.notFound && (
          <VNsCardsGrid
            vns={vns}
            cardType={cardType}
            sexualLevel={sexualLevel}
            violenceLevel={violenceLevel}
          />
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