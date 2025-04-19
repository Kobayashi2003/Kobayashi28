import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface IconButtonProps {
  icon: React.ReactNode
  variant?: "default" | "outline" | "ghost" | "link" | "destructive" | "secondary" | null
  tooltip?: string
  tooltipPosition?: "top" | "bottom" | "left" | "right"
  onClick?: () => void
  disabled?: boolean
  className?: string
}

export function IconButton({ icon, variant, tooltip, tooltipPosition, onClick, disabled, className }: IconButtonProps) {

  const buttonBgColor = "bg-transparent hover:bg-white/10"
  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-white hover:text-white/80"
  const buttonBorderColor = "border-white/10 hover:border-white/20"
  const buttonAnimation = "transition-all duration-300"

  const tooltipBgColor = "bg-black/50"
  const tooltipTextColor = "text-white/80"
  const tooltipFontSize = "text-xs sm:text-sm md:text-base"

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant={variant}
            size="icon"
            onClick={onClick}
            disabled={disabled}
            className={cn(
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
            {icon}
          </Button>
        </TooltipTrigger>
        <TooltipContent
          side={tooltipPosition}
          className={cn(
            tooltipBgColor,
            tooltipTextColor,
            tooltipFontSize,
            !tooltip && "hidden"
          )}
        >
          <p>{tooltip}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
