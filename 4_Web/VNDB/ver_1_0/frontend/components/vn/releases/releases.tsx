"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import type { Release } from "@/lib/types"
import { ReleaseGroup } from "./release-group"

interface ReleasesProps {
  releaseIds?: string[]
}

export function Releases({ releaseIds }: ReleasesProps) {
  const [releases, setReleases] = useState<Release[]>([])

  useEffect(() => {
    async function fetchReleases() {
      if (!releaseIds) return

      const fetchedReleases = await Promise.all(
        releaseIds.map((id) => api.release(id, { size: "large" }).then((res) => res.results[0])),
      )
      setReleases(fetchedReleases)
    }

    fetchReleases()
  }, [releaseIds])

  if (!releases.length) return null

  // Group releases by language and sort within each group
  const groupedReleases = releases.reduce(
    (groups, release) => {
      const mainLanguage = release.languages?.find((l) => l.main)?.lang || "other"
      if (!groups[mainLanguage]) {
        groups[mainLanguage] = []
      }
      groups[mainLanguage].push(release)
      return groups
    },
    {} as Record<string, Release[]>,
  )

  // Sort releases within each language group
  Object.keys(groupedReleases).forEach((lang) => {
    groupedReleases[lang].sort((a, b) => {
      // First, compare by release date
      if (a.released && b.released) {
        const dateComparison = new Date(b.released).getTime() - new Date(a.released).getTime()
        if (dateComparison !== 0) return dateComparison
      } else if (a.released) return -1
      else if (b.released) return 1

      // If release dates are the same or not available, compare by platforms
      const aPlatforms = a.platforms?.join(",") || ""
      const bPlatforms = b.platforms?.join(",") || ""
      if (aPlatforms !== bPlatforms) return aPlatforms.localeCompare(bPlatforms)

      // If platforms are the same, compare by title
      return (a.title || "").localeCompare(b.title || "")
    })
  })

  return (
    <div className="space-y-4">
      {Object.entries(groupedReleases).map(([lang, releases]) => (
        <ReleaseGroup key={lang} lang={lang} releases={releases} />
      ))}
    </div>
  )
}