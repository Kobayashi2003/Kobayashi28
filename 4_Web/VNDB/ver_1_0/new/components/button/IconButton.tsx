import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface IconButtonProps {
  icon: React.ReactNode
  tooltip?: string
  onClick: () => void
  disabled?: boolean
  className?: string
}

export function IconButton({ icon, tooltip, onClick, disabled, className }: IconButtonProps) {

  const buttonBgColor = "bg-transparent hover:bg-white/10"
  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-white hover:text-white/80"
  const buttonBorderColor = "border-white/10 hover:border-white/20"
  const buttonAnimation = "transition-all duration-300"

  const tooltipBgColor = "bg-black/80"
  const tooltipTextColor = "text-white"
  const tooltipFontSize = "text-sm md:text-base"

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant="outline"
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
