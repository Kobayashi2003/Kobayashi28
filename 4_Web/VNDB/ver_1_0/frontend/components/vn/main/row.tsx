import type React from "react"
import { cn } from "@/lib/utils"

// Props for the Row component
interface RowProps {
  label: string
  value: React.ReactNode
  icon?: React.ReactNode
  className?: string
}

// Component to display a single row of information
export function Row({ label, value, icon, className }: RowProps) {
  if (!value) return null

  return (
    <div className="grid grid-cols-[120px_1fr] gap-4 items-start text-sm">
      {/* Label */}
      <span className="text-white/60 font-medium shrink-0">{label}</span>
      {/* Value with optional icon */}
      <div className={cn("text-white/90 min-w-0 break-words", className)}>
        {icon && <span className="mr-2">{icon}</span>}
        {value}
      </div>
    </div>
  )
}