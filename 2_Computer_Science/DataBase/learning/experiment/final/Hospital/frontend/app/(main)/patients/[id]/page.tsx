'use client'

import { use, useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Patient, Registration } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog"
import { useToast } from "@/hooks/use-toast"

export default function PatientDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const [patient, setPatient] = useState<Patient | null>(null)
  const [appointments, setAppointments] = useState<Registration[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [editedPatient, setEditedPatient] = useState<Partial<Patient>>({})
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    const fetchPatientDetails = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }

      try {
        const patientData = await api.getPatient(parseInt(id), token)
        setPatient(patientData)
        setEditedPatient(patientData)

        const appointmentsResponse = await api.getRegistrationsByPatient(patientData.id, 1, 10, 'id', false, token)
        setAppointments(appointmentsResponse.results)
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to load patient details.",
          variant: "destructive",
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchPatientDetails()
  }, [id, router, toast])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEditedPatient({ ...editedPatient, [e.target.name]: e.target.value })
  }

  const handleSelectChange = (value: string) => {
    setEditedPatient({ ...editedPatient, gender: value })
  }

  const handleUpdatePatient = async () => {
    setIsSubmitting(true)
    const token = localStorage.getItem('token')
    if (!token || !patient) return

    try {
      const updatedPatient = await api.updatePatient(patient.id, editedPatient, token)
      setPatient(updatedPatient)
      setIsEditing(false)
      toast({
        title: "Success",
        description: "Patient information updated successfully.",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update patient information.",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeletePatient = async () => {
    setIsSubmitting(true)
    const token = localStorage.getItem('token')
    if (!token || !patient) return

    try {
      await api.deletePatient(patient.id, token)
      toast({
        title: "Success",
        description: "Patient deleted successfully.",
      })
      router.push('/patients')
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete patient.",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
      setIsDeleteDialogOpen(false)
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

  if (!patient) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
            <CardDescription>Failed to load patient details.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/patients')}>Return to Patients</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>{patient.name}</CardTitle>
          <CardDescription>Patient ID: {patient.id}</CardDescription>
        </CardHeader>
        <CardContent>
          {isEditing ? (
            <form onSubmit={(e) => { e.preventDefault(); handleUpdatePatient(); }} className="space-y-4">
              <div>
                <Label htmlFor="name">Name</Label>
                <Input id="name" name="name" value={editedPatient.name} onChange={handleInputChange} />
              </div>
              <div>
                <Label htmlFor="gender">Gender</Label>
                <Select onValueChange={handleSelectChange} defaultValue={editedPatient.gender}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select gender" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="male">Male</SelectItem>
                    <SelectItem value="female">Female</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="birthday">Birthday</Label>
                <Input id="birthday" name="birthday" type="date" value={editedPatient.birthday} onChange={handleInputChange} />
              </div>
              <div>
                <Label htmlFor="phone_number">Phone Number</Label>
                <Input id="phone_number" name="phone_number" value={editedPatient.phone_number} onChange={handleInputChange} />
              </div>
            </form>
          ) : (
            <>
              <p><strong>Gender:</strong> {patient.gender}</p>
              <p><strong>Birthday:</strong> {new Date(patient.birthday).toLocaleDateString()}</p>
              <p><strong>Phone:</strong> {patient.phone_number}</p>
            </>
          )}
          
          <h2 className="text-xl font-semibold mt-6 mb-2">Recent Appointments</h2>
          {appointments.length > 0 ? (
            <ul className="space-y-4">
              {appointments.map((appointment) => (
                <li key={appointment.id} className="border-b pb-4">
                  <p><strong>Date:</strong> {new Date(appointment.created_at).toLocaleString()}</p>
                  <p><strong>Status:</strong> {appointment.status}</p>
                  <Button 
                    className="mt-2" 
                    onClick={() => router.push(`/appointments/${appointment.id}`)}
                  >
                    View Appointment
                  </Button>
                </li>
              ))}
            </ul>
          ) : (
            <p>No recent appointments.</p>
          )}
        </CardContent>
        <CardFooter className="flex justify-between">
          {isEditing ? (
            <>
              <Button type="submit" onClick={handleUpdatePatient} disabled={isSubmitting}>
                {isSubmitting ? 'Saving...' : 'Save Changes'}
              </Button>
              <Button type="button" variant="outline" onClick={() => setIsEditing(false)}>Cancel</Button>
            </>
          ) : (
            <>
              <Button onClick={() => setIsEditing(true)}>Edit Patient</Button>
              <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
                <DialogTrigger asChild>
                  <Button variant="destructive">Delete Patient</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Are you sure you want to delete this patient?</DialogTitle>
                  </DialogHeader>
                  <p>This action cannot be undone.</p>
                  <DialogFooter>
                    <Button variant="outline" onClick={() => setIsDeleteDialogOpen(false)}>Cancel</Button>
                    <Button variant="destructive" onClick={handleDeletePatient} disabled={isSubmitting}>
                      {isSubmitting ? 'Deleting...' : 'Delete'}
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </>
          )}
        </CardFooter>
      </Card>
    </div>
  )
}