import { cn } from "@/lib/utils"
import { Row } from "@/components/row/Row"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { ICON } from "@/lib/icons"
import { ENUMS } from "@/lib/enums"

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

  if (titles.length === 0) return null

  const sortedTitles = [...titles].sort((a, b) => {
    if (a.main && a.official) return -1
    if (b.main && b.official) return 1
    return 0
  })

  return (
    <Row label="Titles" value={
      <div className="flex flex-col gap-1">
        {sortedTitles.map((title, index) => (
          <div key={index} className="flex gap-1 items-center">
            <Tooltip key={title.lang}>
              <TooltipTrigger asChild>
                <span className={cn(
                  ICON.LANGUAGE[title.lang as keyof typeof ICON.LANGUAGE]
                )} />
              </TooltipTrigger>
              <TooltipContent className="bg-black/50 text-white text-xs">
                {ENUMS.LANGUAGE[title.lang as keyof typeof ENUMS.LANGUAGE]}
              </TooltipContent>
            </Tooltip>
            <p className={cn(
              "break-words text-white/90",
              title.main && title.official && "font-bold"
            )}>
              {title.title}
            </p>
            {title.latin && (
              <p className={cn(
                "break-words text-white/60 text-xs"
              )}>
                ({title.latin})
              </p>
            )}
          </div>
        ))}
      </div>
    } />
  )
}