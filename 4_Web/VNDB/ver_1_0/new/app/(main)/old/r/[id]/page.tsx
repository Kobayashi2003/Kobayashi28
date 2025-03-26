"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"

import type { Release } from "@/lib/types"
import { api } from "@/lib/api"

export default function ReleasePage() {
  const params = useParams()
  const id = parseInt(params.id as string)
  
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [release, setRelease] = useState<Release | null>(null)

  useEffect(() => {
    const abortController = new AbortController()
    const fetchRelease = async () => {
      try {
        setLoading(true)
        setError(null)
        const release = await api.by_id.release(id, abortController.signal)
        setRelease(release)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchRelease()
    return () => abortController.abort()
  }, [])

  return (
    <div className="container mx-auto">
      {JSON.stringify(release)}
    </div>
  )
}