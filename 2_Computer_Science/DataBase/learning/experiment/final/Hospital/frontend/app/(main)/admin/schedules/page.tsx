'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Schedule, PaginatedResponse } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { useToast } from '@/hooks/use-toast'

export default function ScheduleManagementPage() {
  const [schedules, setSchedules] = useState<Schedule[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [currentQuery, setCurrentQuery] = useState('')
  const [isSearchMode, setIsSearchMode] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [editingSchedule, setEditingSchedule] = useState<Schedule | null>(null)
  const router = useRouter()
  const { toast } = useToast()

  const fetchSchedules = async (currentPage: number, query: string = '') => {
    setIsLoading(true)
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      let response: PaginatedResponse<Schedule>;
      if (isSearchMode && query) {
        response = await api.searchSchedules(query, currentPage, 10, 'id', false, token)
      } else {
        response = await api.getSchedules(currentPage, 10, 'id', false, token)
      }
      setSchedules(response.results)
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      console.error('Failed to fetch schedules', error)
      toast({
        title: "Error",
        description: "Failed to load schedules.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchSchedules(page, currentQuery)
  }, [page, isSearchMode, currentQuery])

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSearchMode(true)
    setCurrentQuery(searchQuery)
    setPage(1)
    fetchSchedules(1, searchQuery)
  }

  const handleClearSearch = () => {
    setSearchQuery('')
    setCurrentQuery('')
    setIsSearchMode(false)
    setPage(1)
    fetchSchedules(1, '')
  }

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
  }

  const handleCreateSchedule = async (scheduleData: Omit<Schedule, 'id' | 'created_at' | 'updated_at'>) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.createSchedule(scheduleData, token)
      toast({
        title: "Success",
        description: "Schedule created successfully.",
      })
      fetchSchedules(page, currentQuery)
    } catch (error) {
      console.error('Failed to create schedule', error)
      toast({
        title: "Error",
        description: "Failed to create schedule.",
        variant: "destructive",
      })
    }
  }

  const handleUpdateSchedule = async (scheduleId: number, scheduleData: Partial<Omit<Schedule, 'id' | 'created_at' | 'updated_at'>>) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.updateSchedule(scheduleId, scheduleData, token)
      toast({
        title: "Success",
        description: "Schedule updated successfully.",
      })
      fetchSchedules(page, currentQuery)
    } catch (error) {
      console.error('Failed to update schedule', error)
      toast({
        title: "Error",
        description: "Failed to update schedule.",
        variant: "destructive",
      })
    }
  }

  const handleDeleteSchedule = async (scheduleId: number) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.deleteSchedule(scheduleId, token)
      toast({
        title: "Success",
        description: "Schedule deleted successfully.",
      })
      fetchSchedules(page, currentQuery)
    } catch (error) {
      console.error('Failed to delete schedule', error)
      toast({
        title: "Error",
        description: "Failed to delete schedule.",
        variant: "destructive",
      })
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Schedule Management</h1>
      <div className="mb-4 flex justify-between items-center">
        <form onSubmit={handleSearch} className="flex-1 mr-4">
          <div className="flex">
            <Input
              placeholder="Search schedules..."
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
            <Button>Create Schedule</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Schedule</DialogTitle>
            </DialogHeader>
            <form onSubmit={(e) => {
              e.preventDefault()
              const formData = new FormData(e.currentTarget)
              handleCreateSchedule({
                doctor_id: Number(formData.get('doctor_id')),
                department_id: Number(formData.get('department_id')),
                date: formData.get('date') as string,
                start_time: formData.get('start_time') as string,
                end_time: formData.get('end_time') as string,
                max_appointments: Number(formData.get('max_appointments')),
                available_slots: Number(formData.get('available_slots')),
              })
            }}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="doctor_id" className="text-right">
                    Doctor ID
                  </Label>
                  <Input id="doctor_id" name="doctor_id" type="number" required className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="department_id" className="text-right">
                    Department ID
                  </Label>
                  <Input id="department_id" name="department_id" type="number" required className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="date" className="text-right">
                    Date
                  </Label>
                  <Input id="date" name="date" type="date" required className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="start_time" className="text-right">
                    Start Time
                  </Label>
                  <Input id="start_time" name="start_time" type="time" required className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="end_time" className="text-right">
                    End Time
                  </Label>
                  <Input id="end_time" name="end_time" type="time" required className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="max_appointments" className="text-right">
                    Max Appointments
                  </Label>
                  <Input id="max_appointments" name="max_appointments" type="number" required className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="available_slots" className="text-right">
                    Available Slots
                  </Label>
                  <Input id="available_slots" name="available_slots" type="number" required className="col-span-3" />
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
            <TableHead>Doctor ID</TableHead>
            <TableHead>Department ID</TableHead>
            <TableHead>Date</TableHead>
            <TableHead>Start Time</TableHead>
            <TableHead>End Time</TableHead>
            <TableHead>Max Appointments</TableHead>
            <TableHead>Available Slots</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {schedules.map((schedule) => (
            <TableRow key={schedule.id}>
              <TableCell>{schedule.id}</TableCell>
              <TableCell>{schedule.doctor_id}</TableCell>
              <TableCell>{schedule.department_id}</TableCell>
              <TableCell>{schedule.date}</TableCell>
              <TableCell>{schedule.start_time}</TableCell>
              <TableCell>{schedule.end_time}</TableCell>
              <TableCell>{schedule.max_appointments}</TableCell>
              <TableCell>{schedule.available_slots}</TableCell>
              <TableCell>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="mr-2" onClick={() => setEditingSchedule(schedule)}>Edit</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Edit Schedule</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={(e) => {
                      e.preventDefault()
                      const formData = new FormData(e.currentTarget)
                      const updatedData: Partial<Omit<Schedule, 'id' | 'created_at' | 'updated_at'>> = {}
                      if (formData.get('doctor_id')) updatedData.doctor_id = Number(formData.get('doctor_id'))
                      if (formData.get('department_id')) updatedData.department_id = Number(formData.get('department_id'))
                      if (formData.get('date')) updatedData.date = formData.get('date') as string
                      if (formData.get('start_time')) updatedData.start_time = formData.get('start_time') as string
                      if (formData.get('end_time')) updatedData.end_time = formData.get('end_time') as string
                      if (formData.get('max_appointments')) updatedData.max_appointments = Number(formData.get('max_appointments'))
                      if (formData.get('available_slots')) updatedData.available_slots = Number(formData.get('available_slots'))
                      handleUpdateSchedule(schedule.id, updatedData)
                    }}>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-doctor_id" className="text-right">
                            Doctor ID
                          </Label>
                          <Input id="edit-doctor_id" name="doctor_id" type="number" defaultValue={editingSchedule?.doctor_id} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-department_id" className="text-right">
                            Department ID
                          </Label>
                          <Input id="edit-department_id" name="department_id" type="number" defaultValue={editingSchedule?.department_id} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-date" className="text-right">
                            Date
                          </Label>
                          <Input id="edit-date" name="date" type="date" defaultValue={editingSchedule?.date} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-start_time" className="text-right">
                            Start Time
                          </Label>
                          <Input id="edit-start_time" name="start_time" type="time" defaultValue={editingSchedule?.start_time} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-end_time" className="text-right">
                            End Time
                          </Label>
                          <Input id="edit-end_time" name="end_time" type="time" defaultValue={editingSchedule?.end_time} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-max_appointments" className="text-right">
                            Max Appointments
                          </Label>
                          <Input id="edit-max_appointments" name="max_appointments" type="number" defaultValue={editingSchedule?.max_appointments} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-available_slots" className="text-right">
                            Available Slots
                          </Label>
                          <Input id="edit-available_slots" name="available_slots" type="number" defaultValue={editingSchedule?.available_slots} className="col-span-3" />
                        </div>
                      </div>
                      <div className="flex justify-end">
                        <Button type="submit">Update</Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
                <Button variant="destructive" onClick={() => handleDeleteSchedule(schedule.id)}>Delete</Button>
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