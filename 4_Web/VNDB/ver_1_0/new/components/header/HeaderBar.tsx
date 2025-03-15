"use client"

import { HeaderNavi } from "./HeaderNavi"
import { UserHeader } from "./user/UserHeader"
import { SearchHeader } from "./search/SearchHeader"

interface HeaderBarProps {
  className?: string
}

export function HeaderBar({ className }: HeaderBarProps) {
  return (
      <header className={`px-4 border-b border-white/10 ${className}`}>
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