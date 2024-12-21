'use client'

import { use, useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Doctor, Department, Schedule } from '@/lib/types'
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function DoctorDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const [doctor, setDoctor] = useState<Doctor | null>(null)
  const [departments, setDepartments] = useState<Department[]>([])
  const [schedules, setSchedules] = useState<Schedule[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    const fetchDoctorDetails = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }

      try {
        // Fetch doctor details
        const doctorData = await api.getDoctor(parseInt(id), token)
        setDoctor(doctorData)

        // Fetch departments associated with the doctor
        const departmentsResponse = await api.getDepartmentsByDoctor(doctorData.id, 1, 100, 'name', false, token)
        setDepartments(departmentsResponse.results)

        // Fetch upcoming schedules for the doctor
        const schedulesResponse = await api.getSchedulesByDoctor(doctorData.id, 1, 10, 'date', false, token)
        setSchedules(schedulesResponse.results)
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to load doctor details.",
          variant: "destructive",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchDoctorDetails()
  }, [id, router, toast])

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

  if (!doctor) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
            <CardDescription>Failed to load doctor details.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/doctors')}>Return to Doctors List</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>{doctor.name}</CardTitle>
          <CardDescription>{doctor.description || 'Specialist'}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h2 className="text-lg font-semibold">Contact Information</h2>
              <p><strong>Gender:</strong> {doctor.gender}</p>
              <p><strong>Email:</strong> {doctor.email}</p>
              <p><strong>Phone:</strong> {doctor.phone_number}</p>
            </div>

            <div>
              <h2 className="text-lg font-semibold">Departments</h2>
              {departments.length > 0 ? (
                <ul className="list-disc list-inside">
                  {departments.map((dept) => (
                    <li key={dept.id}>{dept.name}</li>
                  ))}
                </ul>
              ) : (
                <p>No departments assigned.</p>
              )}
            </div>

            <div>
              <h2 className="text-lg font-semibold">Upcoming Schedules</h2>
              {schedules.length > 0 ? (
                <ul className="space-y-2">
                  {schedules.map((schedule) => (
                    <li key={schedule.id} className="flex items-center justify-between">
                      <span>{new Date(schedule.date).toLocaleDateString()} {schedule.start_time} - {schedule.end_time}</span>
                      <Button 
                        onClick={() => router.push(`/book/${schedule.id}`)}
                      >
                        Book Appointment
                      </Button>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No upcoming schedules available.</p>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}