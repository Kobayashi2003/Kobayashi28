import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { SearchIcon } from "lucide-react"

interface SearchBarProps {
  searchQuery: string
  setSearchQuery: (query: string) => void
}

export function SearchBar({ searchQuery, setSearchQuery }: SearchBarProps) {
  return (
    <div className="relative">
      <Label htmlFor="searchBar" className="absolute left-3 top-1/2 -translate-y-1/2 text-white/60">
        <SearchIcon className="h-5 w-5" />
      </Label>
      <Input
        id="searchBar"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search..."
        className="pl-10 bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white placeholder:text-white/60"
      />
    </div>
  )
}
