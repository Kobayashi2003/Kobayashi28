"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"

import type { Character } from "@/lib/types"
import { api } from "@/lib/api"

export default function CharacterPage() {

  const params = useParams()
  const id = parseInt(params.id as string)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [character, setCharacter] = useState<Character | null>(null)

  useEffect(() => {
    const abortController = new AbortController()
    const fetchCharacter = async () => {
      try {
        setLoading(true)
        setError(null)
        const character = await api.by_id.character(id, abortController.signal)
        setCharacter(character)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchCharacter()
    return () => abortController.abort()
  }, [])

  return (
    <div className="container mx-auto">
      {JSON.stringify(character)}
    </div>
  )
}
