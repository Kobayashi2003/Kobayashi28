"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"

import type { Trait } from "@/lib/types"
import { api } from "@/lib/api"

export default function TraitPage() {
  const params = useParams()
  const id = parseInt(params.id as string)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [trait, setTrait] = useState<Trait | null>(null)

  useEffect(() => {
    const abortController = new AbortController()
    const fetchTrait = async () => {
      try {
        setLoading(true)
        setError(null)
        const trait = await api.by_id.trait(id, abortController.signal)
        setTrait(trait)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchTrait()
    return () => abortController.abort()
  }, [])

  return (
    <div className="container mx-auto">
      {JSON.stringify(trait)}
    </div>
  )
}