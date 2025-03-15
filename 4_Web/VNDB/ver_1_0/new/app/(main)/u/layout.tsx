"use client"

import { useEffect, useState } from "react"
import { useRouter, usePathname } from "next/navigation"
import { NavBar } from "@/components/common/NavBar"

export default function UserLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()

  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const options = [
    {
      key: "info",
      label: "Info",
      value: "/u/i",
      onClick: () => { router.push("/u/i") }
    },
    {
      key: "categories",
      label: "Categories",
      value: "/u/c",
      onClick: () => { router.push("/u/c") }
    },
    {
      key: "ranking",
      label: "Ranking",
      value: "/u/r",
      onClick: () => { router.push("/u/r") }
    }
  ]

  return (
    <div className="flex flex-row">
      <NavBar 
        options={options} 
        selectedValue={pathname} 
        position="left" 
        className={`flex-1/9 ${mounted ? "opacity-100" : "opacity-0"} transition-opacity duration-500`}
      />
      <div className="flex-8/9">
        {children}
      </div>
    </div>
  )
}
