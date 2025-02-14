"use client"

import { cn } from "@/lib/utils"
import { useState } from "react"
import type { VN } from "@/lib/types"
import { ScreenshotGroup } from "./screenshot-group"

interface ScreenshotsProps {
  vn: VN
}

type FilterOption = "safe" | "suggestive" | "explicit"

export function Screenshots({ vn }: ScreenshotsProps) {
  const [filterOption, setFilterOption] = useState<FilterOption>("safe")

  // Filter function
  const filterScreenshots = (screenshots: NonNullable<VN["screenshots"]>) => {
    return screenshots.filter((screenshot) => {
      const sexual = screenshot.sexual || 0
      const violence = screenshot.violence || 0

      switch (filterOption) {
        case "safe":
          return sexual < 0.5 && violence < 0.5
        case "suggestive":
          return sexual < 1 && violence < 1
        case "explicit":
          return true
      }
    })
  }

  // Group screenshots by release
  const screenshotsByRelease = vn.screenshots?.reduce((acc, screenshot) => {
    const releaseId = screenshot.release?.id || "Unknown"
    if (!acc.has(releaseId)) {
      acc.set(releaseId, [])
    }
    acc.get(releaseId)!.push(screenshot)
    return acc
  }, new Map<string, typeof vn.screenshots>())

  if (!screenshotsByRelease) return null

  // Calculate counts once for all screenshots
  const counts = {
    safe: 0,
    suggestive: 0,
    explicit: 0,
  }

  Array.from(screenshotsByRelease.values()).forEach((screenshots) => {
    screenshots?.forEach((screenshot) => {
      const sexual = screenshot.sexual || 0
      const violence = screenshot.violence || 0

      if (sexual < 0.5 && violence < 0.5) {
        counts.safe++
      } else if (sexual < 1 && violence < 1) {
        counts.suggestive++
      } else {
        counts.explicit++
      }
    })
  })

  return (
    <div className="space-y-4">
      <div className="flex gap-4 px-4 text-sm justify-end">
        {[
          { key: "safe", label: "Safe", activeColor: "text-[#88ccff]" },
          { key: "suggestive", label: "Suggestive", activeColor: "text-[#ffcc66]" },
          { key: "explicit", label: "Explicit", activeColor: "text-[#ff6666]" },
        ].map(({ key, label, activeColor }) => (
          <button
            key={key}
            onClick={() => setFilterOption(key as FilterOption)}
            className={cn("transition-colors", filterOption === key ? activeColor : "text-white/60 hover:text-white")}
          >
            {label} ({counts[key as keyof typeof counts]})
          </button>
        ))}
      </div>
      {Array.from(screenshotsByRelease.entries()).map(([releaseId, screenshots]) => {
        const release = vn.releases?.find((r) => r.id === releaseId)
        const filteredScreenshots = filterScreenshots(screenshots || [])

        if (filteredScreenshots.length === 0) return null

        return (
          <ScreenshotGroup
            key={releaseId}
            releaseId={releaseId}
            title={release?.title || "Unknown Release"}
            screenshots={filteredScreenshots}
          />
        )
      })}
    </div>
  )
}