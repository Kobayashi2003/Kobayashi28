'use client'

import { use, useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Registration, Schedule, Doctor, Department } from '@/lib/types'
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function AppointmentDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const [appointment, setAppointment] = useState<Registration | null>(null)
  const [schedule, setSchedule] = useState<Schedule | null>(null)
  const [doctor, setDoctor] = useState<Doctor | null>(null)
  const [department, setDepartment] = useState<Department | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    const fetchAppointmentDetails = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }

      try {
        // Fetch appointment details
        const appointmentData = await api.getRegistration(parseInt(id), token)
        setAppointment(appointmentData)

        // Fetch related schedule
        const scheduleData = await api.getSchedule(appointmentData.schedule_id, token)
        setSchedule(scheduleData)

        // Fetch related doctor
        const doctorData = await api.getDoctor(scheduleData.doctor_id, token)
        setDoctor(doctorData)

        // Fetch related department
        const departmentData = await api.getDepartment(scheduleData.department_id, token)
        setDepartment(departmentData)
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to load appointment details.",
          variant: "destructive",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchAppointmentDetails()
  }, [id, router, toast])

  const handleCancelAppointment = async () => {
    const token = localStorage.getItem('token')
    if (!token || !appointment) return

    try {
      await api.cancelRegistration(appointment.id, token)
      toast({
        title: "Success",
        description: "Appointment cancelled successfully.",
      })
      router.push('/appointments')
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to cancel appointment. Please try again.",
        variant: "destructive",
      })
    }
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <Skeleton className="h-8 w-1/3 mb-2" />
            <Skeleton className="h-4 w-1/2" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-2/3" />
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!appointment || !schedule || !doctor || !department) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
            <CardDescription>Failed to load appointment details.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/appointments')}>Return to Appointments</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Appointment Details</CardTitle>
          <CardDescription>Appointment ID: {appointment.id}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h2 className="text-lg font-semibold">Status</h2>
              <p>{appointment.status}</p>
            </div>
            <div>
              <h2 className="text-lg font-semibold">Date and Time</h2>
              <p>{new Date(schedule.date).toLocaleDateString()} {schedule.start_time} - {schedule.end_time}</p>
            </div>
            <div>
              <h2 className="text-lg font-semibold">Doctor</h2>
              <p>{doctor.name}</p>
            </div>
            <div>
              <h2 className="text-lg font-semibold">Department</h2>
              <p>{department.name}</p>
            </div>
            <div>
              <h2 className="text-lg font-semibold">Notes</h2>
              <p>{appointment.notes || 'No notes'}</p>
            </div>
            {appointment.status === 'scheduled' && (
              <Button onClick={handleCancelAppointment} variant="destructive">
                Cancel Appointment
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}