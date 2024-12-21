'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function HomePage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    const token = localStorage.getItem('token')
    setIsLoggedIn(!!token)
  }, [])

  const handleLogin = () => {
    router.push('/login')
  }

  const handleRegister = () => {
    router.push('/register')
  }

  const handleEnterApp = () => {
    router.push('/appointments')
  }

  return (
    <div className="container mx-auto px-4 py-8 flex items-center justify-center min-h-screen">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Welcome to Medical Appointment System</CardTitle>
          <CardDescription>Manage your medical appointments with ease</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoggedIn ? (
            <Button onClick={handleEnterApp} className="w-full">
              Enter Application
            </Button>
          ) : (
            <div className="space-y-4">
              <Button onClick={handleLogin} className="w-full">
                Login
              </Button>
              <Button onClick={handleRegister} variant="outline" className="w-full">
                Register
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}