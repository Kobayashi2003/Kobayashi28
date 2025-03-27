import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Star, StarIcon } from "lucide-react"

interface MarkButtonProps {
  marked: boolean
  setMarked: (marked: boolean) => void
  disabled?: boolean
  className?: string
}

export function MarkButton({ marked, setMarked, disabled, className }: MarkButtonProps) {

  const buttonBgColor = "bg-transparent"
  const buttonTextColor = "text-yellow-400 hover:text-yellow-300"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="ghost"
      size="icon"
      className={cn(buttonBgColor, buttonTextColor, buttonAnimation, className)}
      onClick={() => setMarked(!marked)}
      disabled={disabled}
    >
      {marked ? <StarIcon className="w-4 h-4 fill-current" /> : <Star className="w-4 h-4" />}
    </Button>
  )
}
