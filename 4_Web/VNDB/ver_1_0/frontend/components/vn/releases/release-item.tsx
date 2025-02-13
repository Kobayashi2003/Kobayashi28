import type { Release } from "@/lib/types"
import { PLATFORM_ICONS, PLATFORMS, MEDIUM, RELEASE_ICONS, VOICED } from "@/lib/constants"
import { cn } from "@/lib/utils"
import { Heart } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import Link from "next/link"

interface ReleaseItemProps {
  release: Release
}

// Helper function to determine media icon type
function getMediaIcon(media: Array<{ medium?: string; qty?: number }>) {
  if (media.some((m) => m.medium?.toLowerCase() === "in")) return RELEASE_ICONS.media.download
  if (media.some((m) => ["cd", "dvd", "bd", "blr", "gdr", "umd", "flp", "gd"].includes(m.medium?.toLowerCase() || "")))
    return RELEASE_ICONS.media.disk
  if (media.some((m) => ["cart", "mrt"].includes(m.medium?.toLowerCase() || ""))) return RELEASE_ICONS.media.cartridge
  return RELEASE_ICONS.media.disk
}

// Helper function to generate media tooltip text
function getMediaTooltip(media: Array<{ medium?: string; qty?: number }>) {
  return media
    .map(({ medium, qty }) => {
      const mediumName = MEDIUM[medium?.toLowerCase() || ""] || medium
      if (!qty || qty === 1) return mediumName
      return `${qty} ${mediumName}s`
    })
    .join(", ")
}

// Helper function to determine voice status
function getVoicedStatus(voiced?: number | null) {
  if (voiced === undefined || voiced === null) return null
  return {
    className: RELEASE_ICONS.voiced[`v${voiced}` as keyof typeof RELEASE_ICONS.voiced],
    tooltip: VOICED[voiced as keyof typeof VOICED],
  }
}

