"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import type { Release, VN } from "@/lib/types"
import { ReleaseGroup } from "./release-group"

interface ReleasesProps {
  vn : VN
}

export function VNReleases({ vn }: ReleasesProps) {

  const [releases, setReleases] = useState<Release[]>([])

  useEffect(() => {
    async function fetchReleases() {
      const releaseIds =
      vn.releases
        ?.map((release) => release.id)
        .filter((id): id is string => id !== null)
        .map((id) => id.slice(1)) || []
      if (!releaseIds) return

      const fetchedReleases = await Promise.all(
        releaseIds.map((id) => api.release(id, { size: "large" }).then((res) => res.results[0])),
      )
      setReleases(fetchedReleases)
    }
    fetchReleases()
  }, [vn])

  if (!releases.length) return null

  // Group releases by language and sort within each group
  const groupedReleases = releases.reduce(
    (groups, release) => {
      release.languages?.forEach((language) => {
        const lang = language.lang || "unknown"
        if (!groups[lang]) {
          groups[lang] = []
        }
        groups[lang].push(release)
      })
      return groups
    },
    {} as Record<string, Release[]>,
  )

  // Sort platforms for each release
  Object.values(groupedReleases).flat().forEach((release) => {
    if (release.platforms)   {
      release.platforms.sort()
    }
  })

  // Sort releases for each group by released, platforms and title
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
        <ReleaseGroup key={lang} vnid={vn.id || ""} lang={lang} releases={releases} />
      ))}
    </div>
  )
}