import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { RefreshCw } from "lucide-react"

interface ReloadButtonProps {
  handleReload?: () => void
  disabled?: boolean
  className?: string
}

export function ReloadButton({ handleReload, disabled, className }: ReloadButtonProps) {

  const buttonBgColor = "bg-transparent hover:bg-blue-400"
  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-blue-400 hover:text-white"
  const buttonBorderColor = "border-blue-400/40 hover:border-blue-400/60"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={handleReload}
      disabled={disabled}
      className={cn(
        "group",
        "select-none",
        buttonBgColor,
        buttonFont,
        buttonTextSize,
        buttonTextColor,
        buttonBorderColor,
        buttonAnimation,
        className
      )}
    >
      <RefreshCw className="w-4 h-4 group-hover:animate-spin" />
    </Button>
  )
}