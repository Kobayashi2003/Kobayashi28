"use client"

import { LogOut } from "lucide-react"
import { useUserContext } from "@/context/UserContext"
import { Button } from "@/components/ui/button"

export function UserLogout() {
  const { logout } = useUserContext()

  return (
    <Button 
      variant="outline"
      size="icon"
      className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 
      text-white hover:text-white/80 font-bold text-base md:text-lg transition-all duration-300"
      onClick={() => logout()}
    >
      <LogOut className="w-4 h-4" />
    </Button>
  )
}
