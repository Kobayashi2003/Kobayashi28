'use client'

import { useState, useEffect, useCallback, useMemo, Fragment } from 'react'
import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { Calendar, User, Stethoscope, Building2, LogOut, LayoutDashboard, Users } from 'lucide-react'
import { api } from '@/lib/api'
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { useToast } from "@/hooks/use-toast"

// Custom hook for authentication and user state management
const useAuth = () => {
  const [isAdmin, setIsAdmin] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()
  const { toast } = useToast()

  const checkAuth = useCallback(async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const user = await api.getCurrentUser(token)
      setIsAdmin(user.is_admin)
      localStorage.setItem('userId', user.id.toString())
      localStorage.setItem('isAdmin', user.is_admin.toString())
    } catch (error) {
      console.error('Authentication failed', error)
      toast({
        title: "Authentication Error",
        description: "Please log in again.",
        variant: "destructive",
      })
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      localStorage.removeItem('isAdmin')
      router.push('/login')
    } finally {
      setIsLoading(false)
    }
  }, [router, toast])

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  return { isAdmin, isLoading }
}

// Navigation item type
type NavigationItem = {
  name: string
  href: string
  icon: React.ElementType
}

// Main navigation items
const MAIN_NAV_ITEMS: NavigationItem[] = [
  { name: 'Appointments', href: '/appointments', icon: Calendar },
  { name: 'Doctors', href: '/doctors', icon: Stethoscope },
  { name: 'Departments', href: '/departments', icon: Building2 },
  { name: 'Patients', href: '/patients', icon: Users },
  { name: 'Profile', href: '/profile', icon: User },
]

// Admin navigation items
const ADMIN_NAV_ITEMS: NavigationItem[] = [
  { name: 'Admin Dashboard', href: '/admin', icon: LayoutDashboard },
  // More admin items can be added here in the future
]

// NavLink component
const NavLink = ({ item, isActive }: { item: NavigationItem; isActive: boolean }) => (
  <Link
    href={item.href}
    className={cn(
      'group flex items-center px-2 py-2 text-sm font-medium rounded-md',
      isActive ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
    )}
  >
    <item.icon
      className={cn(
        'mr-3 h-5 w-5',
        isActive ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-500'
      )}
    />
    {item.name}
  </Link>
)

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const { isAdmin, isLoading } = useAuth()
  const router = useRouter()
  const pathname = usePathname()
  const { toast } = useToast()

  const handleLogout = useCallback(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
    localStorage.removeItem('isAdmin')
    toast({
      title: "Logged out",
      description: "You have been successfully logged out.",
    })
    router.push('/')
  }, [router, toast])

  const navItems = useMemo(() => {
    return isAdmin ? [...MAIN_NAV_ITEMS, ...ADMIN_NAV_ITEMS] : MAIN_NAV_ITEMS
  }, [isAdmin])

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  return (
    <div className="min-h-screen flex">
      <div className="hidden md:flex md:w-64 md:flex-col">
        <div className="flex flex-col flex-grow border-r border-gray-200 bg-white pt-5">
          <div className="flex-shrink-0 px-4">
            <h1 className="text-xl font-semibold text-gray-900">Medical App</h1>
          </div>

          <nav className="mt-8 flex-1 px-2 space-y-1">
            {navItems.map((item, index) => (
              <Fragment key={item.name}>
                {isAdmin && index === MAIN_NAV_ITEMS.length && <Separator className="my-4" />}
                <NavLink item={item} isActive={pathname === item.href} />
              </Fragment>
            ))}
          </nav>

          <div className="flex-shrink-0 border-t border-gray-200 p-4">
            <Button
              variant="ghost"
              className="w-full"
              onClick={handleLogout}
            >
              <LogOut className="mr-3 h-5 w-5" />
              <span>Logout</span>
            </Button>
          </div>
        </div>
      </div>

      <main className="flex-1 overflow-y-auto bg-gray-50">
        <div className="py-6">{children}</div>
      </main>
    </div>
  )
}