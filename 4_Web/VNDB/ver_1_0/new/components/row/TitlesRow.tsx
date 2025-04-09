import { cn } from "@/lib/utils"
import { ICON } from "@/lib/icons"

interface Title {
  lang: string
  title: string
  latin?: string
  official?: boolean
  main?: boolean
}

interface TitlesRowProps {
  titles: Title[]
}

export function TitlesRow({ titles }: TitlesRowProps) {

  if (!titles.length) return null

  const sortedTitles = [...titles].sort((a, b) => {
    if (a.main && a.official) return -1
    if (b.main && b.official) return 1
    return 0
  })

  return (
    <div className="w-full flex flex-col gap-2">
      <h3 className="text-sm text-white/60">Titles</h3>
      <div className="w-full">
        {sortedTitles.map((title, index) => {
          const isMainAndOfficial = title.main && title.official
          return (
            <div key={index} className="flex gap-1">
              <span className={cn(
                ICON.LANGUAGE[title.lang as keyof typeof ICON.LANGUAGE]
              )}/>
              <div>
                <p className={cn(
                  "break-words text-white/90",
                  isMainAndOfficial && "font-bold"
                )}>{title.title}</p>
                {title.latin && title.latin !== title.title && (
                  <p className="text-white/60 break-words">{title.latin}</p>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}