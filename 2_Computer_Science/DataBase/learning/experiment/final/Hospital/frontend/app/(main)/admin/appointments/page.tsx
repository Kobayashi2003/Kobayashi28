'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Registration, PaginatedResponse } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { useToast } from '@/hooks/use-toast'

export default function AppointmentManagementPage() {
  const [appointments, setAppointments] = useState<Registration[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [currentQuery, setCurrentQuery] = useState('')
  const [isSearchMode, setIsSearchMode] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [editingAppointment, setEditingAppointment] = useState<Registration | null>(null)
  const router = useRouter()
  const { toast } = useToast()

  const fetchAppointments = async (currentPage: number, query: string = '') => {
    setIsLoading(true)
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      let response: PaginatedResponse<Registration>;
      if (isSearchMode && query) {
        response = await api.searchRegistrations(query, currentPage, 10, 'id', false, token)
      } else {
        response = await api.getRegistrations(currentPage, 10, 'id', false, token)
      }
      setAppointments(response.results)
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      console.error('Failed to fetch appointments', error)
      toast({
        title: "Error",
        description: "Failed to load appointments.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchAppointments(page, currentQuery)
  }, [page, isSearchMode, currentQuery])

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSearchMode(true)
    setCurrentQuery(searchQuery)
    setPage(1)
    fetchAppointments(1, searchQuery)
  }

  const handleClearSearch = () => {
    setSearchQuery('')
    setCurrentQuery('')
    setIsSearchMode(false)
    setPage(1)
    fetchAppointments(1, '')
  }

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
  }

  const handleCreateAppointment = async (appointmentData: Omit<Registration, 'id' | 'status' | 'created_at' | 'updated_at'>) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.createRegistration(appointmentData, token)
      toast({
        title: "Success",
        description: "Registration created successfully.",
      })
      fetchAppointments(page, currentQuery)
    } catch (error) {
      console.error('Failed to create appointment', error)
      toast({
        title: "Error",
        description: "Failed to create appointment.",
        variant: "destructive",
      })
    }
  }

  const handleUpdateAppointment = async (appointmentId: number, appointmentData: Partial<Omit<Registration, 'id' | 'status' | 'created_at' | 'updated_at'>>) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.updateRegistration(appointmentId, appointmentData, token)
      toast({
        title: "Success",
        description: "Registration updated successfully.",
      })
      fetchAppointments(page, currentQuery)
    } catch (error) {
      console.error('Failed to update appointment', error)
      toast({
        title: "Error",
        description: "Failed to update appointment.",
        variant: "destructive",
      })
    }
  }

  const handleDeleteAppointment = async (appointmentId: number) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.deleteRegistration(appointmentId, token)
      toast({
        title: "Success",
        description: "Registration deleted successfully.",
      })
      fetchAppointments(page, currentQuery)
    } catch (error) {
      console.error('Failed to delete appointment', error)
      toast({
        title: "Error",
        description: "Failed to delete appointment.",
        variant: "destructive",
      })
    }
  }

  const handleCancelAppointment = async (appointmentId: number) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.cancelRegistration(appointmentId, token)
      toast({
        title: "Success",
        description: "Registration cancelled successfully.",
      })
      fetchAppointments(page, currentQuery)
    } catch (error) {
      console.error('Failed to cancel appointment', error)
      toast({
        title: "Error",
        description: "Failed to cancel appointment.",
        variant: "destructive",
      })
    }
  }

  const handleCompleteAppointment = async (appointmentId: number) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.completeRegistration(appointmentId, token)
      toast({
        title: "Success",
        description: "Registration completed successfully.",
      })
      fetchAppointments(page, currentQuery)
    } catch (error) {
      console.error('Failed to complete appointment', error)
      toast({
        title: "Error",
        description: "Failed to complete appointment.",
        variant: "destructive",
      })
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Registration Management</h1>
      <div className="mb-4 flex justify-between items-center">
        <form onSubmit={handleSearch} className="flex-1 mr-4">
          <div className="flex">
            <Input
              placeholder="Search appointments..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="mr-2"
            />
            <Button type="submit" disabled={isLoading}>Search</Button>
            {isSearchMode && (
              <Button type="button" onClick={handleClearSearch} variant="outline" className="ml-2" disabled={isLoading}>
                Clear Search
              </Button>
            )}
          </div>
        </form>
        <Dialog>
          <DialogTrigger asChild>
            <Button>Create Registration</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Registration</DialogTitle>
            </DialogHeader>
            <form onSubmit={(e) => {
              e.preventDefault()
              const formData = new FormData(e.currentTarget)
              handleCreateAppointment({
                patient_id: Number(formData.get('patient_id')),
                schedule_id: Number(formData.get('schedule_id')),
                notes: formData.get('notes') as string,
              })
            }}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="patient_id" className="text-right">
                    Patient ID
                  </Label>
                  <Input id="patient_id" name="patient_id" type="number" required className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="schedule_id" className="text-right">
                    Schedule ID
                  </Label>
                  <Input id="schedule_id" name="schedule_id" type="number" required className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="notes" className="text-right">
                    Notes
                  </Label>
                  <Input id="notes" name="notes" className="col-span-3" />
                </div>
              </div>
              <div className="flex justify-end">
                <Button type="submit">Create</Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Patient ID</TableHead>
            <TableHead>Schedule ID</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Notes</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {appointments.map((appointment) => (
            <TableRow key={appointment.id}>
              <TableCell>{appointment.id}</TableCell>
              <TableCell>{appointment.patient_id}</TableCell>
              <TableCell>{appointment.schedule_id}</TableCell>
              <TableCell>{appointment.status}</TableCell>
              <TableCell>{appointment.notes}</TableCell>
              <TableCell>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="mr-2" onClick={() => setEditingAppointment(appointment)}>Edit</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Edit Registration</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={(e) => {
                      e.preventDefault()
                      const formData = new FormData(e.currentTarget)
                      const updatedData: Partial<Omit<Registration, 'id' | 'status' | 'created_at' | 'updated_at'>> = {}
                      if (formData.get('patient_id')) updatedData.patient_id = Number(formData.get('patient_id'))
                      if (formData.get('schedule_id')) updatedData.schedule_id = Number(formData.get('schedule_id'))
                      if (formData.get('notes')) updatedData.notes = formData.get('notes') as string
                      handleUpdateAppointment(appointment.id, updatedData)
                    }}>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-patient_id" className="text-right">
                            Patient ID
                          </Label>
                          <Input id="edit-patient_id" name="patient_id" type="number" defaultValue={editingAppointment?.patient_id} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-schedule_id" className="text-right">
                            Schedule ID
                          </Label>
                          <Input id="edit-schedule_id" name="schedule_id" type="number" defaultValue={editingAppointment?.schedule_id} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-notes" className="text-right">
                            Notes
                          </Label>
                          <Input id="edit-notes" name="notes" defaultValue={editingAppointment?.notes} className="col-span-3" />
                        </div>
                      </div>
                      <div className="flex justify-end">
                        <Button type="submit">Update</Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
                <Button variant="destructive" onClick={() => handleDeleteAppointment(appointment.id)} className="mr-2">Delete</Button>
                {appointment.status === 'scheduled' && (
                  <>
                    <Button onClick={() => handleCancelAppointment(appointment.id)} className="mr-2">Cancel</Button>
                    <Button onClick={() => handleCompleteAppointment(appointment.id)}>Complete</Button>
                  </>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className="mt-4 flex justify-between">
        <Button onClick={() => handlePageChange(page - 1)} disabled={page === 1 || isLoading}>Previous</Button>
        <span>Page {page} of {totalPages}</span>
        <Button onClick={() => handlePageChange(page + 1)} disabled={page === totalPages || isLoading}>Next</Button>
      </div>
    </div>
  )
}