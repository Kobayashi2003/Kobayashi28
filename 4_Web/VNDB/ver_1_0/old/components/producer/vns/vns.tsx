"use client"

import { useState, useEffect } from "react"
import { Loader2 } from "lucide-react"
import { api } from "@/lib/api"
import type { VN, Producer } from "@/lib/types"
import { VnItem } from "./vn-item"

interface VNsProps {
  producer: Producer
}

export function ProducerVNs({ producer }: VNsProps) {
  const [vns, setVNs] = useState<VN[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchVns = async () => {
      if (!producer.id) {
        setError("Invalid producer ID")
        setLoading(false)
        return
      }

      try {
        setLoading(true)

        let allResults: VN[] = []
        let page = 1
        let hasMore = true

        while (hasMore) {
          const response = await api.vn("", {
            developer: producer.id,
            size: "small",
            limit: 100,
            page: page,
          })

          allResults = [...allResults, ...response.results]
          hasMore = response.more ?? false
          page++
        }

        const sortedVNs = allResults.sort((a, b) => {
          if (a.released === "TBA" && b.released === "TBA") return 0
          if (a.released === "TBA") return -1
          if (b.released === "TBA") return 1
          const dateA = a.released ? new Date(a.released).getTime() : 0
          const dateB = b.released ? new Date(b.released).getTime() : 0
          return dateB - dateA
        })

        setVNs(sortedVNs)
      } catch (err) {
        setError("Failed to fetch visual novels")
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchVns()
  }, [producer.id])

  if (loading) {
    return (
      <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
        <div className="flex justify-center items-center h-32">
          <Loader2 className="h-8 w-8 animate-spin text-white" />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden p-6">
        <div className="text-red-500">{error}</div>
      </div>
    )
  }

  if (vns.length === 0) {
    return (
      <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden p-6">
        <div className="text-white/60">No visual novels found for {producer.name}.</div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {vns.map((vn) => (
            <VnItem key={vn.id} vn={vn} />
          ))}
        </div>
      </div>
    </div>
  )
}