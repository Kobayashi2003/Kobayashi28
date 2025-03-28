import { cn } from "@/lib/utils"
import { InputBar } from "../input/InputBar"
import { SubmitButton } from "../button/SubmitButton"
import { CancelButton } from "../button/CancelButton"


interface CategorySearcherProps {
  isSearching: boolean
  query: string
  setQuery: (query: string) => void
  handleSearch: (e?: React.FormEvent) => void
  disabled?: boolean
  className?: string
}

export function CategorySearcher({ isSearching, query, setQuery, handleSearch, disabled, className }: CategorySearcherProps) {

  const containerFlex = "flex flex-row justify-between items-center gap-2"
  const containerBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const containerBorder = "border border-white/10 hover:border-white/20 rounded-lg"
  const containerTransition = "transition-all duration-300"

  return (
    <form onSubmit={handleSearch} className={cn(
      "p-4",
      containerFlex,
      containerBgColor,
      containerBorder,
      containerTransition,
      className
    )}>
      <InputBar
        input={query}
        setInput={setQuery}
        placeholder="Search in current category"
        disabled={disabled}
        className="w-full"
      />
      <SubmitButton
        handleSubmit={handleSearch}
        disabled={disabled}
      />
      {isSearching && (
        <CancelButton
          handleCancel={() => { setQuery(""); handleSearch() }}
          disabled={disabled}
        />
      )}
    </form>
  )
}
