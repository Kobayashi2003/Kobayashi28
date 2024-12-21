'use client'

import { use, useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Schedule, Doctor, Department, Patient } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Skeleton } from "@/components/ui/skeleton"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function BookAppointmentPage({ params }: { params: Promise<{ scheduleId: string }> }) {
  const { scheduleId } = use(params)
  const [schedule, setSchedule] = useState<Schedule | null>(null)
  const [doctor, setDoctor] = useState<Doctor | null>(null)
  const [department, setDepartment] = useState<Department | null>(null)
  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatient, setSelectedPatient] = useState<string>('')
  const [notes, setNotes] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    const fetchBookingDetails = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }

      try {
        const scheduleData = await api.getSchedule(parseInt(scheduleId), token)
        setSchedule(scheduleData)

        const doctorData = await api.getDoctor(scheduleData.doctor_id, token)
        setDoctor(doctorData)

        const departmentData = await api.getDepartment(scheduleData.department_id, token)
        setDepartment(departmentData)

        const userId = parseInt(localStorage.getItem('userId') || '0')
        const patientsResponse = await api.getUserPatients(userId, 1, 100, 'name', false, token)
        setPatients(patientsResponse.results)
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to load booking details.",
          variant: "destructive",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchBookingDetails()
  }, [scheduleId, router, toast])

  const handleBookAppointment = async (e: React.FormEvent) => {
    e.preventDefault()
    const token = localStorage.getItem('token')
    if (!token || !schedule || !selectedPatient) {
      toast({
        title: "Error",
        description: "Please select a patient and try again.",
        variant: "destructive",
      })
      return
    }

    setIsSubmitting(true)
    try {
      await api.createRegistration({
        patient_id: parseInt(selectedPatient),
        schedule_id: schedule.id,
        notes: notes
      }, token)

      toast({
        title: "Success",
        description: "Appointment booked successfully.",
      })
      router.push('/appointments')
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to book appointment. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
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

  if (!schedule || !doctor || !department) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
            <CardDescription>Failed to load booking details.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/doctors')}>Return to Doctors</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Book Appointment</CardTitle>
          <CardDescription>Schedule an appointment with Dr. {doctor.name}</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleBookAppointment} className="space-y-4">
            <div>
              <Label>Doctor</Label>
              <Input value={doctor.name} disabled />
            </div>
            <div>
              <Label>Department</Label>
              <Input value={department.name} disabled />
            </div>
            <div>
              <Label>Date</Label>
              <Input value={new Date(schedule.date).toLocaleDateString()} disabled />
            </div>
            <div>
              <Label>Time</Label>
              <Input value={`${schedule.start_time} - ${schedule.end_time}`} disabled />
            </div>
            <div>
              <Label>Patient</Label>
              <Select value={selectedPatient} onValueChange={setSelectedPatient} required>
                <SelectTrigger>
                  <SelectValue placeholder="Select a patient" />
                </SelectTrigger>
                <SelectContent>
                  {patients.map((patient) => (
                    <SelectItem key={patient.id} value={patient.id.toString()}>
                      {patient.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="notes">Notes</Label>
              <Textarea
                id="notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Any additional notes for the appointment"
              />
            </div>
          </form>
        </CardContent>
        <CardFooter>
          <Button type="submit" onClick={handleBookAppointment} disabled={isSubmitting}>
            {isSubmitting ? 'Booking...' : 'Book Appointment'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}