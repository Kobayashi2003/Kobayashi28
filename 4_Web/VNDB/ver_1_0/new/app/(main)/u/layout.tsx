"use client"

import { useEffect, useState, useRef } from "react"
import { useRouter, usePathname } from "next/navigation"
import { useUserContext } from "@/context/UserContext"

import { cn } from "@/lib/utils"
import { NavBar } from "@/components/common/NavBar"
import { useHideOnScroll } from "@/hooks/useHideOnScroll"

export default function UserLayout({ children }: { children: React.ReactNode }) {

  const { user, isLoading } = useUserContext()
  const [mounted, setMounted] = useState(false)
  const router = useRouter()
  const pathname = usePathname()
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

  const { hidden } = useHideOnScroll({
    scrollThreshold: 50,
    throttleTime: 100
  })

  const navBarRef = useRef<HTMLDivElement>(null)
  const [navBarWidth, setNavBarWidth] = useState(0)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/")
    }
  }, [isLoading, user, router])

  useEffect(() => {
    const width = navBarRef.current
    if (!width) return

    setNavBarWidth(width.offsetWidth)

    const observer = new ResizeObserver((entries) => {
      setNavBarWidth(entries[0].target.clientWidth)
    })

    observer.observe(width)
    return () => observer.disconnect()
  }, [])

  return (
    <div className="flex flex-row">
      <div
        ref={navBarRef}
        className={cn(
          "fixed left-0 z-50 h-full",
          "transition-opacity duration-500",
          mounted ? "opacity-100" : "opacity-0",
          hidden ? "opacity-0" : "opacity-100"
        )}
      >
        <NavBar
          options={options}
          selectedValue={pathname}
          position="left"
        />
      </div>
      <div
        className={cn(
          "transform-width duration-300",
          !hidden && "mr-4"
        )}
        style={{ height: "100%", width: `${!hidden ? navBarWidth : 0}px` }}
      />
      {children}
    </div>
  )
}
