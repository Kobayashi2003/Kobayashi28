"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { useUserContext } from "@/context/UserContext"

import { cn } from "@/lib/utils"

import { MarkButton } from "@/components/button/MarkButton"
import { GhostButton } from "@/components/button/GhostButton"
import { LoginButton } from "@/components/button/LoginButton"
import { RegisterButton } from "@/components/button/RegisterButton"
import { LogoutButton } from "@/components/button/LogoutButton"

import { LoginDialog } from "@/components/dialog/LoginDialog"

interface UserHeaderProps {
  className?: string
}

export function UserHeader({ className }: UserHeaderProps) {
  const [loginOpen, setLoginOpen] = useState(false)
  const [registerOpen, setRegisterOpen] = useState(false)

  return (
    <></>
  )
}
