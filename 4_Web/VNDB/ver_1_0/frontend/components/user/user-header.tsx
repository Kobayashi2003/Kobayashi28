"use client"

import { useUser } from "./user-context"
import { UserLogin } from "./user-login"
import { UserRegister } from "./user-register"
import { UserHome } from "./user-home"
import { UserLogout } from "./user-logout"

export function UserHeader() {
  const { user, isLoading } = useUser()

  if (isLoading) {
    return null
  }

  return (
    <div className="flex items-center gap-2">
      {user ? (
        <>
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