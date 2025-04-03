import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";

interface InputBarProps {
  input: string
  setInput: (input: string) => void
  placeholder?: string
  disabled?: boolean
  className?: string
}

export function InputBar({ input, setInput, placeholder, disabled, className }: InputBarProps) {

  const inputBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const inputBorderColor = "border-white/10 hover:border-white/20"
  const inputTextSize = "text-xs sm:text-sm md:text-base"
  const inputTextColor = "text-white"
  const inputPlaceholderColor = "placeholder:text-white/60"
  const inputSelectionColor = "selection:bg-blue-500 selection:text-white"
  const inputAnimation = "transition-all duration-300"

  return (
    <div className={cn(className)}>
      <Input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className={cn(
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
