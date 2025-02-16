"use client"

import { useState, useEffect } from "react"
import { Loader2 } from "lucide-react"
import { api } from "@/lib/api"
import type { VN, Staff } from "@/lib/types"
import { CreditItem } from "./credit-item"

interface CreditsProps {
  staff: Staff
}

export function StaffCredits({ staff }: CreditsProps) {
  const [credits, setCredits] = useState<VN[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCredits = async () => {
      if (!staff.id) {
        setError("Invalid staff ID")
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        const response = await api.vn("", { staff: staff.id, size: "small" })
        setCredits(response.results)
      } catch (err) {
        setError("Failed to fetch visual novels")
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchCredits()
  }, [staff.id])

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

  if (credits.length === 0) {
    return (
      <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden p-6">
        <div className="text-white/60">No visual novels found for {staff.name}.</div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {credits.map((vn) => (
            <CreditItem key={vn.id} vn={vn} />
          ))}
        </div>
      </div>
    </div>
  )
}