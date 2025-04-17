import { cn } from "@/lib/utils";
import { Row } from "@/components/row/Row";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { ICON } from "@/lib/icons";
import { ENUMS } from "@/lib/enums";


interface PlatformsRowProps {
  platforms: string[]
}

export function PlatformsRow({ platforms }: PlatformsRowProps) {

  if (platforms.length === 0) return null

  return (
    <Row label="Platforms" value={
      <div className="flex flex-wrap gap-1 items-center">
        {platforms.map((platform) => (
          <Tooltip key={platform}>
            <TooltipTrigger asChild>
              <span key={platform} className={cn(
              ICON.PLATFORM[platform as keyof typeof ICON.PLATFORM]
            )} />
            </TooltipTrigger>
            <TooltipContent className="bg-black/50 text-white text-xs">
              {ENUMS.PLATFORM[platform as keyof typeof ENUMS.PLATFORM]}
            </TooltipContent>
          </Tooltip>
        ))}
      </div>
    } />
  )
}
