'use client'

import { ReactNode, useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { api } from '@/lib/api'
import { cn } from "@/lib/utils"
import { useToast } from "@/hooks/use-toast"

export default function AdminDashboardLayout({ children }: { children: ReactNode }) {
  const [isAdmin, setIsAdmin] = useState(false)
  const router = useRouter()
  const { toast } = useToast()
  const pathname = usePathname()

  useEffect(() => {
    const checkAdminStatus = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }

      try {
        const user = await api.getCurrentUser(token)
        if (!user.is_admin) {
          toast({
            title: "Access Denied",
            description: "You do not have permission to access this area.",
            variant: "destructive",
          })
          router.push('/dashboard')
        } else {
          setIsAdmin(true)
        }
      } catch (error) {
        console.error('Failed to check admin status', error)
        toast({
          title: "Error",
          description: "Failed to verify admin status. Please try logging in again.",
          variant: "destructive",
        })
        router.push('/login')
      }
    }

    checkAdminStatus()
  }, [router, toast])

  if (!isAdmin) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  return (
    <div className="flex min-h-screen">
      <nav className="w-64 border-r bg-background">
        <div className="flex flex-col gap-2 p-4">
          <Link 
            href="/dashboard/admin" 
            className={cn(
              "px-3 py-2 rounded-md text-sm transition-colors",
              pathname === "/dashboard/admin"
                ? "bg-primary text-primary-foreground" 
                : "text-foreground/60 hover:text-foreground hover:bg-accent"
            )}
          >
            Admin Dashboard
          </Link>
          <Link 
            href="/dashboard/admin/users" 
            className={cn(
              "px-3 py-2 rounded-md text-sm transition-colors",
              pathname === "/dashboard/admin/users"
                ? "bg-primary text-primary-foreground" 
                : "text-foreground/60 hover:text-foreground hover:bg-accent"
            )}
          >
            User Management
          </Link>
          <Link 
            href="/dashboard/admin/doctors" 
            className={cn(
              "px-3 py-2 rounded-md text-sm transition-colors",
              pathname === "/dashboard/admin/doctors"
                ? "bg-primary text-primary-foreground" 
                : "text-foreground/60 hover:text-foreground hover:bg-accent"
            )}
          >
            Doctor Management
          </Link>
          <Link 
            href="/dashboard/admin/departments" 
            className={cn(
              "px-3 py-2 rounded-md text-sm transition-colors",
              pathname === "/dashboard/admin/departments"
                ? "bg-primary text-primary-foreground" 
                : "text-foreground/60 hover:text-foreground hover:bg-accent"
            )}
          >
            Department Management
          </Link>
          <Link 
            href="/dashboard/admin/schedules" 
            className={cn(
              "px-3 py-2 rounded-md text-sm transition-colors",
              pathname === "/dashboard/admin/schedules"
                ? "bg-primary text-primary-foreground" 
                : "text-foreground/60 hover:text-foreground hover:bg-accent"
            )}
          >
            Schedule Management
          </Link>
          <Link 
            href="/dashboard/admin/appointments" 
            className={cn(
              "px-3 py-2 rounded-md text-sm transition-colors",
              pathname === "/dashboard/admin/appointments"
                ? "bg-primary text-primary-foreground" 
                : "text-foreground/60 hover:text-foreground hover:bg-accent"
            )}
          >
            Appointment Management
          </Link>
        </div>
      </nav>
      <main className="flex-1 bg-background p-4">
        {children}
      </main>
    </div>
  )
}