"use client"

import { useEffect, useState } from "react"
import { cn } from "@/lib/utils"
import { HeaderNavi } from "./HeaderNavi"
import { UserHeader } from "./user/UserHeader"
import { SearchHeader } from "./search/SearchHeader"

interface HeaderBarProps {
  className?: string
}

export function HeaderBar({ className }: HeaderBarProps) {

  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  return (
      <header className={cn("px-4 border-b border-white/10", className, !mounted && "opacity-0", "transition-opacity duration-300")}>
        <div className="flex flex-col justify-center items-between py-4 gap-1">
          <div className="flex flex-row justify-between items-center gap-2">
            <HeaderNavi />
            <SearchHeader className="hidden md:flex" />
            <UserHeader />
          </div>
          <SearchHeader className="flex md:hidden" />
        </div>
      </header>
  )
}