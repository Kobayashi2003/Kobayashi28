import { LANGUAGE_ICONS } from "@/lib/constants"

// Props for the Titles component
interface TitlesProps {
  titles?: Array<{
    lang?: string
    title?: string
    latin?: string
    official?: boolean
    main?: boolean
  }>
}

// Component to display various titles of a visual novel
export function Titles({ titles }: TitlesProps) {
  if (!titles?.length) return null

  // Sort titles to prioritize main and official titles
  const sortedTitles = [...titles].sort((a, b) => {
    if (a.main && a.official) return -1
    if (b.main && b.official) return 1
    return 0
  })

  return (
    <div className="space-y-1">
      {sortedTitles.map((title, index) => {
        const isMainAndOfficial = title.main && title.official
        return (
          <div key={index} className="flex items-start gap-2 text-sm">
            {/* Language icon */}
            <span className="w-6 text-center">
              {title.lang && <span className={LANGUAGE_ICONS[title.lang] || LANGUAGE_ICONS.en} />}
            </span>
            <div className="space-y-0.5 min-w-0">
              {/* Title in original language */}
              <div className={`break-words text-white/90 ${isMainAndOfficial ? "font-bold" : ""}`}>{title.title}</div>
              {/* Romanized title if different from original */}
              {title.latin && title.latin !== title.title && (
                <div className="text-white/60 break-words">{title.latin}</div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}