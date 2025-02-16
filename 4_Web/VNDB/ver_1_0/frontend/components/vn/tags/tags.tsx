"use client"

import { Fragment, useState } from "react"
import { cn } from "@/lib/utils"
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"
import type { VN } from "@/lib/types"
import { TagItem } from "./tag-item"

interface TagsProps {
  vn: VN
}

const CATEGORIES_DISPLAY = [
  { id: "cont", label: "content" },
  { id: "tech", label: "technical" },
  { id: "ero", label: "sexual content" },
]

export function VNTags({ vn }: TagsProps) {
  const [selectedCategories, setSelectedCategories] = useState<string[]>(["cont"])
  const [spoilerLevel, setSpoilerLevel] = useState(0)
  const [showLowRated] = useState(true)

  // Filter and sort tags
  const filteredTags = (vn.tags || [])
    .filter((tag) => {
      if (!showLowRated && (tag.rating || 0) < 1) return false
      if ((tag.spoiler || 0) > spoilerLevel) return false
      if (selectedCategories.length > 0 && tag.category && !selectedCategories.includes(tag.category)) return false
      return true
    })
    .sort((a, b) => (b.rating || 0) - (a.rating || 0))

  return (
    <div className="w-full max-w-5xl mx-auto space-y-4">

      {/* Scrollable area for category and spoiler level selection */}
      <ScrollArea className="w-full">
        {/* Container for buttons with semi-transparent background */}
        <div className="bg-[#0F2942]/80 backdrop-blur-md px-4 py-1 flex items-center justify-end text-xs sm:text-sm whitespace-nowrap min-w-full">
          {/* Category selection buttons */}
          <div className="flex items-center">
            {CATEGORIES_DISPLAY.map((category) => (
              <button
                key={category.id}
                className={cn(
                  "px-2 py-1 transition-colors",
                  // Highlight selected categories
                  selectedCategories.includes(category.id) ? "text-[#88ccff]" : "text-white/60 hover:text-white",
                )}
                onClick={() => {
                  setSelectedCategories((prev) =>
                    // Toggle category selection
                    prev.includes(category.id) ? prev.filter((c) => c !== category.id) : [...prev, category.id],
                  )
                }}
              >
                {category.label}
              </button>
            ))}
          </div>

          {/* Separator between category and spoiler level buttons */}
          <span className="text-white/20 px-2">|</span>

          {/* Spoiler level selection buttons */}
          <div className="flex items-center gap-2 text-sm">
            {[
              { level: 0, text: "Hide spoilers", color: "text-[#88ccff]" },
              { level: 1, text: "Show minor spoilers", color: "text-[#ffcc66]" },
              { level: 2, text: "Spoil me!", color: "text-[#ff6666]" },
            ].map((button, index) => (
              <Fragment key={button.level}>
                {/* Add separator between spoiler level buttons */}
                {index > 0 && <span className="text-white/20">|</span>}
                <button
                  onClick={() => setSpoilerLevel(button.level)}
                  className={cn(
                    "transition-colors",
                    spoilerLevel === button.level ? button.color : "text-white/60 hover:text-white",
                  )}
                >
                  {button.text}
                </button>
              </Fragment>
            ))}
          </div>
        </div>
        {/* Horizontal scroll bar for overflow content */}
        <ScrollBar orientation="horizontal" className="bg-[#0F2942]/40" />
      </ScrollArea>

      {selectedCategories.length > 0 && filteredTags.length > 0 && (
        <div className="bg-[#0F2942]/80 backdrop-blur-md p-4 rounded-lg border border-white/10">
          <div className="flex flex-wrap items-center">
            {filteredTags.map((tag, index) => (
              <Fragment key={tag.id}>
                <TagItem tag={tag} rating={tag.rating || 0} spoiler={tag.spoiler || 0} />
                {index < filteredTags.length - 1 && <span className="text-[#88ccff] mx-2 opacity-50">·</span>}
              </Fragment>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}