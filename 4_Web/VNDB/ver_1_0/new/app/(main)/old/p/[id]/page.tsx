"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"

import type { Producer } from "@/lib/types"
import { api } from "@/lib/api"

export default function ProducerPage() {
  const params = useParams()
  const id = parseInt(params.id as string)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [producer, setProducer] = useState<Producer | null>(null)

  useEffect(() => {
    const abortController = new AbortController()
    const fetchProducer = async () => {
      try {
        setLoading(true)
        setError(null)
        const producer = await api.by_id.producer(id, abortController.signal)
        setProducer(producer)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchProducer()
    return () => abortController.abort()
  }, [])

  return (
    <div className="container mx-auto">
      {JSON.stringify(producer)}
    </div>
  )
}
