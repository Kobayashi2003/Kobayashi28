"use client"

import { cn } from "@/lib/utils"
import { useState } from "react"
import { ChevronDown } from 'lucide-react'
import type { Release } from "@/lib/types"
import { LANGUAGES, LANGUAGE_ICONS } from "@/lib/constants"
import { ReleaseItem } from "./release-item"

interface ReleaseGroupProps {
  vnid: string
  lang: string
  releases: Release[]
}

export function ReleaseGroup({ vnid, lang, releases }: ReleaseGroupProps) {
  const [isExpanded, setIsExpanded] = useState(['ja', 'zh', 'zh-Hans', 'zh-Hant'].includes(lang))
  const languageName = LANGUAGES[lang] || lang
  const iconClass = LANGUAGE_ICONS[lang] || LANGUAGE_ICONS.en

  return (
    <div>
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full bg-[#0F2942] p-2 font-bold text-[#88ccff] flex items-center justify-between group"
      >
        <div>
          <span className={iconClass}></span>
          <span className="ml-2">{languageName}</span>
        </div>
        <ChevronDown
          className={cn(
            "h-5 w-5 transition-transform duration-200",
            isExpanded ? "transform rotate-180" : "",
            "opacity-0 group-hover:opacity-100",
          )}
        />
      </button>
      {isExpanded && (
        <div className="space-y-0.5">
          {releases.map((release, index) => (
            <ReleaseItem key={`${lang}-${release.id}-${index}`} vnid={vnid} lang={lang} release={release} />
          ))}
        </div>
      )}
    </div>
  )
}