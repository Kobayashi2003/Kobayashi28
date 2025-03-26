"use client"

import { useState } from "react"
import { useUserContext } from "@/context/UserContext"
import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Loader2 } from "lucide-react"

interface LoginOrRegisterPanelProps {
  defaultTab?: "login" | "register"
  className?: string
}

interface LoginPanelProps {
  isLoading: boolean
  handleLogin: (username: string, password: string) => Promise<void>
  className?: string
}

interface RegisterPanelProps {
  isLoading: boolean
  handleRegister: (username: string, password: string) => Promise<void>
  className?: string
}

function LoginPanel({ isLoading, handleLogin }: LoginPanelProps) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    await handleLogin(username, password)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div className="space-y-2">
          <Label className="text-white/80 font-medium">Username</Label>
          <Input
            id="username"
            className="bg-white/10 border-none text-white placeholder:text-white/60
                     focus-visible:ring-2 focus-visible:ring-white/50"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
          />
        </div>
        
        <div className="space-y-2">
          <Label className="text-white/80 font-medium">Password</Label>
          <Input
            type="password"
            id="password"
            className="bg-white/10 border-none text-white placeholder:text-white/60
                     focus-visible:ring-2 focus-visible:ring-white/50"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
          />
        </div>
      </div>

      <Button 
        type="submit" 
        disabled={isLoading}
        className="w-full bg-white text-blue-900 hover:bg-white/90 hover:text-blue-800
                 font-semibold h-11 transition-transform active:scale-95"
      >
        {isLoading ? (
          <Loader2 className="w-5 h-5 animate-spin" />
        ) : "Sign In"}
      </Button>
    </form>
  )
}

function RegisterPanel({ isLoading, handleRegister }: RegisterPanelProps) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    await handleRegister(username, password)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div className="space-y-2">
          <Label className="text-white/80 font-medium">Username</Label>
          <Input
            id="username"
            className="bg-white/10 border-none text-white placeholder:text-white/60
                     focus-visible:ring-2 focus-visible:ring-white/50"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Create a username"
          />
        </div>
        
        <div className="space-y-2">
          <Label className="text-white/80 font-medium">Password</Label>
          <Input
            type="password"
            id="password"
            className="bg-white/10 border-none text-white placeholder:text-white/60
                     focus-visible:ring-2 focus-visible:ring-white/50"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
          />
        </div>

        <div className="space-y-2">
          <Label className="text-white/80 font-medium">Confirm Password</Label>
          <Input
            type="password"
            id="confirmPassword"
            className="bg-white/10 border-none text-white placeholder:text-white/60
                     focus-visible:ring-2 focus-visible:ring-white/50"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="••••••••"
          />
        </div>
      </div>

      <Button 
        type="submit" 
        disabled={isLoading}
        className="w-full bg-white text-blue-900 hover:bg-white/90 hover:text-blue-800
                 font-semibold h-11 transition-transform active:scale-95"
      >
        {isLoading ? (
          <Loader2 className="w-5 h-5 animate-spin" />
        ) : "Create Account"}
      </Button>
    </form>
  )
}

export function LoginOrRegisterPanel({ defaultTab = "login", className }: LoginOrRegisterPanelProps) {
  const { login, register } = useUserContext()
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (username: string, password: string) => {
    setIsLoading(true)
    try {
      await login(username, password)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRegister = async (username: string, password: string) => {
    setIsLoading(true)
    try {
      await register(username, password)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={cn(
      "w-full max-w-md p-8 space-y-8 rounded-2xl",
      "bg-gradient-to-br from-[#1a365d] via-[#153e75] to-[#2b6cb0]",
      "border border-white/20 shadow-2xl shadow-blue-900/50",
      "transform transition-all duration-300 hover:shadow-blue-900/60",
      "opacity-70 hover:opacity-90",
      "backdrop-blur-sm",
      className
    )}>
      <Tabs defaultValue={defaultTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-2 bg-transparent h-12 p-1">
          <TabsTrigger 
            value="login" 
            className={cn(
              "relative z-10 rounded-xl font-semibold",
              "data-[state=active]:text-blue-900 data-[state=active]:bg-white",
              "transition-colors duration-300 hover:text-white/90"
            )}
          >
            Login
          </TabsTrigger>
          <TabsTrigger 
            value="register" 
            className={cn(
              "relative z-10 rounded-xl font-semibold",
              "data-[state=active]:text-blue-900 data-[state=active]:bg-white",
              "transition-colors duration-300 hover:text-white/90"
            )}
          >
            Register
          </TabsTrigger>
        </TabsList>

        <TabsContent value="login" className="pt-4">
          <LoginPanel isLoading={isLoading} handleLogin={handleLogin} />
        </TabsContent>

        <TabsContent value="register" className="pt-4">
          <RegisterPanel isLoading={isLoading} handleRegister={handleRegister} />
        </TabsContent>
      </Tabs>
    </div>
  )
}