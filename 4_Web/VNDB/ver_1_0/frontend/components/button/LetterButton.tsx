import { cn } from "@/lib/utils"
import { IconButton } from "@/components/button/IconButton"

interface LetterButtonProps {
  letter: string
  onClick?: () => void
  disabled?: boolean
  className?: string
}

export function LetterButton({ letter, onClick, disabled, className }: LetterButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  const icon = <span className="font-bold font-serif italic">{letter}</span>

  return (
    <IconButton
      icon={icon}
      variant="outline"
      onClick={onClick}
      disabled={disabled}
      className={cn(buttonBgColor, className)}
    />
  )
}