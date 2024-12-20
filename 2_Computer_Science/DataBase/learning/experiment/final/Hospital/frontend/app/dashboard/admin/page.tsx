'use client'

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function AdminDashboardPage() {
  const [stats, setStats] = useState({
    totalUsers: 0,
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
        const [users, doctors, departments, appointments, schedules] = await Promise.all([
          api.getUsers(1, 1, 'id', false, token),
          api.getDoctors(1, 1, 'id', false, token),
          api.getDepartments(1, 1, 'id', false, token),
          api.getRegistrations(1, 1, 'id', false, token),
          api.getSchedules(1, 1, 'id', false, token)
        ])

        setStats({
          totalUsers: users.count,
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

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Total Users</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.totalUsers}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Total Doctors</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.totalDoctors}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Total Departments</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.totalDepartments}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Total Appointments</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.totalAppointments}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Total Schedules</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.totalSchedules}</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}