import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"

interface LevelSelecterProps {
  levelOptions: {
    key: string,
    label: string,
    labelSmall?: string,
    value: string,
    activeColor: string,
  }[],
  selectedValue: string,
  onChange: (value: string) => void,
}

export function LevelSelecter({ levelOptions, selectedValue, onChange }: LevelSelecterProps) {
  return (
    <>
      {/* When screen is large enough, show all options */}
      <div className="hidden sm:flex flex-wrap gap-2 items-center select-none">
        {levelOptions.map((option) => (
          <button
            key={option.key}
            onClick={() => onChange(option.value)}
            className={`transition-colors ${
              selectedValue === option.value 
                ? option.activeColor 
                : "text-white"
            } hover:text-white/80`}
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