import { cn } from "@/lib/utils"
import { IconButton } from "@/components/button/IconButton"
import { Star, StarIcon } from "lucide-react"

interface MarkButtonProps {
  isMarked: boolean
  onClick: () => void
  disabled?: boolean
  className?: string
}

export function MarkButton({ isMarked, onClick, disabled, className }: MarkButtonProps) {

  const buttonBgColor = "bg-transparent"
  const buttonTextColor = "text-yellow-400 hover:text-yellow-300"
  const buttonAnimation = "transition-all duration-300"

  return (
    <IconButton
      icon={isMarked ? 
        <StarIcon className="w-4 h-4 fill-current" /> : 
        <Star className="w-4 h-4" />
      }
      variant="ghost"
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "select-none",
        buttonBgColor, 
        buttonTextColor, 
        buttonAnimation, 
        className
      )}
    />
  )
}