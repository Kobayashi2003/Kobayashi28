import type React from "react"
import { cn } from "@/lib/utils"

interface RowProps {
  label: string
  value: React.ReactNode
}

export function Row({ label, value }: RowProps) {
  if (!value) return null

  return (
    <div className="grid grid-cols-[100px_1fr] gap-2 items-start text-sm">
      <span className="text-white/60 font-medium shrink-0">{label}</span>
      <div className={cn("text-white/90 min-w-0 break-words")}>
        {value}
      </div>
    </div>
  )
}