"use client"

import { usePathname, useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "../ui/button"
import { ArrowBigLeft } from "lucide-react"

interface HeaderNaviProps {
  className?: string
}

export function HeaderNavi({ className }: HeaderNaviProps) {
  const router = useRouter()
  const pathname = usePathname()
  const isHomePage = pathname === "/home"

  return (
    <div className={`flex flex-row justify-between items-center gap-1 ${className}`}>
      {!isHomePage && (
        <Button
          variant="ghost"
          size="icon"
          onClick={() => router.back()}
          className="text-white hover:text-white/80 hover:bg-white/10"
          aria-label="Go back"
        >
          <ArrowBigLeft className="h-5 w-5" />
        </Button>
      )}
      <Link 
        href="/home" 
        className="hover:opacity-80 transition-opacity"
        onClick={() => isHomePage ? window.location.reload() : router.push("/home")}
      >
        <h1 className="font-serif italic font-black text-xl text-white">VNDB</h1>
      </Link>
    </div>
  )
}
