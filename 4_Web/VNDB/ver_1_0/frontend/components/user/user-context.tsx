"use client"

import type React from "react"

import { createContext, useContext, useState, useEffect } from "react"
import { api } from "@/lib/api"

interface User {
  username: string
  // Add any other user properties returned by the API
}

interface UserContextType {
  user: User | null
  login: (username: string, password: string) => Promise<void>
  register: (username: string, password: string) => Promise<void>
  logout: () => void
  updateUser: (newUsername: string) => Promise<void>
  changePassword: (oldPassword: string, newPassword: string) => Promise<void>
  isLoading: boolean
}

const UserContext = createContext<UserContextType | undefined>(undefined)

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const getUserData = async (username: string) => {
    const token = localStorage.getItem("access_token")
    if (!token) return null

    try {
      const userData = await api.getUser(username)
      return userData
    } catch (error) {
      console.error("Failed to get user data:", error)
      return null
    }
  }

  useEffect(() => {
    const initializeUser = async () => {
      setIsLoading(true)
      const token = localStorage.getItem("access_token")
      if (token) {
        // Attempt to get username from token (implementation depends on your token structure)
        const username = extractUsernameFromToken(token) // Implement this function
        if (username) {
          const userData = await getUserData(username)
          setUser(userData)
        }
      }
      setIsLoading(false)
    }

    initializeUser()
  }, []) // Removed getUserData from dependencies

  const login = async (username: string, password: string) => {
    try {
      const response = await api.login(username, password)
      localStorage.setItem("access_token", response.access_token)
      const userData = await getUserData(username)
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
      const userData = await getUserData(username)
      setUser(userData)
    } catch (error) {
      console.error("Registration failed:", error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem("access_token")
    setUser(null)
  }

  const updateUser = async (newUsername: string) => {
    if (!user) throw new Error("No user logged in")
    try {
      const updatedUser = await api.updateUser(user.username, newUsername)
      setUser(updatedUser)
    } catch (error) {
      console.error("Failed to update user:", error)
      throw error
    }
  }

  const changePassword = async (oldPassword: string, newPassword: string) => {
    if (!user) throw new Error("No user logged in")
    try {
      await api.changePassword(user.username, oldPassword, newPassword)
    } catch (error) {
      console.error("Failed to change password:", error)
      throw error
    }
  }

  return (
    <UserContext.Provider value={{ user, login, register, logout, updateUser, changePassword, isLoading }}>
      {children}
    </UserContext.Provider>
  )
}

export function useUser() {
  const context = useContext(UserContext)
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider")
  }
  return context
}

// Placeholder function - needs actual implementation based on your token structure
const extractUsernameFromToken = (token: string): string | null => {
  // Example: Assuming token is a JWT and username is in the payload
  try {
    const payload = JSON.parse(atob(token.split(".")[1]))
    return payload.username
  } catch (error) {
    console.error("Failed to extract username from token:", error)
    return null
  }
}