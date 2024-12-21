'use client'

import { use, useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Department, Doctor, Schedule } from '@/lib/types'
import { format, addDays, startOfToday } from 'date-fns'
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

const DAYS_OF_WEEK = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export default function DepartmentDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const [department, setDepartment] = useState<Department | null>(null)
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [schedules, setSchedules] = useState<(Schedule & { doctor: Doctor })[]>([])
  const [filteredSchedules, setFilteredSchedules] = useState<(Schedule & { doctor: Doctor })[]>([])
  const [selectedDate, setSelectedDate] = useState(startOfToday())
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    const fetchDepartmentDetails = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }

      try {
        // Fetch department details
        const departmentData = await api.getDepartment(parseInt(id), token)
        setDepartment(departmentData)

        // Fetch doctors associated with the department
        const doctorsResponse = await api.getDoctorsByDepartment(departmentData.id, 1, 100, 'name', false, token)
        setDoctors(doctorsResponse.results)

        // Fetch upcoming schedules for the department
        const schedulesResponse = await api.getSchedulesByDepartment(departmentData.id, 1, 100, 'date', false, token)
        
        // Fetch doctor details for each schedule and filter for next 7 days
        const today = startOfToday()
        const sevenDaysLater = addDays(today, 7)
        
        const schedulesWithDoctors = await Promise.all(
          schedulesResponse.results
            .filter(schedule => {
              const scheduleDate = new Date(schedule.date)
              return scheduleDate >= today && scheduleDate < sevenDaysLater
            })
            .map(async (schedule) => {
              const doctor = await api.getDoctor(schedule.doctor_id, token)
              return { ...schedule, doctor }
            })
        )
        setSchedules(schedulesWithDoctors)
        setFilteredSchedules(schedulesWithDoctors.filter(schedule => 
          format(new Date(schedule.date), 'yyyy-MM-dd') === format(selectedDate, 'yyyy-MM-dd')
        ))
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to load department details.",
          variant: "destructive",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchDepartmentDetails()
  }, [id, router, toast, selectedDate])

  const handleDateSelect = (date: Date) => {
    setSelectedDate(date)
    setFilteredSchedules(schedules.filter(schedule => 
      format(new Date(schedule.date), 'yyyy-MM-dd') === format(date, 'yyyy-MM-dd')
    ))
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

  if (!department) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
            <CardDescription>Failed to load department details.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/departments')}>Return to Departments</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>{department?.name}</CardTitle>
          <CardDescription>{department?.description || 'No description available.'}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold mb-2">Doctors</h2>
              {doctors.length > 0 ? (
                <ul className="space-y-2 divide-y divide-gray-200">
                  {doctors.map((doctor, index) => (
                    <li 
                      key={doctor.id} 
                      className={`flex items-center justify-between p-2 ${
                        index % 2 === 0 ? 'bg-gray-50' : 'bg-white'
                      }`}
                    >
                      <span className="font-medium">
                        {doctor.name} (ID: {doctor.id})
                      </span>
                      <Button 
                        onClick={() => router.push(`/doctors/${doctor.id}`)}
                        variant="outline"
                      >
                        View Doctor
                      </Button>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No doctors assigned to this department.</p>
              )}
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-4">Upcoming Schedules</h2>
              <div className="border rounded-lg overflow-hidden">
                {/* Calendar Header */}
                <div className="grid grid-cols-7 bg-muted">
                  {DAYS_OF_WEEK.map((day, index) => {
                    const date = addDays(startOfToday(), index)
                    const isSelected = format(date, 'yyyy-MM-dd') === format(selectedDate, 'yyyy-MM-dd')
                    return (
                      <button
                        key={day}
                        onClick={() => handleDateSelect(date)}
                        className={`
                          p-2 text-center transition-colors
                          ${isSelected ? 'bg-primary text-primary-foreground' : 'hover:bg-muted-foreground/10'}
                        `}
                      >
                        <div className="font-medium">{day}</div>
                        <div className="text-xs mt-1">{format(date, 'MM/dd')}</div>
                      </button>
                    )
                  })}
                </div>

                {/* Schedule Content */}
                <div className="divide-y divide-border">
                  {filteredSchedules.length > 0 ? (
                    filteredSchedules.map((schedule, index) => (
                      <div 
                        key={schedule.id}
                        className={`
                          grid grid-cols-[1.5fr,2fr,1fr,1fr] gap-4 p-4 items-center
                          ${index % 2 === 0 ? 'bg-background' : 'bg-muted/30'}
                        `}
                      >
                        <div className="space-y-1">
                          <div className="font-medium">Time</div>
                          <div>{schedule.start_time} - {schedule.end_time}</div>
                        </div>
                        <div className="space-y-1">
                          <div className="font-medium">Doctor</div>
                          <div>{schedule.doctor.name}</div>
                        </div>
                        <div className="space-y-1 text-sm">
                          <div className="font-medium">Availability</div>
                          <div className={`${
                            schedule.available_slots > 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {schedule.max_appointments - schedule.available_slots} / {schedule.max_appointments} slots
                          </div>
                        </div>
                        <div className="text-right">
                          <Button 
                            onClick={() => router.push(`/book/${schedule.id}`)}
                            size="sm"
                            disabled={schedule.available_slots === 0}
                            variant={schedule.available_slots > 0 ? "default" : "secondary"}
                          >
                            {schedule.available_slots > 0 ? 'Book' : 'Full'}
                          </Button>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="p-8 text-center text-muted-foreground">
                      No schedules available for {format(selectedDate, 'MMMM d, yyyy')}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}