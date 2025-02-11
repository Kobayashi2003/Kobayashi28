import { cn } from "@/lib/utils"
import Link from "next/link"
import { Heart } from 'lucide-react'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import type { Release } from "@/lib/types"
import { PLATFORM_ICONS, PLATFORMS } from "@/lib/constants"

interface ReleaseItemProps {
  release: Release
}

// Determine the erotic content status and associated UI elements
function getEroStatus(hasEro?: boolean, uncensored?: boolean) {
  if (hasEro === undefined || hasEro === null) return null

  if (!hasEro) return { color: "text-blue-400", tooltip: "No erotic scenes" }
  if (uncensored === true) return { color: "text-green-400", tooltip: "Contains uncensored erotic scenes" }
  if (uncensored === false) return { color: "text-red-400", tooltip: "Contains erotic scenes with optical censoring" }
  return { color: "text-white", tooltip: "Contains erotic scenes" }
}

export function ReleaseItem({ release }: ReleaseItemProps) {
  const hasMTL = release.languages?.some((lang) => lang.mtl) ?? false

  // Compile release status information
  const statuses = [
    hasMTL && "machine translation",
    release.official === false && "unofficial",
    release.patch && "patch"
  ].filter(Boolean)
  const statusText = statuses.length > 0 ? `(${statuses.join(" ")})` : ""

  const eroStatus = getEroStatus(release.has_ero, release.uncensored)

  return (
    <div
      className={cn(
        "grid grid-cols-[100px_48px_120px_1fr] items-center gap-2 px-4 py-1 hover:bg-[#0F2942]/50",
        hasMTL && "opacity-60",
      )}
    >
      <div className="text-sm text-[#88ccff]">{release.released}</div>
      <div className="text-sm text-[#88ccff] flex items-center gap-1">
        {eroStatus && (
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger>
                <Heart className={cn("h-3 w-3 fill-current", eroStatus.color)} />
              </TooltipTrigger>
              <TooltipContent>
                <p className="text-xs">{eroStatus.tooltip}</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        )}
        {release.minage === 0 ? "ALL" : release.minage ? `${release.minage}+` : ""}
      </div>
      <div className="flex justify-end gap-2">
        {(release.platforms || []).map((platform, index) => {
          const platformKey = platform.toLowerCase()
          const iconClass = PLATFORM_ICONS[platformKey]
          return iconClass ? (
            <span
              key={`${release.id}-${platform}-${index}`}
              className={`${iconClass} inline-block`}
              title={PLATFORMS[platformKey]}
            />
          ) : null
        })}
      </div>
      <div className="text-sm text-[#88ccff] overflow-hidden text-ellipsis">
        <Link href={`/r${release.id}`} className="hover:text-white hover:underline transition-colors">
          {release.title}
        </Link>
        {statusText && <span className="text-[#88ccff]/80 ml-1">{statusText}</span>}
      </div>
    </div>
  )
}