"use client"

import { cn } from "@/lib/utils"
import { HeaderNavi } from "./HeaderNavi"
import { UserHeader } from "./UserHeader"
import { SearchHeader } from "./SearchHeader"

interface HeaderBarProps {
  hidden?: boolean
  className?: string
}

export function HeaderBar({ hidden = false, className }: HeaderBarProps) {

  return (
    <header className={cn("px-4 border-b border-white/10", className)}>
      <div className="flex flex-wrap items-center py-4 gap-2">
        <HeaderNavi className="order-1" />
        <UserHeader hidden={hidden} className="order-3 md:order-3 ml-auto md:ml-0" />
        <SearchHeader hidden={hidden} className="order-4 md:order-2 w-full md:w-auto md:mx-auto" />
      </div>
    </header>
  )
}