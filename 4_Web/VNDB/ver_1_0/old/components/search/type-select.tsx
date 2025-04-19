"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import type { SearchType } from "@/lib/types"

interface TypeSelectProps {
  value: SearchType
  onValueChange: (value: SearchType) => void
}

interface TypeOption {
  value: SearchType
  label: string
  short: string
}

const searchTypes: TypeOption[] = [
  { value: "vn", label: "Visual Novels", short: "V" },
  { value: "release", label: "Releases", short: "R" },
  { value: "character", label: "Characters", short: "C" },
  { value: "producer", label: "Producers", short: "P" },
  { value: "staff", label: "Staff", short: "S" },
  { value: "tag", label: "Tags", short: "G" },
  { value: "trait", label: "Traits", short: "I" },
]

export function TypeSelect({ value, onValueChange }: TypeSelectProps) {
  const [open, setOpen] = useState(false)
  const currentType = searchTypes.find((t) => t.value === value)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          className="w-12 h-10 bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
        >
          <span className="font-serif italic font-black text-xl text-white">{currentType?.label[0]}</span>
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-48 p-1 bg-[#0F2942] border-white/10" align="start">
        <div className="grid gap-1">
          {searchTypes.map((type) => (
            <Button
              key={type.value}
              variant="ghost"
              className="w-full justify-start font-normal text-white hover:bg-white/10 hover:text-white"
              onClick={() => {
                onValueChange(type.value)
                setOpen(false)
              }}
            >
              <span className="font-serif italic font-black mr-2">{type.short}</span>
              {type.label}
            </Button>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  )
}