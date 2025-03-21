import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ArrowRight, X } from "lucide-react"

interface CategorySearcherProps {
  loading: boolean
  isSearching: boolean
  query: string
  setQuery: (query: string) => void
  handleSearch: (e?: React.FormEvent) => void
  className?: string
}

export function CategorySearcher({ loading, isSearching, query, setQuery, handleSearch, className }: CategorySearcherProps) {
  return (
    <form onSubmit={handleSearch} className={cn(
      "bg-[#0F2942]/80 hover:bg-[#0F2942] flex flex-row gap-2 p-4",
      "border border-white/10 hover:border-white/20 rounded-lg",
      "transition-all duration-300",
      className
    )}>
      <Input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search in current category"
        className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 text-white placeholder:text-white/60"
      />
      <Button
        variant="outline"
        size="icon"
        disabled={loading}
        onClick={handleSearch}
        className={cn(
          "bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20",
          "text-white hover:text-white/80 font-bold text-base md:text-lg transition-all duration-300",
          loading && "animate-pulse"
        )}
      >
        <ArrowRight className="w-4 h-4" />
      </Button>
      {isSearching && (
        <Button
          variant="outline"
          size="icon"
          onClick={() => {
            setQuery("")
            handleSearch()
          }}
          className={cn(
            "bg-[#0F2942]/80 hover:bg-[#0F2942] border-red-500/20 hover:border-red-500/40",
            "text-red-500 hover:text-red-600 font-bold text-base md:text-lg transition-all duration-300",
            loading && "animate-pulse"
          )}
        >
          <X className="w-4 h-4" />
        </Button>
      )}
    </form>
  )
}
