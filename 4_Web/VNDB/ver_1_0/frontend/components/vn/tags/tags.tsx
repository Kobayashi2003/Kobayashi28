"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import { Group } from "./group"

interface TagsProps {
  tags: Array<{
    id?: string
    name?: string
    rating?: number
    spoiler?: number
    category?: string
  }>
}

const CATEGORIES = [
  { id: "cont", label: "content" },
  { id: "tech", label: "technical" },
  { id: "ero", label: "sexual content" },
]

const SPOILER_LEVELS = [
  { id: "hide", label: "hide spoilers", value: 0 },
  { id: "minor", label: "show minor spoilers", value: 1 },
  { id: "all", label: "spoil me!", value: 2 },
]

export function Tags({ tags }: TagsProps) {
  const [selectedCategories, setSelectedCategories] = useState<string[]>(["cont"])
  const [selectedSpoilerLevel, setSelectedSpoilerLevel] = useState<string>("hide")
  const [showLowRated, setShowLowRated] = useState(true)

  return (
    <div className="w-full max-w-5xl mx-auto space-y-4">
      <div className="bg-[#0F2942]/80 backdrop-blur-md px-4 py-1 flex items-center justify-end text-sm">
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
          {SPOILER_LEVELS.map((level) => (
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
      {selectedCategories.length > 0 ? (
        <div className="bg-[#0F2942]/80 backdrop-blur-md p-4 rounded-lg border border-white/10">
          <Group
            tags={tags}
            showLowRated={showLowRated}
            selectedCategories={selectedCategories}
            maxSpoilerLevel={SPOILER_LEVELS.find((level) => level.id === selectedSpoilerLevel)?.value || 0}
          />
        </div>
      ) : null}
    </div>
  )
}