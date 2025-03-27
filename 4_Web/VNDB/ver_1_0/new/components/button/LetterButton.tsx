import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

interface LetterButtonProps {
  letter: string
  onClick: () => void
  disabled?: boolean
  className?: string
}

export function LetterButton({ letter, onClick, disabled, className }: LetterButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20"
  const buttonFont = "font-bold font-serif italic"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-white hover:text-white/80"
  const buttonBorderColor = "border-white/10 hover:border-white/20"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={onClick}
      disabled={disabled}
      className={cn(
        buttonBgColor,
        buttonFont,
        buttonTextSize,
        buttonTextColor,
        buttonBorderColor,
        buttonAnimation,
        className
      )}
    >
      {letter}
    </Button>
  )
}