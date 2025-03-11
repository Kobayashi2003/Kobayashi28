"use client"

import { useRouter, usePathname } from "next/navigation"
import Link from "next/link"
import { Button } from "../ui/button"
import { ArrowLeft } from "lucide-react"
import { useUserContext } from "@/context/UserContext"
import { UserMark } from "./user/UserMark"
import { UserHome } from "./user/UserHome"
import { UserLogout } from "./user/UserLogout"
import { UserLogin } from "./user/UserLogin"
import { UserRegister } from "./user/UserRegister"


interface HeaderBarProps {

}

export function HeaderBar({}: HeaderBarProps) {

  const router = useRouter()
  const pathname = usePathname()
  const isHomePage = pathname === "/"

  const { user, isLoading } = useUserContext()

  return (
      <header className="px-4 border-b border-white/10">
        <div className="container mx-auto flex flex-col justify-center items-between py-4 gap-1">
          <div className="flex flex-row justify-between items-center gap-2">
            <div className="flex flex-row justify-between items-center gap-1">
              {!isHomePage && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => router.back()}
                  className="text-white hover:bg-white/10"
                  aria-label="Go back"
                >
                  <ArrowLeft className="h-5 w-5" />
                </Button>
              )}
              <Link href="/" className="hover:opacity-80 transition-opacity">
                <h1 className="font-bold text-white text-sm md:text-base lg:text-lg xl:text-xl">Visual Novel Database</h1>
              </Link>
            </div>
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
          <div className=""></div>
        </div>
      </header>
  )
}