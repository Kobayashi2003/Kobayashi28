"use client"

import { useUserContext } from "@/context/UserContext"
import { UserMark } from "./UserMark"
import { UserHome } from "./UserHome"
import { UserLogout } from "./UserLogout"
import { UserLogin } from "./UserLogin"
import { UserRegister } from "./UserRegister"
import { GhostButton } from "./GhostButton"

interface UserHeaderProps {
  className?: string
}

export function UserHeader({ className }: UserHeaderProps) {
  const { user, isLoading } = useUserContext()

  return (
    <div className={`flex flex-row justify-between items-center gap-1 ${isLoading && "animate-pulse"} ${className}`}>
      {isLoading ? (
        <>
          <GhostButton />
          <GhostButton />
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
