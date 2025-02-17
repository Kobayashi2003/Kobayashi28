"use client"

import type React from "react"
import { createContext, useContext, useState, useEffect } from "react"
import { api } from "@/lib/api"
import type { User } from "@/lib/types"

interface UserContextType {
  user: User | null
  login: (username: string, password: string) => Promise<void>
  register: (username: string, password: string) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const UserContext = createContext<UserContextType | undefined>(undefined)

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const initializeUser = async () => {
      setIsLoading(true)
      const token = localStorage.getItem("access_token")

      if (token) {
        try {
          const username = localStorage.getItem("username")
          if (username) {
            const userData = await api.getUser(username)
            setUser(userData)
          }
        } catch (error) {
          console.error("Failed to get user data:", error)
          localStorage.removeItem("access_token")
          localStorage.removeItem("username")
        }
      }

      setIsLoading(false)
    }

    initializeUser()
  }, [])

  const login = async (username: string, password: string) => {
    try {
      const response = await api.login(username, password)
      localStorage.setItem("access_token", response.access_token)
      localStorage.setItem("username", response.username)
      const userData = await api.getUser(response.username)
      setUser(userData)
    } catch (error) {
      console.error("Login failed:", error)
      throw error
    }
  }

  const register = async (username: string, password: string) => {
    try {
      const response = await api.register(username, password)
      localStorage.setItem("access_token", response.access_token)
      localStorage.setItem("username", response.username)
      const userData = await api.getUser(response.username)
      setUser(userData)
    } catch (error) {
      console.error("Registration failed:", error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("username")
    setUser(null)
  }

  return <UserContext.Provider value={{ user, login, register, logout, isLoading }}>{children}</UserContext.Provider>
}

export function useUser() {
  const context = useContext(UserContext)
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider")
  }
  return context
}