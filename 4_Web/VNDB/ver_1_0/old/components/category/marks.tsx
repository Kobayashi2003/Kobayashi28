"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { api } from "@/lib/api"
import type { VN, Character, Producer, Staff, ResourceType } from "@/lib/types"
import Image from "next/image"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Loader2, ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react"

interface MarksProps {
  type: "v" | "c" | "p" | "s"
  categoryId: number
}

type MarkData = ResourceType & { marked_at: string }

function hasImage(mark: MarkData): mark is (VN | Character) & { marked_at: string } {
  return "image" in mark
}

function hasTitle(mark: MarkData): mark is VN & { marked_at: string } {
  return "title" in mark
}

function hasName(mark: MarkData): mark is (Character | Producer | Staff) & { marked_at: string } {
  return "name" in mark
}

export function Marks({ type, categoryId }: MarksProps) {
  const [marks, setMarks] = useState<(MarkData & { marked_at: string })[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [totalCount, setTotalCount] = useState(0)
  const [totalPages, setTotalPages] = useState(0)
  const searchParams = useSearchParams()
  const currentPage = Number(searchParams.get("page")) || 1
  const itemsPerPage = 20

  const fetchMarks = async (page: number) => {
    setLoading(true)
    setError(null)
    try {
      const marksResponse = await api.getMarks(type, categoryId, {
        page,
        limit: itemsPerPage,
        sort: "marked_at",
        reverse: true,
        count: true,
      })

      if (marksResponse.results.length === 0) {
        setMarks([])
        setTotalCount(0)
        setTotalPages(0)
        setLoading(false)
        return
      }

      const ids = marksResponse.results.map((mark) => mark.id).join(",")

      let detailedData
      switch (type) {
        case "v":
          detailedData = await api.vn("", { id: ids, page: page, size: "small" })
          break
        case "c":
          detailedData = await api.character("", { id: ids, page: page, size: "small" })
          break
        case "p":
          detailedData = await api.producer("", { id: ids, page: page, size: "small" })
          break
        case "s":
          detailedData = await api.staff("", { id: ids, page: page, size: "small" })
          break
        default:
          throw new Error("Unsupported type")
      }

      const combinedData = detailedData.results.map((item: ResourceType) => {
        const mark = marksResponse.results.find((m) => m.id === Number(item.id.slice(1)))
        return { ...item, marked_at: mark ? mark.marked_at : "" }
      })

      setMarks(combinedData)
      setTotalCount(marksResponse.count || 0)
      setTotalPages(Math.ceil((marksResponse.count || 0) / itemsPerPage))
    } catch (err) {
      setError("Failed to fetch marks")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMarks(currentPage)
  }, [currentPage, categoryId])

  if (error) {
    return <div className="text-red-500">{error}</div>
  }

  return (
    <div>
      <h2 className="text-xl font-semibold text-white mb-4">Marked Items ({totalCount})</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
        {marks.map((mark) => (
          <div key={mark.id} className="relative group">
            <Link href={`/${mark.id}`} className="block">
              <div className="bg-[#0F2942] rounded-lg overflow-hidden shadow-lg transition-all duration-300 ease-in-out group-hover:shadow-xl group-hover:scale-105">
                <div className="relative w-full h-0" style={{ paddingBottom: "133.33%" }}>
                  {hasImage(mark) && mark.image?.url ? (
                    <Image
                      src={mark.image.url || "/placeholder.svg"}
                      alt={hasTitle(mark) ? mark.title : hasName(mark) ? mark.name : ""}
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
                  <h3 className="text-lg font-semibold text-white truncate">
                    {hasTitle(mark) ? mark.title : hasName(mark) ? mark.name : "Untitled"}
                  </h3>
                  <p className="text-sm text-white/60">Marked: {new Date(mark.marked_at).toLocaleDateString()}</p>
                </div>
              </div>
            </Link>
          </div>
        ))}
      </div>
      {loading && (
        <div className="flex justify-center items-center mt-4">
          <Loader2 className="h-8 w-8 animate-spin text-white" />
        </div>
      )}
      {!loading && totalPages > 1 && <MarksPagination currentPage={currentPage} totalPages={totalPages} />}
    </div>
  )
}

function MarksPagination({ currentPage, totalPages }: { currentPage: number; totalPages: number }) {
  const renderPageNumbers = () => {
    const items: React.ReactNode[] = []
    const ellipsis = (key: string) => (
      <span key={key} className="px-2 text-white font-bold">
        ...
      </span>
    )

    const addPageButton = (pageNum: number) => {
      items.push(
        <PageButton key={pageNum} page={pageNum} isActive={currentPage === pageNum}>
          {pageNum}
        </PageButton>,
      )
    }

    addPageButton(1)

    let leftBound = Math.max(2, currentPage - 1)
    let rightBound = Math.min(totalPages - 1, currentPage + 1)

    if (currentPage <= 3) {
      leftBound = 2
      rightBound = Math.min(4, totalPages - 1)
    } else if (currentPage >= totalPages - 2) {
      leftBound = Math.max(totalPages - 3, 2)
      rightBound = totalPages - 1
    }

    if (leftBound > 2) {
      items.push(ellipsis("start"))
    }

    for (let i = leftBound; i <= rightBound; i++) {
      addPageButton(i)
    }

    if (rightBound < totalPages - 1) {
      items.push(ellipsis("end"))
    }

    if (totalPages > 1) {
      addPageButton(totalPages)
    }

    return items
  }

  return (
    <div className="flex items-center justify-center gap-1 mt-4">
      <Button
        variant="outline"
        size="icon"
        className="h-8 w-8 bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
        asChild
        disabled={currentPage === 1}
      >
        <Link href={createPageUrl(1)}>
          <ChevronsLeft className="h-4 w-4 text-white" />
        </Link>
      </Button>
      <Button
        variant="outline"
        size="icon"
        className="h-8 w-8 bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
        asChild
        disabled={currentPage === 1}
      >
        <Link href={createPageUrl(Math.max(1, currentPage - 1))}>
          <ChevronLeft className="h-4 w-4 text-white" />
        </Link>
      </Button>

      {renderPageNumbers()}

      <Button
        variant="outline"
        size="icon"
        className="h-8 w-8 bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
        asChild
        disabled={currentPage === totalPages}
      >
        <Link href={createPageUrl(Math.min(totalPages, currentPage + 1))}>
          <ChevronRight className="h-4 w-4 text-white" />
        </Link>
      </Button>
      <Button
        variant="outline"
        size="icon"
        className="h-8 w-8 bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
        asChild
        disabled={currentPage === totalPages}
      >
        <Link href={createPageUrl(totalPages)}>
          <ChevronsRight className="h-4 w-4 text-white" />
        </Link>
      </Button>
    </div>
  )
}

function PageButton({ page, isActive, children }: { page: number; isActive: boolean; children: React.ReactNode }) {
  return (
    <Button
      variant="outline"
      size="icon"
      className={`h-8 w-8 font-bold ${
        isActive
          ? "bg-[#1A3A5A] text-white border-white/20"
          : "bg-[#0F2942]/80 text-white border-white/10 hover:bg-[#0F2942] hover:border-white/20"
      }`}
      asChild
    >
      <Link href={createPageUrl(page)}>{children}</Link>
    </Button>
  )
}

function createPageUrl(page: number): string {
  const params = new URLSearchParams(useSearchParams())
  params.set("page", page.toString())
  return `?${params.toString()}`
}