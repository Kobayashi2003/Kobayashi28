import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { SearchIcon } from "lucide-react"

interface SearchBarProps {
  input: string
  setInput: (input: string) => void
  placeholder?: string
  disabled?: boolean
  className?: string
}

export function SearchBar({ input, setInput, placeholder, disabled, className }: SearchBarProps) {

  const containerPosition = "relative"
  const labelPosition = "absolute left-3 top-1/2 -translate-y-1/2"
  const labelTextColor = "text-white/60"
  const inputPadding = "pl-10"
  const inputBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const inputBorderColor = "border-white/10 hover:border-white/20"
  const inputTextSize = "text-xs sm:text-sm md:text-base"
  const inputTextColor = "text-white"
  const inputPlaceholderColor = "placeholder:text-white/60"
  const inputSelectionColor = "selection:bg-blue-500 selection:text-white"
  const inputAnimation = "transition-all duration-300"

  return (
    <div className={cn(containerPosition, className)}>
      <Label className={cn(labelPosition, labelTextColor)}>
        <SearchIcon className="w-4 h-4" />
      </Label>
      <Input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className={cn(
          inputPadding,
          inputBgColor,
          inputBorderColor,
          inputTextSize,
          inputTextColor,
          inputPlaceholderColor,
          inputSelectionColor,
          inputAnimation
        )}
      />
    </div>
  )
}