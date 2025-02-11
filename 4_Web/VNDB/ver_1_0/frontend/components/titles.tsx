"use client"

import * as Collapsible from "@radix-ui/react-collapsible"
import { ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"
import { useState } from "react"
import { LANG_FLAGS } from "@/lib/constants"

interface TitlesProps {
  titles?: Array<{
    lang?: string
    title?: string
    latin?: string
    official?: boolean
    main?: boolean
  }>
  mainTitle?: string
}

export function Titles({ titles, mainTitle }: TitlesProps) {
  const [isOpen, setIsOpen] = useState(false)

  if (!titles?.length) return null

  // Find the main official title to display by default
  const defaultTitle = titles.find((t) => t.official && t.main) || titles[0]

  return (
    <Collapsible.Root open={isOpen} onOpenChange={setIsOpen}>
      <Collapsible.Trigger className="flex items-center gap-2 w-full text-sm text-white/90 hover:text-white">
        <ChevronDown className={cn("h-4 w-4 transition-transform", isOpen && "transform rotate-180")} />
        <span>Titles</span>
      </Collapsible.Trigger>
      <Collapsible.Content className="pt-2">
        <div className="space-y-1 pl-6">
          {titles.map((title, index) => (
            <div key={index} className="flex items-start gap-2 text-sm">
              <span className="w-6 text-center" title={title.lang && LANG_FLAGS[title.lang]?.name}>
                {title.lang && LANG_FLAGS[title.lang]?.flag}
              </span>
              <div className="space-y-0.5 min-w-0">
                <div
                  className={cn("break-words", title.official && "text-white/90", !title.official && "text-white/60")}
                >
                  {title.title}
                  {title.main && title.official && " (Main)"}
                </div>
                {title.latin && title.latin !== title.title && (
                  <div className="text-white/60 break-words">{title.latin}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      </Collapsible.Content>
    </Collapsible.Root>
  )
}