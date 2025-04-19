"use client"

import { useState, useEffect } from "react"
import Image from "next/image"

interface Image2Props {
  url: string
  dims?: [number, number]
  thumbnail?: string
  thumbnail_dims?: [number, number]
}

export function Image2({ url, dims, thumbnail, thumbnail_dims }: Image2Props) {

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(false)
  }, [url, thumbnail])

  const handleRetry = () => {
    // TODO: Implement retry
  }

  return (
    <></>
  )
}