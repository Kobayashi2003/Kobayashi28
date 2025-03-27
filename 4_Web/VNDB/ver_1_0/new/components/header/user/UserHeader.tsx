"use client"

import { useRouter } from "next/navigation"
import { useUserContext } from "@/context/UserContext"
import { UserMark } from "./UserMark"
// import { UserHome } from "./UserHome"
// import { UserLogout } from "./UserLogout"
import { UserLogin } from "./UserLogin"
import { UserRegister } from "./UserRegister"
import { GhostButton } from "./GhostButton"
import { LetterButton } from "@/components/button/LetterButton"
import { LogoutButton } from "@/components/button/LogoutButton"

interface UserHeaderProps {
  className?: string
}

export function UserHeader({ className }: UserHeaderProps) {
  const router = useRouter()
  const { user, isLoading, logout } = useUserContext()

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
          {/* <UserHome /> */}
          <LetterButton letter={user.username.charAt(0).toUpperCase()} onClick={() => router.push("/u/c")} disabled={false} className={""} />
          {/* <UserLogout /> */}
          <LogoutButton handleLogout={() => logout()} disabled={false} className={""} />
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
