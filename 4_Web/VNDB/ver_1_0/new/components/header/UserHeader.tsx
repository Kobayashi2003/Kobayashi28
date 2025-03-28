"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useUserContext } from "@/context/UserContext"

import { cn } from "@/lib/utils"

import { GhostButton } from "@/components/button/GhostButton"
import { LetterButton } from "@/components/button/LetterButton"
import { LoginButton } from "@/components/button/LoginButton"
import { RegisterButton } from "@/components/button/RegisterButton"
import { LogoutButton } from "@/components/button/LogoutButton"
import { MarkButton } from "@/components/button/MarkButton"

import { LoginDialog } from "@/components/dialog/LoginDialog"
import { RegisterDialog } from "@/components/dialog/RegisterDialog"
import { MarkDialog } from "@/components/dialog/MarkDialog"
import { ConfirmDialog } from "@/components/dialog/ConfirmDialog"

interface UserHeaderProps {
  className?: string
}

export function UserHeader({ className }: UserHeaderProps) {

  const router = useRouter()
  const { user, isLoading, login, register, logout } = useUserContext()

  const [loginDialogOpen, setLoginDialogOpen] = useState(false)
  const [registerDialogOpen, setRegisterDialogOpen] = useState(false)
  const [logoutDialogOpen, setLogoutDialogOpen] = useState(false)
  const [markDialogOpen, setMarkDialogOpen] = useState(false)

  return (
    <div className={cn(
      "flex flex-row justify-between items-center gap-1",
      className
    )}>
      {isLoading && (
        <>
          <GhostButton />
          <GhostButton />
        </>
      )}
      {!isLoading && user ? (
        <>
          <MarkButton 
            onClick={() => setMarkDialogOpen(!markDialogOpen)}
            disabled={isLoading}
          />
          <MarkDialog 
            open={markDialogOpen} 
            setOpen={setMarkDialogOpen}
          />
          <LetterButton
            letter={user.username.charAt(0).toUpperCase()}
            onClick={() => router.push("/u/c")}
            disabled={isLoading}
          />
          <LogoutButton
            handleLogout={() => setLogoutDialogOpen(!logoutDialogOpen)}
            disabled={isLoading}
          />
          <ConfirmDialog
            open={logoutDialogOpen}
            setOpen={setLogoutDialogOpen}
            title="Logout"
            description="Are you sure you want to logout?"
            confirmText="Logout"
            cancelText="Cancel"
            onConfirm={() => logout()}
            onCancel={() => setLogoutDialogOpen(false)}
          />
        </>
      ) : (
        <>
          <LoginButton
            handleLogin={() => setLoginDialogOpen(!loginDialogOpen)}
            disabled={isLoading}
          />
          <LoginDialog
            open={loginDialogOpen}
            setOpen={setLoginDialogOpen}
            handleLogin={login}
            disabled={isLoading}
          />
          <RegisterButton
            handleRegister={() => setRegisterDialogOpen(!registerDialogOpen)}
            disabled={isLoading}
          />
          <RegisterDialog
            open={registerDialogOpen}
            setOpen={setRegisterDialogOpen}
            handleRegister={register}
            disabled={isLoading}
          />
        </>
      )}
    </div>
  )
}
