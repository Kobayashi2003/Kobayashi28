"use client"

import { useEffect, useState, useCallback } from "react"
import { api } from "@/lib/api"
import type { Release } from "@/lib/types"
import { ReleaseGroup } from "./group"

interface ReleasesProps {
  releaseIds?: string[]
}

export function Releases({ releaseIds }: ReleasesProps) {
  const [releases, setReleases] = useState<Release[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const fetchRelease = useCallback(async (id: string) => {
    try {
      const response = await api.release(id, { size: "large" })
      return response?.results?.[0] || null
    } catch (error) {
      console.error(`Error fetching release ${id}:`, error)
      return null
    }
  }, [])

  useEffect(() => {
    if (!releaseIds?.length) {
      setIsLoading(false)
      return
    }

    setIsLoading(true)
    setReleases([])

    const fetchReleases = async () => {
      const newReleases = await Promise.all(
        releaseIds.map(async (id) => {
          const release = await fetchRelease(id)
          return release
        })
      )
      setReleases(newReleases.filter((r): r is Release => r !== null))
      setIsLoading(false)
    }

    fetchReleases()
  }, [releaseIds, fetchRelease])

  // Group releases by language
  const groupedReleases = releases.reduce((groups, release) => {
    const mainLanguage = release.languages?.find((l) => l.main)?.lang || "other"
    if (!groups[mainLanguage]) {
      groups[mainLanguage] = []
    }
    groups[mainLanguage].push(release)
    return groups
  }, {} as Record<string, Release[]>)

  if (isLoading && releases.length === 0) {
    return <div>Loading releases...</div>
  }

  return (
    <div className="space-y-4">
      {Object.entries(groupedReleases).map(([lang, releases]) => (
        <ReleaseGroup key={`${lang}-group`} lang={lang} releases={releases} />
      ))}
      {isLoading && releases.length > 0 && <div>Loading more releases...</div>}
    </div>
  )
}