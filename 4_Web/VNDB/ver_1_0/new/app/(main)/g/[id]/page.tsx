"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"

import type { Tag } from "@/lib/types"
import { api } from "@/lib/api"
import { error } from "console"

export default function TagPage() {
  const params = useParams()
  const id = parseInt(params.id as string)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [tag, setTag] = useState<Tag | null>(null)


  useEffect(() => {
    const abortController = new AbortController()
    const fetchTag = async () => {
      try {
        setLoading(true)
        setError(null)
        const tag = await api.by_id.tag(id, abortController.signal)
        setTag(tag)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchTag()
    return () => abortController.abort()
  }, [])

  return (
    <div className="container mx-auto">
      {JSON.stringify(tag)}
    </div>
  )
}

