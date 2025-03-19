"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"

import type { Staff } from "@/lib/types"
import { api } from "@/lib/api"

export default function StaffPage() {
  const params = useParams()
  const id = parseInt(params.id as string)
  
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [staff, setStaff] = useState<Staff | null>(null)

  useEffect(() => {
    const fetchStaff = async () => {
      try {
        const staff = await api.by_id.staff(id)
        setStaff(staff)
      } catch (error) {
        setError(error as string)
      } finally {
        setLoading(false)
      }
    }
    fetchStaff()
  }, [])
  
  return (
    <div className="container mx-auto">
      {JSON.stringify(staff)}
    </div>
  )
}