import { cn } from "@/lib/utils"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"

interface LevelSelecterProps {
  levelOptions: {
    key: string,
    label: string,
    labelSmall?: string,
    value: string,
    activeColor?: string,
    defaultColor?: string,
    className?: string,
    defaultClassName?: string,
    activeClassName?: string,
  }[],
  selectedValue: string,
  onChange: (value: string) => void,
  className?: string,
}

export function LevelSelecter({ levelOptions, selectedValue, onChange, className }: LevelSelecterProps) {
  return (
    <>
      {/* When screen is large enough, show all options */}
      <div className={`hidden sm:flex flex-wrap gap-2 items-center select-none ${className}`}>
        {levelOptions.map((option) => (
          <button
            key={option.key}
            onClick={() => onChange(option.value)}
            className={cn(
              "transition-colors",
              selectedValue === option.value
                ? option.activeColor || "text-white"
                : option.defaultColor || "text-white/80",
              selectedValue === option.value
                ? option.activeClassName
                : option.defaultClassName,
              option.className
            )}
          >
            {option.label}
          </button>
        ))}
      </div>
      {/* When screen is small, show a dropdown */}
      <div className="sm:hidden">
        <Select value={selectedValue} onValueChange={(value) => onChange(value)}>
          <SelectTrigger className="bg-[#0F2942]/80 border-white/10 text-white font-bold">
            <SelectValue placeholder="Level" />
          </SelectTrigger>
          <SelectContent className="bg-[#0F2942]/80 border-white/10 text-white font-bold">
            {levelOptions.map((option) => (
              <SelectItem key={option.key} value={option.value}>
                {option.labelSmall || option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </>
  )
}