import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";

interface SearchTypeSelectorProps {
  searchType: string
  onSearchTypeChange: (type: string) => void
}

const searchTypeOptions: { value: string, label: string, short: string }[] = [
  { value: "vn", label: "Visual Novels", short: "V" },
  { value: "release", label: "Releases", short: "R" },
  { value: "character", label: "Characters", short: "C" },
  { value: "producer", label: "Producers", short: "P" },
  { value: "staff", label: "Staff", short: "S" },
  { value: "tag", label: "Tags", short: "G" },
  { value: "trait", label: "Traits", short: "I" },
]

export function SearchTypeSelector({ searchType, onSearchTypeChange }: SearchTypeSelectorProps) {
  const [open, setOpen] = useState(false)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 select-none
          text-white hover:text-white/80 text-base md:text-lg font-bold font-serif italic transition-all duration-300"
        >
          <span className="font-serif italic font-black text-xl text-white">
            {searchTypeOptions.find(t => t.value === searchType)?.short}
          </span>
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-48 p-1 bg-[#0F2942]/80 border-white/10" align="start">
        <div className="grid gap-1">
          {searchTypeOptions.map((option) => (
            <Button
              key={option.value}
              variant="ghost"
              className={`w-full justify-start font-normal text-white hover:text-white hover:bg-white/10 select-none ${searchType === option.value ? "bg-white/10" : ""}`}
              onClick={() => {
                onSearchTypeChange(option.value)
                setOpen(false)
              }}
            >
              <span className="font-serif italic font-black mr-2">
                {option.short}
              </span>
              {option.label}
            </Button>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  )
}