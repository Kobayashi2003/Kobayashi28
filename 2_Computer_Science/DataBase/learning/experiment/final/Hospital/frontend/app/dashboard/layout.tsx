'use client'

import { ReactNode, useEffect, useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { api } from '@/lib/api'
import { cn } from "@/lib/utils"

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const [isAdmin, setIsAdmin] = useState(false)

  useEffect(() => {
    const checkAdminStatus = async () => {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          const user = await api.getCurrentUser(token)
          setIsAdmin(user.is_admin)
        } catch (error) {
          console.error('Failed to check admin status', error)
        }
      }
    }

    checkAdminStatus()
  }, [])

  return (
    <div className="flex min-h-screen bg-background">
      <nav className="w-64 border-r bg-background">
        <div className="flex flex-col gap-2 p-4">
          <Link 
            href="/dashboard" 
            className={cn(
              "px-3 py-2 rounded-md text-sm transition-colors",
              pathname === "/dashboard" 
                ? "bg-primary text-primary-foreground" 
                : "text-foreground/60 hover:text-foreground hover:bg-accent"
            )}
          >
            Dashboard
          </Link>
          <Link 
            href="/dashboard/profile" 
            className={cn(
              "px-3 py-2 rounded-md text-sm transition-colors",
              pathname === "/dashboard/profile" 
                ? "bg-primary text-primary-foreground" 
                : "text-foreground/60 hover:text-foreground hover:bg-accent"
            )}
          >
            Profile
          </Link>
          {isAdmin && (
            <Link 
              href="/dashboard/admin" 
              className={cn(
                "px-3 py-2 rounded-md text-sm transition-colors",
                pathname.startsWith("/dashboard/admin")
                  ? "bg-primary text-primary-foreground" 
                  : "text-foreground/60 hover:text-foreground hover:bg-accent"
              )}
            >
              Admin
            </Link>
          )}
        </div>
      </nav>
      <main className="flex-1 p-4">
        {children}
      </main>
    </div>
  )
}