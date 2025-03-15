"use client"

import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { useUserContext } from "@/context/UserContext"

export function UserHome() {
  const router = useRouter()
  const { user } = useUserContext()
  if (!user) return null
  const initial = user.username.charAt(0).toUpperCase()
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => router.push("/u/c")}
      className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 select-none
      text-white hover:text-white/80 text-base md:text-lg font-bold font-serif italic transition-all duration-300"
    >
      {initial}
    </Button>
  )
}
