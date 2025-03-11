"use client"

import { useState } from "react"
import { useUserContext } from "@/context/UserContext"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Loader2, UserPlus } from "lucide-react"

interface UserRegisterButtonProps {
  setOpen: (open: boolean) => void
}

interface UserRegisterDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
}

function UserRegisterButton({ setOpen }: UserRegisterButtonProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 
      text-white hover:text-white/80 font-bold text-base md:text-lg transition-all duration-300"
      onClick={() => setOpen(true)}
    >
      <UserPlus className="w-4 h-4" />
    </Button>
  )
}

function UserRegisterDialog({ open, setOpen }: UserRegisterDialogProps) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const { register } = useUserContext()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (password !== confirmPassword) {
      alert("Passwords do not match")
      return
    }
    setIsLoading(true)
    try {
      await register(username, password)
      setOpen(false)
    } catch (error) {
      console.error("Registration failed:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="bg-[#0F2942]/80 border-white/10">
        <DialogHeader>
          <DialogTitle className="text-xl text-white">Register</DialogTitle>
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
          <div className="space-y-2">
            <Label htmlFor="confirmPassword" className="text-white">
              Confirm Password
            </Label>
            <Input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Enter your password again"
              className="bg-[#0A1929] border-white/10 text-white placeholder:text-white/50"
              required
            />
          </div>
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full bg-[#1A3A5A] hover:bg-[#254B75] text-white font-bold"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : "Register"}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export function UserRegister() {
  const [open, setOpen] = useState(false)
  return (
    <>
      <UserRegisterButton setOpen={setOpen} />
      <UserRegisterDialog open={open} setOpen={setOpen} />
    </>
  )
}
