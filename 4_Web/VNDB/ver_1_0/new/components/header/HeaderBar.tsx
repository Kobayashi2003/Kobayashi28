"use client"

import { useRouter, usePathname } from "next/navigation"
import Link from "next/link"
import { Button } from "../ui/button"
import { ArrowBigLeft } from "lucide-react"
import { useUserContext } from "@/context/UserContext"
import { UserMark } from "./user/UserMark"
import { UserHome } from "./user/UserHome"
import { UserLogout } from "./user/UserLogout"
import { UserLogin } from "./user/UserLogin"
import { UserRegister } from "./user/UserRegister"
import { Search } from "./search/Search"

interface HeaderBarProps {
  className?: string
}

export function HeaderBar({ className }: HeaderBarProps) {

  const router = useRouter()
  const pathname = usePathname()
  const isHomePage = pathname === "/"

  const { user, isLoading } = useUserContext()

  return (
      <header className={`px-4 border-b border-white/10 ${className}`}>
        <div className="container mx-auto flex flex-col justify-center items-between py-4 gap-1">
          <div className="flex flex-row justify-between items-center gap-2">
            <div className="flex flex-row justify-between items-center gap-1">
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
              <Link href="/" className="hover:opacity-80 transition-opacity">
                <h1 className="font-serif italic font-black text-xl text-white">VNDB</h1>
              </Link>
            </div>
            <Search className="hidden md:flex" />
            <div className="flex flex-row justify-between items-center gap-1">
              {isLoading ? (
                <>
                  <div className="w-5 h-5 bg-[#0F2942]/80 rounded-full animate-pulse delay-0" />
                  <div className="w-5 h-5 bg-[#88ccff]/80 rounded-full animate-pulse delay-100" />
                  <div className="w-5 h-5 bg-[#ff6666]/80 rounded-full animate-pulse delay-200" />
                </>
              ) : user ? (
                <>
                  <UserMark />
                  <UserHome />
                  <UserLogout />
                </>
              ) : (
                <>
                  <UserLogin />
                  <UserRegister />
                </>
              )}
            </div>
          </div>
          <Search className="flex md:hidden" />
        </div>
      </header>
  )
}