import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Trash2 } from "lucide-react"

interface DeleteButtonProps {
  handleDelete: () => void
  disabled?: boolean
  className?: string
}

export function DeleteButton({ handleDelete, disabled, className }: DeleteButtonProps) {

  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-red-400 hover:text-white"
  const buttonBorderColor = "border-red-400/40 hover:border-red-400/60"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={handleDelete}
      disabled={disabled}
      className={cn(
        "select-none",
        buttonFont,
        buttonTextSize,
        buttonTextColor,
        buttonBorderColor,
        buttonAnimation,
        className
      )}
    >
      <Trash2 className="w-4 h-4" />
    </Button>
  )
}