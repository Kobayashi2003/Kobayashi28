"use client"

import { useEffect, useState } from "react"
import { Loader2 } from "lucide-react"
import Link from "next/link"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ImageCard } from "@/components/common/ImageCard"
import { LevelSelecter } from "@/components/common/LevelSelecter"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { VN_Small } from "@/lib/types"
import { api } from "@/lib/api"

export default function Home() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [selectedYear, setSelectedYear] = useState(() => {
    const now = new Date()
    return `${now.getFullYear().toString()}`
  })
  const [selectedMonth, setSelectedMonth] = useState(() => {
    const now = new Date()
    return `${(now.getMonth() + 1).toString().padStart(2, '0')}`
  })

  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const itemsPerPage = 24

  const currentYear = new Date().getFullYear()
  const yearsSelectable = Array.from({ length: 37 }, (_, i) => ({
    value: (currentYear - 35 + i).toString(),
    label: (currentYear - 35 + i).toString()
  }))
  const monthsSelectable = [
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
    // { value: "01", label: "January" },
    // { value: "02", label: "February" }, 
    // { value: "03", label: "March" },
    // { value: "04", label: "April" },
    // { value: "05", label: "May" },
    // { value: "06", label: "June" },
    // { value: "07", label: "July" },
    // { value: "08", label: "August" },
    // { value: "09", label: "September" },
    // { value: "10", label: "October" },
    // { value: "11", label: "November" },
    // { value: "12", label: "December" }
  ]

  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const [vns, setVNs] = useState<VN_Small[]>([])

  useEffect(() => {
    setLoading(true)
    setError(null)
    setVNs([])
    fetchVNs()
  }, [selectedYear, selectedMonth, currentPage, sexualLevel, violenceLevel])

  const fetchVNs = async () => {
    try {
      const startDateStr1 = `${selectedYear}-${selectedMonth}-01`
      const startDateStr2 = `${selectedYear}-${selectedMonth}-01`

      const lastDay = new Date(Number.parseInt(selectedYear), Number.parseInt(selectedMonth), 0).getDate()
      const endDateStr1 = `${selectedYear}-${selectedMonth}-${lastDay}`

      const nextMonth = Number.parseInt(selectedMonth) === 12 ? "01" : String(Number.parseInt(selectedMonth) + 1).padStart(2, "0")
      const nextMonthYear = Number.parseInt(selectedMonth) === 12 ? String(Number.parseInt(selectedYear) + 1) : selectedYear
      const endDateStr2 = `${nextMonthYear}-${nextMonth}-01`

      const response = await api.small.vn("", {
        released: `(>=${startDateStr1}+<=${endDateStr1}),(>=${startDateStr2}+<${endDateStr2})`,
        olang: "ja",
        sort: "released",
        reverse: true,
        page: currentPage,
        limit: itemsPerPage,
      })

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

  const handleYearChange = (value: string) => {
    setSelectedYear(value)
    setCurrentPage(1)
  }

  const handleMonthChange = (value: string) => {
    setSelectedMonth(value)
    setCurrentPage(1)
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
      {/* Filters */}
      <div className="flex overflow-x-auto items-center justify-between mb-4 gap-4">
        <div className="flex flex-wrap justify-start gap-2">
          {/* Year Selector */}
          <Select value={selectedYear} onValueChange={(value) => handleYearChange(value)}>
            <SelectTrigger className="bg-[#0F2942]/80 border-white/10 text-white font-bold">
              <SelectValue placeholder="Year" />
            </SelectTrigger>
            <SelectContent className="bg-[#0F2942]/80 border-white/10 text-white font-bold">
              {yearsSelectable.map((year) => (
                <SelectItem key={year.value} value={year.value}>{year.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          {/* Month Selector */}
          <Select value={selectedMonth} onValueChange={(value) => handleMonthChange(value)}>
            <SelectTrigger className="bg-[#0F2942]/80 border-white/10 text-white font-bold">
              <SelectValue placeholder="Month" />
            </SelectTrigger>
            <SelectContent className="bg-[#0F2942]/80 border-white/10 text-white font-bold">
              {monthsSelectable.map((month) => (
                <SelectItem key={month.value} value={month.value}>{month.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="flex flex-wrap justify-end gap-2">
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
          <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block"></div>
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
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
          {vns.map((vn) => (
            <Link key={vn.id} href={"#"}>
              <ImageCard imageTitle={vn.title} imageUrl={vn.image?.thumbnail} imageDims={vn.image?.thumbnail_dims} />
            </Link>
          ))}
        </div>
      )}

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