'use client'

import { ReactNode, useEffect, useState } from 'react'
import { Users, UserCog, Stethoscope, Building2, Calendar, ClipboardList, LayoutDashboard, Link2 } from 'lucide-react'
import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { api } from '@/lib/api'
import { cn } from "@/lib/utils"
import { useToast } from "@/hooks/use-toast"

const adminLinks = [
  { href: "/admin", label: "Admin Dashboard", icon: LayoutDashboard },
  { href: "/admin/users", label: "User Management", icon: Users },
  { href: "/admin/patients", label: "Patient Management", icon: UserCog },
  { href: "/admin/doctors", label: "Doctor Management", icon: Stethoscope },
  { href: "/admin/departments", label: "Department Management", icon: Building2 },
  { href: "/admin/schedules", label: "Schedule Management", icon: Calendar },
  { href: "/admin/appointments", label: "Appointment Management", icon: ClipboardList },
  { href: "/admin/affiliations", label: "Affiliation Management", icon: Link2 },
]

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
      <nav className="w-64 border-r bg-background hidden md:block">
        <div className="flex flex-col gap-2 p-4">
          {adminLinks.map((link) => (
            <Link 
              key={link.href}
              href={link.href} 
              className={cn(
                "px-3 py-2 rounded-md text-sm transition-colors flex items-center gap-2",
                pathname === link.href
                  ? "bg-primary text-primary-foreground" 
                  : "text-foreground/60 hover:text-foreground hover:bg-accent"
              )}
            >
              <link.icon className="w-4 h-4" />
              {link.label}
            </Link>
          ))}
        </div>
      </nav>
      <main className="flex-1 bg-background p-4 overflow-auto">
        {children}
      </main>
    </div>
  )
}