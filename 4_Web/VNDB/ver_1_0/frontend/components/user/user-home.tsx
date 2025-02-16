"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { useUser } from "./user-context"

export function UserHome() {
  const { user } = useUser()

  if (!user) return null

  const initial = user.username.charAt(0).toUpperCase()

  return (
    <Button
      asChild
      variant="outline"
      className="bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20 w-10 h-10 p-0"
    >
      <Link href="/user">
        <span className="font-serif italic font-black text-xl text-white">{initial}</span>
      </Link>
    </Button>
  )
}