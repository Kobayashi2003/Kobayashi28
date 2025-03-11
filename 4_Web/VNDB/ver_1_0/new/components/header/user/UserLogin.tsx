"use client"

import { useState } from "react"
import { useUserContext } from "@/context/UserContext"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Loader2, LogIn } from "lucide-react"


interface UserLoginButtonProps {
  setOpen: (open: boolean) => void
}

interface UserLoginDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
}

function UserLoginButton({ setOpen }: UserLoginButtonProps) {
  return (
    <Button 
      variant="outline"
      size="icon"
      className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 
      text-white hover:text-white/80 font-bold text-base md:text-lg transition-all duration-300"
      onClick={() => setOpen(true)}
    >
      <LogIn className="w-4 h-4" />
    </Button>
  )
}

function UserLoginDialog({ open, setOpen }: UserLoginDialogProps) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const { login } = useUserContext()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      await login(username, password)
      setOpen(false)
    } catch (error) {
      console.error("Login failed:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="bg-[#0F2942]/80 border-white/10">
        <DialogHeader>
          <DialogTitle className="text-xl text-white">Login</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username" className="text-white">
              Username
            </Label>
            <Input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              className="bg-[#0A1929] border-white/10 text-white placeholder:text-white/50"
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password" className="text-white">
              Password
            </Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              className="bg-[#0A1929] border-white/10 text-white placeholder:text-white/50"
              required
            />
          </div>
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full bg-[#1A3A5A] hover:bg-[#254B75] text-white font-bold transition-all duration-300"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : "Login"}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export function UserLogin() {
  const [open, setOpen] = useState(false)
  return (
    <>
      <UserLoginButton setOpen={setOpen} />
      <UserLoginDialog open={open} setOpen={setOpen} />
    </>
  )
}
