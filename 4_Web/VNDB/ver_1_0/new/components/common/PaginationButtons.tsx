import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react"
import { Button } from "@/components/ui/button"

interface PaginationButtonsProps {
  totalPages: number,
  currentPage: number,
  onPageChange: (page: number) => void,
}

export function PaginationButtons({ currentPage, totalPages, onPageChange }: PaginationButtonsProps) {

  const pageButtons = []
  if (totalPages < 7) {
    for (let i = 1; i <= totalPages; i++) {
      pageButtons.push(i)
    }
  } else {
    pageButtons.push(1)
    for (let i = currentPage -2; i <= currentPage + 2; ++i) {
      if (i > 1 && i < totalPages) {
        pageButtons.push(i)
      }
    }
    pageButtons.push(totalPages)
  }
  // insert 0 to the pageButtons array to indicate the omitted pages
  for (let i = 0; i < pageButtons.length - 1; i++) {
    if (pageButtons[i] + 1 !== pageButtons[i + 1]) {
      pageButtons.splice(++i, 0, 0)
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
        onClick={() => onPageChange(currentPage - 1)}
      >
        <ChevronLeft />
      </Button>

      {pageButtons.map((page, index) => (
        page === 0 ? (
          <div key={`page-ellipsis-${index}`}>
            ...
          </div>
        ) : (
          <Button
            key={`page-button-${page}`}
            variant="outline"
            size="icon"
            className="h-8 w-8 border border-white/10 bg-[#0F2942]/80 hover:bg-[#0F2942] hover:border-white/50 hover:text-white/50"
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
        onClick={() => onPageChange(totalPages)}
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
