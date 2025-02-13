import { SPOILER } from "@/lib/constants"
import { cn } from "@/lib/utils"

interface SpoilerControlsProps {
  value: number
  onChange: (value: number) => void
}

export function SpoilerControls({ value, onChange }: SpoilerControlsProps) {
  return (
    <div className="flex items-center gap-2 text-sm">
      {SPOILER.map((level, index) => (
        <div key={level.id} className="flex items-center">
          <button
            onClick={() => onChange(level.value)}
            className={cn(
              "hover:text-white transition-colors",
              value === level.value ? "text-[#88ccff]" : "text-white/60",
            )}
          >
            {level.label}
          </button>
          {index < SPOILER.length - 1 && <span className="text-white/20 ml-2">|</span>}
        </div>
      ))}
    </div>
  )
}