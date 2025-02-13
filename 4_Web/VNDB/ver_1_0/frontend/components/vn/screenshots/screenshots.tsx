import type { VN } from "@/lib/types"
import { ScreenshotGroup } from "./screenshot-group"

interface ScreenshotsProps {
  vn: VN
}

export function Screenshots({ vn }: ScreenshotsProps) {
  // Group screenshots by release
  const screenshotsByRelease = vn.screenshots?.reduce((acc, screenshot) => {
    const releaseId = screenshot.release?.id || "unknown"
    if (!acc.has(releaseId)) {
      acc.set(releaseId, [])
    }
    acc.get(releaseId)!.push(screenshot)
    return acc
  }, new Map<string, typeof vn.screenshots>())

  if (!screenshotsByRelease) return null

  return (
    <div className="space-y-4">
      {Array.from(screenshotsByRelease.entries()).map(([releaseId, screenshots]) => {
        const release = vn.releases?.find((r) => r.id === releaseId)
        return (
          <ScreenshotGroup
            key={releaseId}
            releaseId={releaseId}
            title={release?.title || "Unknown Release"}
            screenshots={screenshots}
          />
        )
      })}
    </div>
  )
}