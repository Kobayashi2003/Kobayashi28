'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Schedule } from '@/lib/types'
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
      let response;
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
    fetchSchedules(newPage, currentQuery)
  }

  const handleCreateSchedule = async (scheduleData: Omit<Schedule, 'id'>) => {
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

  const handleUpdateSchedule = async (scheduleId: number, scheduleData: Partial<Schedule>) => {
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
            <Button type="submit">Search</Button>
            {isSearchMode && (
              <Button type="button" onClick={handleClearSearch} variant="outline" className="ml-2">
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
              handleCreateSchedule(Object.fromEntries(formData) as any)
            }}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="doctor_id" className="text-right">
                    Doctor ID
                  </Label>
                  <Input id="doctor_id" name="doctor_id" type="number" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="start_time" className="text-right">
                    Start Time
                  </Label>
                  <Input id="start_time" name="start_time" type="datetime-local" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="end_time" className="text-right">
                    End Time
                  </Label>
                  <Input id="end_time" name="end_time" type="datetime-local" className="col-span-3" />
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
            <TableHead>Start Time</TableHead>
            <TableHead>End Time</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {schedules.map((schedule) => (
            <TableRow key={schedule.id}>
              <TableCell>{schedule.id}</TableCell>
              <TableCell>{schedule.doctor_id}</TableCell>
              <TableCell>{new Date(schedule.start_time).toLocaleString()}</TableCell>
              <TableCell>{new Date(schedule.end_time).toLocaleString()}</TableCell>
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
                      handleUpdateSchedule(schedule.id, Object.fromEntries(formData) as any)
                    }}>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-doctor_id" className="text-right">
                            Doctor ID
                          </Label>
                          <Input id="edit-doctor_id" name="doctor_id" type="number" defaultValue={editingSchedule?.doctor_id} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-start_time" className="text-right">
                            Start Time
                          </Label>
                          <Input id="edit-start_time" name="start_time" type="datetime-local" defaultValue={editingSchedule?.start_time} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-end_time" className="text-right">
                            End Time
                          </Label>
                          <Input id="edit-end_time" name="end_time" type="datetime-local" defaultValue={editingSchedule?.end_time} className="col-span-3" />
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
        <Button onClick={() => handlePageChange(page - 1)} disabled={page === 1}>Previous</Button>
        <span>Page {page} of {totalPages}</span>
        <Button onClick={() => handlePageChange(page + 1)} disabled={page === totalPages}>Next</Button>
      </div>
    </div>
  )
}

