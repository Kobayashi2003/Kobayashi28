import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react"
import { Button } from "@/components/ui/button"

interface PaginationButtonsProps {
  totalPages: number,
  currentPage: number,
  onPageChange: (page: number) => void,
  disabled?: boolean
  className?: string
}

export function PaginationButtons({ currentPage, totalPages, onPageChange }: PaginationButtonsProps) {

  const pageButtonsLong: number[] = []
  const minPageLong = (currentPage - currentPage % 10)
  const maxPageLong = ((currentPage - currentPage % 10) / 10 + 1) * 10 + 1
  for (let i = minPageLong; i <= maxPageLong; ++i) {
    if (i > 0 && i <= totalPages) {
      pageButtonsLong.push(i)
    }
  }

  const pageButtonsMedium: number[] = []
  if (totalPages < 7) {
    for (let i = 1; i <= totalPages; ++i) {
      pageButtonsMedium.push(i)
    }
  } else {
    pageButtonsMedium.push(1)
    for (let i = currentPage -2; i <= currentPage + 2; ++i) {
      if (i > 1 && i < totalPages) {
        pageButtonsMedium.push(i)
      }
    }
    pageButtonsMedium.push(totalPages)
  }
  // insert 0 to the pageButtons array to indicate the omitted pages
  for (let i = 0; i < pageButtonsMedium.length - 1; ++i) {
    if (pageButtonsMedium[i] + 1 !== pageButtonsMedium[i + 1]) {
      pageButtonsMedium.splice(++i, 0, 0)
    }
  }

  const pageButtonsShort: number[] = []
  if (totalPages < 5) {
    for (let i = 1; i <= totalPages; i++) {
      pageButtonsShort.push(i)
    }
  } else {
    pageButtonsShort.push(1)
    for (let i = currentPage - 1; i <= currentPage + 1; ++i) {
      if (i > 1 && i < totalPages) {
        pageButtonsShort.push(i)
      }
    }
    pageButtonsShort.push(totalPages)
  }
  // insert 0 to the pageButtons array to indicate the omitted pages
  for (let i = 0; i < pageButtonsShort.length - 1; ++i) {
    if (pageButtonsShort[i] + 1 !== pageButtonsShort[i + 1]) {
      pageButtonsShort.splice(++i, 0, 0)
    }
  }

  return (
    <div className="flex items-center gap-1 text-white select-none">

      <Button
        variant="outline"
        size="icon"
        className="h-8 w-8 border border-white/10 bg-[#0F2942]/80 hover:bg-[#0F2942] hover:border-white/50 hover:text-white/50"
        asChild
        disabled={currentPage === 1}
        onClick={() => onPageChange(1)}
      >
        <ChevronsLeft />
      </Button>

      <Button
        variant="outline"
        size="icon"
        className="h-8 w-8 border border-white/10 bg-[#0F2942]/80 hover:bg-[#0F2942] hover:border-white/50 hover:text-white/50"
        asChild
        disabled={currentPage === 1}
        onClick={() => {
          if (currentPage > 1) {
            onPageChange(currentPage - 1)
          }
        }}
      >
        <ChevronLeft />
      </Button>

      {pageButtonsLong.map((page, index) => (
        <Button
          key={`page-button-${page}`}
          variant="outline"
          size="icon"
          className="h-8 w-8 border border-white/10 bg-[#0F2942]/80 hover:bg-[#0F2942] hover:border-white/50 hover:text-white/50 hidden lg:block"
          disabled={currentPage === page}
          onClick={() => onPageChange(page)}
        >
          {page}
        </Button>
      ))}

      {pageButtonsMedium.map((page, index) => (
        page === 0 ? (
          <div key={`page-ellipsis-${index}`} className="hidden md:block lg:hidden">
            ...
          </div>
        ) : (
          <Button
            key={`page-button-${page}`}
            variant="outline"
            size="icon"
            className="h-8 w-8 border border-white/10 bg-[#0F2942]/80 hover:bg-[#0F2942] hover:border-white/50 hover:text-white/50 hidden md:block lg:hidden"
            disabled={currentPage === page}
            onClick={() => onPageChange(page)}
          >
            {page}
          </Button>
        )
      ))}

      {pageButtonsShort.map((page, index) => (
        page === 0 ? (
          <div key={`page-ellipsis-${index}`} className="block md:hidden">
            ...
          </div>
        ) : (
          <Button
            key={`page-button-${page}`}
            variant="outline"
            size="icon"
            className="h-8 w-8 border border-white/10 bg-[#0F2942]/80 hover:bg-[#0F2942] hover:border-white/50 hover:text-white/50 block md:hidden"
            disabled={currentPage === page}
            onClick={() => onPageChange(page)}
          >
            {page}
          </Button>
        )
      ))}

      <Button
        variant="outline"
        size="icon"
        className="h-8 w-8 border border-white/10 bg-[#0F2942]/80 hover:bg-[#0F2942] hover:border-white/50 hover:text-white/50"
        asChild
        disabled={currentPage === totalPages}
        onClick={() => {
          if (currentPage < totalPages) {
            onPageChange(currentPage + 1)
          }
        }}
      >
        <ChevronRight />
      </Button>

      <Button
        variant="outline"
        size="icon"
        className="h-8 w-8 border border-white/10 bg-[#0F2942]/80 hover:bg-[#0F2942] hover:border-white/50 hover:text-white/50"
        asChild
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(totalPages)}
      >
        <ChevronsRight />
      </Button>
    </div>
  )
}
