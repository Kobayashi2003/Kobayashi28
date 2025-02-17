"use client"

import type React from "react"
import Image from "next/image"
import Link from "next/link"
import { useSearchParams } from "next/navigation" 
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react"
import type { SearchType, ResourceType, VisualNovelDataBaseQueryResponse } from "@/lib/types"

interface SearchResultsProps {
  type: SearchType
  response?: VisualNovelDataBaseQueryResponse<ResourceType>
  currentPage: number
  itemsPerPage: number
}

export function SearchResults({ type, response, currentPage, itemsPerPage }: SearchResultsProps) {
  if (!response) {
    return <p className="text-center text-lg text-white">No results found.</p>
  }

  const { results, count } = response

  if (results.length === 0) {
    return <p className="text-center text-lg text-white">No results found.</p>
  }

  // TODO
  const uniqueResults = Array.from(new Map(results.map((item) => [item.id, item])).values())

  const totalPages = count ? Math.ceil(count / itemsPerPage) : 0

  return (
    <div>
      <p className="mb-4 text-lg text-white">{count} results found</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 xl:grid-cols-7 gap-6 mb-8">
        {uniqueResults.map((item) => renderResultItem(type, item))}
      </div>
      {totalPages > 1 && <SearchPagination currentPage={currentPage} totalPages={totalPages} />}
    </div>
  )
}

function renderResultItem(type: SearchType, item: ResourceType) {
  switch (type) {
    case "vn":
    case "character":
      return <ImageResultCard key={item.id} type={type} item={item} />
    case "release":
    case "producer":
    case "staff":
    case "tag":
    case "trait":
      return <TextResultCard key={item.id} type={type} item={item} />
    default:
      return null
  }
}

function ImageResultCard({ type, item }: { type: SearchType; item: ResourceType }) {
  const title = getTitle(type, item)
  const imageUrl = getImageUrl(type, item)

  return (
    <Link href={`/${item.id}`} className="block group">
      <div className="bg-[#0F2942] rounded-lg overflow-hidden shadow-lg transition-all duration-300 ease-in-out group-hover:shadow-xl group-hover:scale-105">
        <div className="relative w-full" style={{ paddingBottom: "117.1875%" }}>
          {imageUrl ? (
            <Image
              src={imageUrl || "/placeholder.svg"}
              alt={title || "Image"}
              layout="fill"
              objectFit="cover"
              loading="lazy"
              className="transition-transform duration-300 ease-in-out group-hover:scale-110"
            />
          ) : (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-200 text-gray-500">No image</div>
          )}
        </div>
        <div className="p-4 transition-colors duration-300 ease-in-out group-hover:bg-[#1A3A5A]">
          <h2 className="text-lg font-semibold text-white mb-2 truncate">{title}</h2>
        </div>
      </div>
    </Link>
  )
}

function TextResultCard({ type, item }: { type: SearchType; item: ResourceType }) {
  const title = getTitle(type, item)

  return (
    <Link href={`/${item.id}`} className="block group">
      <div className="bg-[#0F2942] rounded-lg overflow-hidden shadow-lg transition-all duration-300 ease-in-out group-hover:shadow-xl group-hover:scale-105 p-4">
        <h2 className="text-lg font-semibold text-white mb-2 truncate transition-colors duration-300 ease-in-out group-hover:text-blue-300">
          {title}
        </h2>
      </div>
    </Link>
  )
}

function SearchPagination({ currentPage, totalPages }: { currentPage: number; totalPages: number }) {
  const renderPageNumbers = () => {
    const items: React.ReactNode[] = []
    const ellipsis = (key: string) => (
      <span key={key} className="px-2 text-white font-bold">
        ...
      </span>
    )

    // Helper function to add page numbers
    const addPageButton = (pageNum: number) => {
      items.push(
        <PageButton key={pageNum} page={pageNum} isActive={currentPage === pageNum}>
          {pageNum}
        </PageButton>,
      )
    }

    // Always show first page
    addPageButton(1)

    // Calculate the range of pages to show around current page
    let leftBound = Math.max(2, currentPage - 1)
    let rightBound = Math.min(totalPages - 1, currentPage + 1)

    // Adjust bounds for edge cases
    if (currentPage <= 3) {
      leftBound = 2
      rightBound = Math.min(4, totalPages - 1)
    } else if (currentPage >= totalPages - 2) {
      leftBound = Math.max(totalPages - 3, 2)
      rightBound = totalPages - 1
    }

    // Add ellipsis if there's a gap after first page
    if (leftBound > 2) {
      items.push(ellipsis("start"))
    }

    // Add page numbers between bounds
    for (let i = leftBound; i <= rightBound; i++) {
      addPageButton(i)
    }

    // Add ellipsis if there's a gap before last page
    if (rightBound < totalPages - 1) {
      items.push(ellipsis("end"))
    }

    // Always show last page if we have more than one page
    if (totalPages > 1) {
      addPageButton(totalPages)
    }

    return items
  }

  return (
    <div className="flex items-center justify-center gap-1">
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

function getTitle(type: SearchType, item: ResourceType): string {
  switch (type) {
    case "vn":
    case "release":
      return (item as any).title || "Untitled"
    case "character":
    case "producer":
    case "staff":
    case "tag":
    case "trait":
      return (item as any).name || "Unnamed"
    default:
      return "Unknown"
  }
}

function getImageUrl(type: SearchType, item: ResourceType): string | null {
  if (type === "vn" || type === "character") {
    return (item as any).image?.url || null
  }
  return null
}