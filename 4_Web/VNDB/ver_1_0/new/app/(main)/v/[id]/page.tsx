"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { VNDetailsPanel } from "@/components/panel/VNDetails/VNDetailsPanel"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"

import type { VN } from "@/lib/types"
import { api } from "@/lib/api"

export default function VNPage() {

  const params = useParams()
  const id = parseInt(params.id as string)

  const [loadingVN, setLoadingVN] = useState(true)
  const [errorVN, setErrorVN] = useState<string | null>(null)
  const [vn, setVN] = useState<VN | null>(null)

  useEffect(() => {
    const fetchVN = async () => {
      try {
        const vn = await api.by_id.vn(id)
        setVN(vn)
      } catch (error) {
        setErrorVN(error as string)
      } finally {
        setLoadingVN(false)
      }
    }
    fetchVN()
  }, [])

  return (
    <>
      {loadingVN ? (
        <Loading message="Loading VN..." />
      ) : errorVN ? (
        <Error message="Error loading VN" />
      ) : !vn ? (
        <NotFound message="VN not found" />
      ) : (
        <VNDetailsPanel vn={vn} />
      )}
    </>
  )
}