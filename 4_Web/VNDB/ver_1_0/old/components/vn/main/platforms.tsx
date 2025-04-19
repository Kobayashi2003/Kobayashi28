import { PLATFORM_ICONS, PLATFORMS } from "@/lib/constants"

// Props for the Platforms component
interface PlatformsProps {
  platforms?: string[]
}

// Component to display platform icons
export function Platforms({ platforms }: PlatformsProps) {
  if (!platforms || platforms.length === 0) return null

  return (
    <div className="flex flex-wrap gap-2">
      {platforms.map((platform) => {
        const platformKey = platform.toLowerCase()
        const iconClass = PLATFORM_ICONS[platformKey]
        if (!iconClass) return null
        // Display platform icon with tooltip
        return <span key={platform} className={`${iconClass} inline-block`} title={PLATFORMS[platformKey]} />
      })}
    </div>
  )
}