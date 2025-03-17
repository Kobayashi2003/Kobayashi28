"use client"

import { useEffect } from "react"
import { IMGSERVE_BASE_URL } from "@/lib/constants"

export default function BGPage() {
  const bgUrl = `url(${IMGSERVE_BASE_URL}/bg)`

  useEffect(() => {
    const interval = setInterval(() => {
      window.location.reload()
    }, 1000 * 60)
    return () => clearInterval(interval)
  }, [])

  return (
    <div 
      className="min-h-screen"
      onClick={() => window.location.reload()}
      style={{ 
          backgroundImage: bgUrl, 
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
      }}
    >
    </div>
  )
}