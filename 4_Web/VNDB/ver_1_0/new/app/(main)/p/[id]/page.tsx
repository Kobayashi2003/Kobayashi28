"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"

import type { Producer } from "@/lib/types"
import { api } from "@/lib/api"

export default function ProducerPage() {
  const params = useParams()
  const id = parseInt(params.id as string)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [producer, setProducer] = useState<Producer | null>(null)

  useEffect(() => {
    const fetchProducer = async () => {
      try {
        const producer = await api.by_id.producer(id)
        setProducer(producer)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchProducer()
  }, [])

  return (
    <div className="container mx-auto">
      {JSON.stringify(producer)}
    </div>
  )
}
