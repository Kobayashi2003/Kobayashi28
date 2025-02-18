"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import Link from "next/link"
import { ChevronDown, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { api } from "@/lib/api"
import type { VN } from "@/lib/types"

export default function Home() {
  const [selectedDate, setSelectedDate] = useState(() => {
    const now = new Date()
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`
  })
  const [vns, setVns] = useState<VN[]>([])
  const [loading, setLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const [hasMore, setHasMore] = useState(false)
  const itemsPerPage = 20

  const currentYear = new Date().getFullYear()
  const years = Array.from({ length: 37 }, (_, i) => currentYear - 35 + i)

  // Generate month options
  const months = Array.from({ length: 12 }, (_, i) => ({
    value: String(i + 1).padStart(2, "0"),
    label: new Date(2000, i).toLocaleString("default", { month: "long" }),
  }))

  useEffect(() => {
    const fetchVNs = async () => {
      setLoading(true)
      try {
        const [year, month] = selectedDate.split("-")
        const startDateStr1 = `${year}-${month}-01`
        const startDateStr2 = `${year}-${month}-01`

        const lastDay = new Date(Number.parseInt(year), Number.parseInt(month), 0).getDate()
        const endDateStr1 = `${year}-${month}-${lastDay}`

        const nextMonth = Number.parseInt(month) === 12 ? "01" : String(Number.parseInt(month) + 1).padStart(2, "0")
        const nextMonthYear = Number.parseInt(month) === 12 ? String(Number.parseInt(year) + 1) : year
        const endDateStr2 = `${nextMonthYear}-${nextMonth}-01`

        const response = await api.vn("", {
          released: `(>=${startDateStr1}+<=${endDateStr1}),(>=${startDateStr2}+<${endDateStr2})`,
          // olang: "ja,zh,zh-Hans,zh-Hant",
          olang: "ja",
          size: "small",
          sort: "released",
          reverse: true,
          page: currentPage,
          limit: itemsPerPage,
        })

        setVns((prev) => (currentPage === 1 ? response.results : [...prev, ...response.results]))
        setHasMore(response.more ?? false)
      } catch (error) {
        console.error("Failed to fetch VNs:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchVNs()
  }, [selectedDate, currentPage])

  const handleDateChange = (value: string) => {
    setSelectedDate(value)
    setCurrentPage(1)
    setVns([])
  }

  return (
    <main className="container mx-auto p-4 pb-8">
      <div className="mb-8 flex flex-col gap-4">
        <h1 className="text-3xl font-bold text-white">Visual Novel Releases</h1>

        <div className="flex gap-4">
          <Select
            value={selectedDate.split("-")[0]}
            onValueChange={(year) => handleDateChange(`${year}-${selectedDate.split("-")[1]}`)}
          >
            <SelectTrigger className="w-[180px] bg-[#0F2942]/80 border-white/10 text-white font-bold ">
              <SelectValue placeholder="Select year" />
            </SelectTrigger>
            <SelectContent>
              {years.map((year) => (
                <SelectItem key={year} value={year.toString()}>
                  {year}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Select
            value={selectedDate.split("-")[1]}
            onValueChange={(month) => handleDateChange(`${selectedDate.split("-")[0]}-${month}`)}
          >
            <SelectTrigger className="w-[180px] bg-[#0F2942]/80 border-white/10 text-white font-bold">
              <SelectValue placeholder="Select month" />
            </SelectTrigger>
            <SelectContent>
              {months.map((month) => (
                <SelectItem key={month.value} value={month.value}>
                  {month.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        {vns.map((vn) => (
          <Link key={vn.id} href={`/${vn.id}`} className="group">
            <div className="bg-[#0F2942] rounded-lg overflow-hidden shadow-lg transition-all duration-300 ease-in-out group-hover:shadow-xl group-hover:scale-105">
              <div className="relative w-full" style={{ paddingBottom: "133.33%" }}>
                {vn.image?.url ? (
                  <Image
                    src={vn.image.url || "/placeholder.svg"}
                    alt={vn.title || "Visual Novel Cover"}
                    fill
                    style={{ objectFit: "cover" }}
                    className="transition-transform duration-300 ease-in-out group-hover:scale-110"
                  />
                ) : (
                  <div className="absolute inset-0 flex items-center justify-center bg-gray-200 text-gray-500">
                    No image
                  </div>
                )}
              </div>
              <div className="p-4 transition-colors duration-300 ease-in-out group-hover:bg-[#1A3A5A]">
                <h3 className="text-lg font-semibold text-white truncate">{vn.title}</h3>
                <p className="text-sm text-white/60">{vn.released}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {loading && (
        <div className="flex justify-center items-center mt-8">
          <Loader2 className="h-8 w-8 animate-spin text-white" />
        </div>
      )}

      {!loading && hasMore && (
        <div className="flex justify-center mt-8">
          <Button
            variant="outline"
            className="bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
            onClick={() => setCurrentPage((prev) => prev + 1)}
          >
            Load More
            <ChevronDown className="ml-2 h-4 w-4" />
          </Button>
        </div>
      )}
    </main>
  )
}