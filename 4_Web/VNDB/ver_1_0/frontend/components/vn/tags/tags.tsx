"use client"

import { useState } from "react"
import { TagGroup } from "./tag-group"
import { cn } from "@/lib/utils"
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"
import { CATEGORIES, SPOILER } from "@/lib/constants"

// Props for the Tags component
interface TagsProps {
  tags: Array<{
    id?: string
    name?: string
    rating?: number
    spoiler?: number
    category?: string
  }>
}

// Main component for displaying and filtering tags
export function Tags({ tags }: TagsProps) {
  // State for selected categories, spoiler level, and low-rated tag visibility
  const [selectedCategories, setSelectedCategories] = useState<string[]>(["cont"])
  const [selectedSpoilerLevel, setSelectedSpoilerLevel] = useState<string>("hide")
  const [showLowRated] = useState(true) // This state is not currently used, but kept for potential future use

  return (
    <div className="w-full max-w-5xl mx-auto space-y-4">
      <ScrollArea className="w-full">
        <div className="bg-[#0F2942]/80 backdrop-blur-md px-4 py-1 flex items-center justify-end text-xs sm:text-sm whitespace-nowrap min-w-full">
          <div className="flex items-center">
            {CATEGORIES.map((category) => (
              <button
                key={category.id}
                className={cn(
                  "px-2 py-1 transition-colors",
                  selectedCategories.includes(category.id) ? "text-[#88ccff]" : "text-white/60 hover:text-white",
                )}
                onClick={() => {
                  setSelectedCategories((prev) =>
                    prev.includes(category.id) ? prev.filter((c) => c !== category.id) : [...prev, category.id],
                  )
                }}
              >
                {category.label}
              </button>
            ))}
          </div>
          <span className="text-white/20 px-2">|</span>
          <div className="flex items-center">
            {SPOILER.map((level) => (
              <button
                key={level.id}
                className={cn(
                  "px-2 py-1 transition-colors",
                  selectedSpoilerLevel === level.id ? "text-[#88ccff]" : "text-white/60 hover:text-white",
                )}
                onClick={() => setSelectedSpoilerLevel(level.id)}
              >
                {level.label}
              </button>
            ))}
          </div>
        </div>
        <ScrollBar orientation="horizontal" className="bg-[#0F2942]/40" />
      </ScrollArea>
      {selectedCategories.length > 0 ? (
        <div className="bg-[#0F2942]/80 backdrop-blur-md p-4 rounded-lg border border-white/10">
          <TagGroup
            tags={tags}
            showLowRated={showLowRated}
            selectedCategories={selectedCategories}
            maxSpoilerLevel={SPOILER.find((level) => level.id === selectedSpoilerLevel)?.value || 0}
          />
        </div>
      ) : null}
    </div>
  )
}