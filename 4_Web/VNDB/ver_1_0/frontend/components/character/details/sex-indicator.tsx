import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { SEX, SEX_ICONS, SEX_COLORS } from "@/lib/constants"
import { cn } from "@/lib/utils"

interface SexIndicatorProps {
  sex?: string[]
  spoilerLevel: number
}

export function SexIndicator({ sex, spoilerLevel }: SexIndicatorProps) {
  if (!sex?.length) return null

  const [apparent, real] = sex
  const showReal = spoilerLevel === 2 && real && apparent !== real

  const getSexIcon = (sexValue: string | null) => {
    if (!sexValue) return null
    return (
      <span
        className={cn(SEX_ICONS[sexValue as keyof typeof SEX_ICONS], SEX_COLORS[sexValue as keyof typeof SEX_COLORS])}
      />
    )
  }

  const getSexDisplay = (sexValue: string | null) => {
    if (!sexValue) return "Unknown"
    return SEX[sexValue as keyof typeof SEX] || "Unknown"
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger className="flex items-center gap-1">
          {getSexIcon(apparent)}
          {showReal && (
            <>
              <span className="text-white/20 mx-1">→</span>
              {getSexIcon(real)}
            </>
          )}
        </TooltipTrigger>
        <TooltipContent side="top" className="bg-[#0F2942]">
          <p className="text-white">
            {getSexDisplay(apparent)}
            {showReal && (
              <>
                <span className="text-white/60 mx-1">→</span>
                {getSexDisplay(real)}
              </>
            )}
          </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}