export function ReleaseItem({ release }: ReleaseItemProps) {
  // Determine MTL status and build status text
  const hasMTL = release.languages?.some((lang) => lang.mtl) ?? false
  const statuses = [
    hasMTL && "machine translation",
    release.official === false && "unofficial",
    release.patch && "patch",
  ].filter(Boolean)
  const statusText = statuses.length > 0 ? `(${statuses.join(" ")})` : ""

  // Get various status indicators
  const voicedStatus = getVoicedStatus(release.voiced)
  // Fix the type safety issue with optional chaining and null coalescing
  const rtypeIcon =
    release.vns?.[0]?.rtype && RELEASE_ICONS.rtype[release.vns[0].rtype as keyof typeof RELEASE_ICONS.rtype]

  // Determine erotic content status
  const eroStatus = (() => {
    if (release.has_ero === undefined) return null
    if (!release.has_ero) return { color: "text-blue-400", tooltip: "No erotic scenes" }
    if (release.uncensored === true) return { color: "text-green-400", tooltip: "Contains uncensored erotic scenes" }
    if (release.uncensored === false)
      return { color: "text-red-400", tooltip: "Contains erotic scenes with optical censoring" }
    return { color: "text-white", tooltip: "Contains erotic scenes" }
  })()

  return (
    <TooltipProvider>
      <div className={cn("flex items-center gap-4 px-4 py-1 hover:bg-[#0F2942]/50", hasMTL && "opacity-60")}>
        {/* Release date - Always visible */}
        <div className={cn("w-24 shrink-0 text-sm", release.released === "TBA" ? "text-red-500" : "text-[#88ccff]")}>
          {release.released}
        </div>

        {/* Age rating and ero status - Hidden on small screens */}
        <div className="hidden sm:flex w-12 text-sm text-[#88ccff] items-center gap-1">
          {eroStatus && (
            <Tooltip>
              <TooltipTrigger>
                <Heart className={cn("h-3 w-3 fill-current", eroStatus.color)} />
              </TooltipTrigger>
              <TooltipContent side="top" className="bg-[#0F2942]">
                <p className="text-white">{eroStatus.tooltip}</p>
              </TooltipContent>
            </Tooltip>
          )}
          {release.minage === 0 ? "ALL" : release.minage ? `${release.minage}+` : ""}
        </div>

        {/* Platform and release type icons - Hidden on small screens */}
        <div className="hidden sm:flex w-32 gap-1">
          {rtypeIcon && (
            <Tooltip>
              <TooltipTrigger>
                <span className={rtypeIcon} />
              </TooltipTrigger>
              <TooltipContent side="top" className="bg-[#0F2942]">
                <p className="text-white">
                  {release.vns?.[0]?.rtype &&
                    `${release.vns[0].rtype.charAt(0).toUpperCase()}${release.vns[0].rtype.slice(1)} release`}
                </p>
              </TooltipContent>
            </Tooltip>
          )}
          {release.platforms?.map((platform) => {
            const platformKey = platform.toLowerCase()
            const iconClass = PLATFORM_ICONS[platformKey]
            if (!iconClass) return null
            return (
              <Tooltip key={platform}>
                <TooltipTrigger>
                  <span className={`${iconClass} inline-block`} />
                </TooltipTrigger>
                <TooltipContent side="top" className="bg-[#0F2942]">
                  <p className="text-white">{PLATFORMS[platformKey]}</p>
                </TooltipContent>
              </Tooltip>
            )
          })}
        </div>

        {/* Title and status - Always visible */}
        <div className="flex-1 min-w-0 text-sm">
          <Link
            href={`/${release.id}`}
            className="text-[#88ccff] hover:text-white transition-colors"
            aria-label={`View details for release: ${release.title}`}
          >
            <div className="truncate">
              {release.title}
              {statusText && <span className="text-[#88ccff]/80 ml-1">{statusText}</span>}
            </div>
          </Link>
        </div>

        {/* Additional information icons - Hidden on small screens */}
        <div className="hidden sm:flex items-center gap-2">
          {/* Notes icon */}
          {release.notes && (
            <Tooltip>
              <TooltipTrigger>
                <span className={RELEASE_ICONS.other.notes} />
              </TooltipTrigger>
              <TooltipContent side="left" className="max-w-sm bg-[#0F2942]">
                <p className="text-white">{release.notes}</p>
              </TooltipContent>
            </Tooltip>
          )}

          {/* Media icon */}
          {release.media && release.media.length > 0 && (
            <Tooltip>
              <TooltipTrigger>
                <span className={getMediaIcon(release.media)} />
              </TooltipTrigger>
              <TooltipContent side="left" className="bg-[#0F2942]">
                <p className="text-white">{getMediaTooltip(release.media)}</p>
              </TooltipContent>
            </Tooltip>
          )}

          {/* Freeware/Non-free icon */}
          {release.freeware !== undefined && (
            <Tooltip>
              <TooltipTrigger>
                <span className={release.freeware ? RELEASE_ICONS.other.free : RELEASE_ICONS.other.nonfree} />
              </TooltipTrigger>
              <TooltipContent side="left" className="bg-[#0F2942]">
                <p className="text-white">{release.freeware ? "Freeware" : "Non-free"}</p>
              </TooltipContent>
            </Tooltip>
          )}

          {/* Voiced icon */}
          {voicedStatus && (
            <Tooltip>
              <TooltipTrigger>
                <span className={voicedStatus.className} />
              </TooltipTrigger>
              <TooltipContent side="left" className="bg-[#0F2942]">
                <p className="text-white">{voicedStatus.tooltip}</p>
              </TooltipContent>
            </Tooltip>
          )}

          {/* External links icon */}
          {release.extlinks && release.extlinks.length > 0 && (
            <Tooltip>
              <TooltipTrigger asChild>
                <a href={release.extlinks[0].url} target="_blank" rel="noopener noreferrer" className="inline-block">
                  <span className={RELEASE_ICONS.other.external} />
                </a>
              </TooltipTrigger>
              <TooltipContent side="left" className="p-0 overflow-hidden bg-[#0F2942]">
                <div className="py-1">
                  {release.extlinks.map((link, index) => (
                    <a
                      key={index}
                      href={link.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between px-3 py-1 hover:bg-white/5 transition-colors"
                    >
                      <span className="text-white">{link.label || link.name}</span>
                      {link.id && <span className="ml-4 text-xs text-white">{link.id}</span>}
                    </a>
                  ))}
                </div>
              </TooltipContent>
            </Tooltip>
          )}
        </div>
      </div>
    </TooltipProvider>
  )
}