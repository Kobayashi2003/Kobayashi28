"use client"

import { useRef, useEffect, useState } from "react"
import { useOnScroll } from "@/hooks/useOnScroll"
import { HeaderBar } from "@/components/header/HeaderBar"
import { UserProvider } from "@/context/UserContext"
import { SearchProvider } from "@/context/SearchContext"
import { IMGSERVE_BASE_URL } from "@/lib/constants"

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const bgUrl = `url(${IMGSERVE_BASE_URL}/bg)`

  const { trigger } = useOnScroll({
    scrollThreshold: 30,
    throttleTime: 150,
    debounceTime: 200
  })

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
            className={
              `fixed top-0 left-0 right-0
              bg-[#0A1929]/80 backdrop-blur-sm 
              transition-opacity duration-300
              ${trigger ? "opacity-0 z-[-1]" : "opacity-100 z-50"}`
            }
          >
            <HeaderBar />
          </div>
          <div style={{ height: `${headerHeight}px` }} />
          {children}
        </UserProvider>
        </SearchProvider>
      </div>
    </div>
  )
}