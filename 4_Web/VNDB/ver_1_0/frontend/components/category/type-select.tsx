"use client"

import { Button } from "@/components/ui/button"

interface Type {
  code: "v" | "c" | "p" | "s"
  label: string
  short: string
}

const TYPES: Type[] = [
  { code: "v", label: "Visual Novel", short: "𝓥" },
  { code: "c", label: "Character", short: "𝓒" },
  { code: "p", label: "Producer", short: "𝓟" },
  { code: "s", label: "Staff", short: "𝓢" },
]

interface TypeSelectProps {
  activeType: "v" | "c" | "p" | "s"
  onTypeChange: (type: "v" | "c" | "p" | "s") => void
}

export function TypeSelect({ activeType, onTypeChange }: TypeSelectProps) {
  return (
    <div className="flex space-x-4 mb-6">
      {TYPES.map((type) => (
        <Button
          key={type.code}
          onClick={() => onTypeChange(type.code)}
          variant={activeType === type.code ? "default" : "outline"}
          className={`min-w-[100px] bg-[#0A1929] hover:bg-[#0F2942] border-white/10 ${
            activeType === type.code ? "border-2 border-white/40" : ""
          }`}
        >
          <span className="font-serif text-xl text-white mr-2">{type.short}</span>
          <span className="text-sm text-white/80">{type.label}</span>
        </Button>
      ))}
    </div>
  )
}