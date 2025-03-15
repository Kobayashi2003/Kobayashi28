"use client"

import { useUserContext } from "@/context/UserContext"
import { UserMark } from "./UserMark"
import { UserHome } from "./UserHome"
import { UserLogout } from "./UserLogout"
import { UserLogin } from "./UserLogin"
import { UserRegister } from "./UserRegister"

interface UserHeaderProps {
  className?: string
}

export function UserHeader({ className }: UserHeaderProps) {
  const { user, isLoading } = useUserContext()

  return (
    <div className={`flex flex-row justify-between items-center gap-1 ${className}`}>
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
  )
}
