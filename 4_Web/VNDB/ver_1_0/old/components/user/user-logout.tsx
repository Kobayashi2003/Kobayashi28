"use client"

import { Button } from "@/components/ui/button"
import { useUser } from "./user-context"

export function UserLogout() {
  const { logout } = useUser()

  return (
    <Button
      variant="outline"
      className="bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20 text-white font-bold"
      onClick={logout}
    >
      Logout
    </Button>
  )
}