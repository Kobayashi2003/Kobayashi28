"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"

import type { Tag } from "@/lib/types"
import { api } from "@/lib/api"
import { error } from "console"

export default function TagPage() {
  const params = useParams()
  const id = parseInt(params.id as string)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tag, setTag] = useState<Tag | null>(null)

  useEffect(() => {
    const fetchTag = async () => {
      try {
        const tag = await api.by_id.tag(id)
        setTag(tag)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchTag()
  }, [])

  return (
    <div className="container mx-auto">
      {JSON.stringify(tag)}
    </div>
  )
}

