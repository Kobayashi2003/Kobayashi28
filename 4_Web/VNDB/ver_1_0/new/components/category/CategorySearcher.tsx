import { cn } from "@/lib/utils"
import { InputBar } from "../input/InputBar"
import { SubmitButton } from "../button/SubmitButton"
import { CancelButton } from "../button/CancelButton"


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
      <InputBar
        input={query}
        setInput={setQuery}
        placeholder="Search in current category"
        disabled={loading}
        className="w-full"
      />
      <SubmitButton
        handleSubmit={handleSearch}
        disabled={loading}
      />
      {isSearching && (
        <CancelButton
          handleCancel={() => { setQuery(""); handleSearch() }}
          disabled={loading}
        />
      )}
    </form>
  )
}
