"use client"

import { usePathname, useRouter } from "next/navigation"
import Link from "next/link"
import { BackButton } from "@/components/button/BackButton"

interface HeaderNaviProps {
  className?: string
}

export function HeaderNavi({ className }: HeaderNaviProps) {
  const router = useRouter()
  const pathname = usePathname()
  const isHomePage = pathname === "/"

  return (
    <div className={`flex flex-row justify-between items-center gap-1 ${className} select-none`}>
      {!isHomePage && (
        <BackButton
          handleBack={() => router.back()}
          disabled={false}
          className="text-white hover:text-white/80 hover:bg-white/10"
        />
      )}
      <Link 
        href="/" 
        className="hover:opacity-80 transition-opacity"
        // onClick={() => isHomePage ? window.location.reload() : router.push("/")}
        onClick={() => isHomePage ? router.replace("/") : router.push("/")}
      >
        <h1 className="font-serif italic font-black text-xl text-white">VNDB</h1>
      </Link>
    </div>
  )
}
