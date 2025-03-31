import { cn } from "@/lib/utils";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";

interface levelOption {
  key: string
  value: string
  label: string
  selectedClassName?: string
  unselectedClassName?: string
  className?: string
}

interface LevelSelectorProps {
  levelOptions: levelOption[]
  selectedLevel: string
  setSelectedLevel: (value: string) => void
  disabled?: boolean
  className?: string
}

export function LevelSelectorButton({ levelOptions, selectedLevel, setSelectedLevel, disabled, className }: LevelSelectorProps) {
  const containerStyle = "flex flex-wrap gap-2 justify-center items-center"
  const buttonBaseStyle = "text-xs sm:text-sm md:text-base transition-all duration-300"

  return (
    <div className={cn(containerStyle, className)}>
      {levelOptions.map((option) => (
        <button
          key={option.key}
          onClick={() => setSelectedLevel(option.value)}
          disabled={disabled}
          className={cn(
            buttonBaseStyle,
            selectedLevel === option.value
              ? option.selectedClassName
              : option.unselectedClassName,
            option.className
          )}
        >
          {option.label}
        </button>
      ))}
    </div>
  )
}

export function LevelSelectorSelect({ levelOptions, selectedLevel, setSelectedLevel, className }: LevelSelectorProps) {
  const triggerStyle = "bg-[#0F2942]/80 border-white/10 text-white font-bold"
  const contentStyle = "bg-[#0F2942]/80 border-white/10 text-white font-bold"
  const itemStyle = ""

  return (
    <Select value={selectedLevel} onValueChange={setSelectedLevel}>
      <SelectTrigger className={cn(triggerStyle, className)}>
        <SelectValue placeholder="Level" />
      </SelectTrigger>
      <SelectContent className={cn(contentStyle)}>
        {levelOptions.map((option) => (
          <SelectItem
            key={option.value}
            value={option.value}
            className={cn(
              itemStyle,
              selectedLevel === option.value
                ? option.selectedClassName
                : option.unselectedClassName,
              option.className
            )}
          >
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}