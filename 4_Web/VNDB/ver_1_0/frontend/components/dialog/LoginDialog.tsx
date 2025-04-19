"use client"

import { useState } from "react"

import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Loader2, ArrowRight } from "lucide-react"

interface LoginDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  handleLogin: (username: string, password: string) => void
  disabled?: boolean
  className?: string
}

export function LoginDialog({ open, setOpen, handleLogin, disabled, className }: LoginDialogProps) {

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const fields = [
    {
      id: "username", value: username, setValue: setUsername, label: "Username",
      type: "text", placeholder: "Enter your username", required: true
    },
    {
      id: "password", value: password, setValue: setPassword, label: "Password",
      type: "password", placeholder: "Enter your password", required: true
    },
  ]

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    handleLogin(username, password)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className={cn(
        "bg-[#0F2942]/80 border-white/10",
        "data-[state=open]:animate-in data-[state=closed]:animate-out",
        "data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
        "data-[state=closed]:slide-out-to-bottom-1/2 data-[state=open]:slide-in-from-bottom-1/2",
        className
      )}>
        <DialogHeader>
          <DialogTitle className="text-xl text-white">Login</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          {fields.map((field) => (
            <div key={field.id} className="space-y-2">
              <Label htmlFor={field.id} className="text-white">{field.label}</Label>
              <Input id={field.id} type={field.type} placeholder={field.placeholder}
                value={field.value} onChange={(e) => field.setValue(e.target.value)} required={field.required}
                className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50 selection:bg-blue-500 selection:text-white" />
            </div>
          ))}
          <Button type="submit" disabled={disabled} className="w-full bg-[#1A3A5A] hover:bg-[#254B75] text-white font-bold transition-all duration-300">
            {disabled ? <Loader2 className="w-4 h-4 animate-spin" /> : <ArrowRight className="w-4 h-4" />}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
