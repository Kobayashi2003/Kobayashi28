import { cn } from "@/lib/utils"
import Link from "next/link"
import { Heart } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import type { Release } from "@/lib/types"
import { PLATFORMS, PLATFORM_ICONS, RELEASE_ICONS } from "@/lib/constants"

interface ReleaseItemProps {
  vnid: string
  lang: string
  release: Release
}

const MEDIUM_DISPLAY: Record<string, string> = {
  in: "Internet download",
  cd: "CD",
  dvd: "DVD",
  blr: "Blu-ray",
  gd: "GD",
  gdr: "GD-ROM",
  umd: "UMD",
  flp: "Floppy Disk",
  mrt: "Cartridge",
}

const VOICED_DISPLAY: Record<number, string> = {
  1: "Not voiced",
  2: "Only ero scenes voiced",
  3: "Partially voiced",
  4: "Fully voiced",
}

function getMediaIcon(medium: string) {
  const lowerMedium = medium.toLowerCase()
  if (lowerMedium === "in") return RELEASE_ICONS.download
  if (["cd", "dvd", "bd", "blr", "gdr", "umd", "flp", "gd"].includes(lowerMedium)) return RELEASE_ICONS.disk
  if (["cart", "mrt"].includes(lowerMedium)) return RELEASE_ICONS.cartridge
  return RELEASE_ICONS.disk
}

function getMediaTooltip(medium: string, qty: number) {
  const mediumName = MEDIUM_DISPLAY[medium.toLowerCase()]
  if (qty <= 1) return mediumName
  return `${qty} ${mediumName}s`
}

export function ReleaseItem({ vnid, lang, release }: ReleaseItemProps) {

  const hasEro: boolean = release.has_ero ?? false
  const isUncensored: boolean = release.uncensored ?? false
  const eroStatus = (() => {
    if (release.has_ero === undefined) return null
    if (!hasEro) return { color: "text-blue-400", tooltip: "No erotic scenes" }
    if (isUncensored) return { color: "text-green-400", tooltip: "Contains uncensored erotic scenes" }
    if (!isUncensored) return { color: "text-red-400", tooltip: "Contains erotic scenes with optical censoring" }
    return { color: "text-white", tooltip: "Contains erotic scenes" }
  })()

  const isMTL: boolean = release.languages?.find((l) => l.lang === lang)?.mtl ?? false
  const isOfficial: boolean = release.official ?? false
  const isPatch: boolean = release.patch ?? false
  const extStatus = [
    isMTL && "machine translation",
    !isOfficial && "unofficial",
    isPatch && "patch",
  ].filter(Boolean)
  const extStatusText = extStatus.length > 0 ? `(${extStatus.join(" ")})` : ""

  const rtype: string = release.vns?.find((vn) => vn.id === vnid)?.rtype ?? ""
  const rtypeIcon = rtype && RELEASE_ICONS[rtype]

  const voiced: number = release.voiced ?? 0
  const voicedStatus = (() => {
    if (release.voiced === undefined) return null
    return { classname: RELEASE_ICONS[`v${voiced}`], tooltip: VOICED_DISPLAY[voiced] }
  })()

  return (
    <TooltipProvider>
      <div className={cn("flex items-center gap-4 px-4 py-1 hover:bg-[#0F2942]/50", (isMTL || !isOfficial) && "opacity-60")}>

        {/* Release date */}
        <div className={cn("w-24 shrink-0 text-sm", release.released === "TBA" ? "text-red-500" : "text-[#88ccff]")}>
          {release.released}
        </div>

        {/* Age rating and ero status */}
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

        {/* Platform and release type icons */}
        <div className="hidden sm:flex w-32 gap-1">
          {rtypeIcon && (
            <Tooltip>
              <TooltipTrigger>
                <span className={rtypeIcon} />
              </TooltipTrigger>
              <TooltipContent side="top" className="bg-[#0F2942]">
                <p className="text-white">
                  {rtype && `${rtype.charAt(0).toUpperCase()}${rtype.slice(1)} release`}
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

        {/* Title and extral status */}
        <div className="flex-1 min-w-0 text-sm">
          <Link
            href={`/${release.id}`}
            className="text-[#88ccff] hover:text-white transition-colors"
            aria-label={`View details for release: ${release.title}`}
          >
            <div className="truncate">
              {release.title}
              {extStatusText && <span className="text-[#88ccff]/80 ml-1">{extStatusText}</span>}
            </div>
          </Link>
        </div>

        {/* Additional information icons */}
        <div className="hidden sm:flex items-center gap-2">

          {/* Notes icon */}
          {release.notes && (
            <Tooltip>
              <TooltipTrigger>
                <span className={RELEASE_ICONS.notes} />
              </TooltipTrigger>
              <TooltipContent side="left" className="max-w-sm bg-[#0F2942]">
                <p className="text-white">{release.notes}</p>
              </TooltipContent>
            </Tooltip>
          )}

          {/* Media icons */}
          {release.media?.map((mediaItem, index) => (
            <Tooltip key={`${mediaItem.medium}-${index}`}>
              <TooltipTrigger>
                <span className={getMediaIcon(mediaItem.medium || "")} />
              </TooltipTrigger>
              <TooltipContent side="left" className="bg-[#0F2942]">
                <p className="text-white">{getMediaTooltip(mediaItem.medium ?? "", mediaItem.qty ?? 0)}</p>
              </TooltipContent>
            </Tooltip>
          ))}

          {/* Freeware/Non-free icon */}
          {release.freeware !== undefined && (
            <Tooltip>
              <TooltipTrigger>
                <span className={release.freeware ? RELEASE_ICONS.free : RELEASE_ICONS.nonfree} />
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
                <span className={voicedStatus.classname} />
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
                  <span className={RELEASE_ICONS.external} />
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
                      {/* {link.id && <span className="ml-4 text-xs text-white">{link.id}</span>} */}
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