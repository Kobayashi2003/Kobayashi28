import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ArrowBigLeft } from "lucide-react"

interface BackButtonProps {
  handleBack: () => void
  disabled?: boolean
  className?: string
}

export function BackButton({ handleBack, disabled, className }: BackButtonProps) {

  const buttonBgColor = "bg-transparent hover:bg-white/10"
  const buttonTextColor = "text-white hover:text-white/80"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={handleBack}
      disabled={disabled}
      className={cn(
        "select-none",
        buttonBgColor,
        buttonTextColor,
        buttonAnimation,
        className
      )}
    >
      <ArrowBigLeft className="h-5 w-5" />
    </Button>
  )
}