import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react"

interface PaginationButtonsProps {
  totalPages: number
  currentPage: number
  onPageChange: (page: number) => void
  disabled?: boolean
  className?: string
}

function getPageButtons(currentPage: number, totalPages: number, size: "long" | "medium" | "short") {
  switch (size) {
    case "long":
      const minPageLong = (currentPage - currentPage % 10)
      const maxPageLong = ((currentPage - currentPage % 10) / 10 + 1) * 10 + 1
      return Array.from({ length: maxPageLong - minPageLong + 1 }, (_, i) => minPageLong + i).filter(page => page > 0 && page <= totalPages)
    case "medium":
      if (totalPages < 7) {
        return Array.from({ length: totalPages }, (_, i) => i + 1)
      } else {
        return [1, ...Array.from({ length: 5 }, (_, i) => currentPage - 2 + i).filter(page => page > 1 && page < totalPages), totalPages]
      }
    case "short":
      if (totalPages < 5) {
        return Array.from({ length: totalPages }, (_, i) => i + 1)
      } else {
        return [1, ...Array.from({ length: 3 }, (_, i) => currentPage - 1 + i).filter(page => page > 1 && page < totalPages), totalPages]
      }
  }
}

function addIndicators(pageButtons: number[]) {
  for (let i = 0; i < pageButtons.length - 1; i++) {
    if (pageButtons[i] + 1 !== pageButtons[i + 1]) {
      pageButtons.splice(++i, 0, 0)
    }
  }
  return pageButtons
}

export function PaginationButtons({ currentPage, totalPages, onPageChange, disabled, className }: PaginationButtonsProps) {

  const containerStyle = "flex justify-center items-center gap-1 bg-transparent select-none"
  const buttonStyle = "bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/50 text-white hover:text-white/50"

  return (
    <div className={cn(containerStyle, className)}>
      <Button
        variant="outline"
        size="icon"
        onClick={() => onPageChange(1)}
        disabled={disabled || currentPage === 1}
        className={cn(buttonStyle)}
      >
        <ChevronsLeft className="w-4 h-4" />
      </Button>

      <Button
        variant="outline"
        size="icon"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={disabled || currentPage === 1}
        className={cn(buttonStyle)}
      >
        <ChevronLeft className="w-4 h-4" />
      </Button>

      {getPageButtons(currentPage, totalPages, "long").map((page) => (
        <Button
          key={page}
          variant="outline"
          size="icon"
          onClick={() => onPageChange(page)}
          disabled={disabled || currentPage === page}
          className={cn(buttonStyle, "hidden lg:block")}
        >
          {page}
        </Button>
      ))}

      {addIndicators(getPageButtons(currentPage, totalPages, "medium")).map((page, index) => (
        page === 0 ? (
          <div key={`page-ellipsis-${index}`} className="hidden md:block lg:hidden">
            ...
          </div>
        ) : (
          <Button
            key={page}
            variant="outline"
            size="icon"
            onClick={() => onPageChange(page)}
            disabled={disabled || currentPage === page}
            className={cn(buttonStyle, "hidden md:block lg:hidden")}
          >
            {page}
          </Button>
        )
      ))}

      {addIndicators(getPageButtons(currentPage, totalPages, "short")).map((page, index) => (
        page === 0 ? (
          <div key={`page-ellipsis-${index}`} className="block md:hidden">
            ...
          </div>
        ) : (
          <Button
            key={page}
            variant="outline"
            size="icon"
            onClick={() => onPageChange(page)}
            disabled={disabled || currentPage === page}
            className={cn(buttonStyle, "block md:hidden")}
          >
            {page}
          </Button>
        )
      ))}

      <Button
        variant="outline"
        size="icon"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={disabled || currentPage === totalPages}
        className={cn(buttonStyle)}
      >
        <ChevronRight className="w-4 h-4" />
      </Button>

      <Button
        variant="outline"
        size="icon"
        onClick={() => onPageChange(totalPages)}
        disabled={disabled || currentPage === totalPages}
        className={cn(buttonStyle)}
      >
        <ChevronsRight className="w-4 h-4" />
      </Button>
    </div>
  )
}
