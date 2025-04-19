"use client"

import { useRef, useEffect, useState } from "react"
import { useOnScroll } from "@/hooks/useOnScroll"
import { UserProvider } from "@/context/UserContext"
import { SearchProvider } from "@/context/SearchContext"
import { IMGSERVE_BASE_URL } from "@/lib/constants"

import { cn } from "@/lib/utils"
import { HeaderBar } from "@/components/header/HeaderBar"

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const bgUrl = `url(${IMGSERVE_BASE_URL}/bg)`

  const { trigger } = useOnScroll({
    scrollThreshold: 30,
    throttleTime: 150,
    debounceTime: 200
  })

  const [mounted, setMounted] = useState(false)

  const headerRef = useRef<HTMLDivElement>(null)
  const [headerHeight, setHeaderHeight] = useState(0)

  useEffect(() => {
    const header = headerRef.current
    if (!header) return

    setHeaderHeight(header.offsetHeight)

    const observer = new ResizeObserver((entries) => {
      setHeaderHeight(entries[0].target.clientHeight)
    })

    observer.observe(header)
    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    setMounted(true)
    return () => setMounted(false)
  }, [])

  return (
    <div style={{ 
        backgroundImage: bgUrl, 
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed',
      }}>
      <div className="min-h-screen bg-[#0A1929]/80 text-white">
        <SearchProvider>
        <UserProvider>
          <div
            ref={headerRef}
            className={cn(
              "fixed top-0 left-0 right-0",
              "bg-[#0A1929]/80",
              "backdrop-blur-sm",
              "transition-opacity duration-300",
              trigger ? "opacity-0 z-[-1]" : "opacity-100 z-1",
              !mounted && "hidden"
            )}
          >
            <HeaderBar hidden={trigger} />
          </div>
          <div 
            style={{
              height: `${headerHeight}px`
            }} 
            className={cn(
              !mounted && "hidden"
            )}
          />
          {children}
        </UserProvider>
        </SearchProvider>
      </div>
    </div>
  )
}