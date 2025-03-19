"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { VNDetailsPanel } from "@/components/panel/VNDetails/VNDetailsPanel"

import type { VN } from "@/lib/types"
import { api } from "@/lib/api"

export default function VNPage() {

  const params = useParams()
  const id = parseInt(params.id as string)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [vn, setVN] = useState<VN | null>(null)

  useEffect(() => {
    const fetchVN = async () => {
      try {
        const vn = await api.by_id.vn(id)
        setVN(vn)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchVN()
  }, [])

  return (
    <div className="container mx-auto">
      <VNDetailsPanel vn={vn} loading={loading} error={error} />
    </div>
  )
}