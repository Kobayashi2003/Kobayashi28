'use client'

import { useEffect, useState } from "react"
import { Users, UserCog, Stethoscope, Building2, Calendar, ClipboardList } from 'lucide-react'
import Link from 'next/link'
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

interface Stats {
  totalUsers: number
  totalPatients: number
  totalDoctors: number
  totalDepartments: number
  totalAppointments: number
  totalSchedules: number
}

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<Stats>({
    totalUsers: 0,
    totalPatients: 0,
    totalDoctors: 0,
    totalDepartments: 0,
    totalAppointments: 0,
    totalSchedules: 0
  })
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    const fetchStats = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }

      try {
        const [users, patients, doctors, departments, appointments, schedules] = await Promise.all([
          api.getUsers(1, 1, 'id', false, token),
          api.getPatients(1, 1, 'id', false, token),
          api.getDoctors(1, 1, 'id', false, token),
          api.getDepartments(1, 1, 'id', false, token),
          api.getRegistrations(1, 1, 'id', false, token),
          api.getSchedules(1, 1, 'id', false, token)
        ])

        setStats({
          totalUsers: users.count,
          totalPatients: patients.count,
          totalDoctors: doctors.count,
          totalDepartments: departments.count,
          totalAppointments: appointments.count,
          totalSchedules: schedules.count
        })
      } catch (error) {
        console.error('Failed to fetch stats', error)
        toast({
          title: "Error",
          description: "Failed to load dashboard stats.",
          variant: "destructive",
        })
      }
    }

    fetchStats()
  }, [router, toast])

  const statCards = [
    { title: "Total Users", value: stats.totalUsers, icon: Users, href: "/admin/users" },
    { title: "Total Patients", value: stats.totalPatients, icon: UserCog, href: "/admin/patients" },
    { title: "Total Doctors", value: stats.totalDoctors, icon: Stethoscope, href: "/admin/doctors" },
    { title: "Total Departments", value: stats.totalDepartments, icon: Building2, href: "/admin/departments" },
    { title: "Total Appointments", value: stats.totalAppointments, icon: ClipboardList, href: "/admin/appointments" },
    { title: "Total Schedules", value: stats.totalSchedules, icon: Calendar, href: "/admin/schedules" },
  ]

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {statCards.map((card, index) => (
          <Link href={card.href} key={index}>
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {card.title}
                </CardTitle>
                <card.icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{card.value}</div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}