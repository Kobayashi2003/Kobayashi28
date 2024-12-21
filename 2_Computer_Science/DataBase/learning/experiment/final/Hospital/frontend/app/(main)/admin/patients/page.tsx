'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Patient, PaginatedResponse } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { useToast } from '@/hooks/use-toast'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function PatientManagementPage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [currentQuery, setCurrentQuery] = useState('')
  const [isSearchMode, setIsSearchMode] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [editingPatient, setEditingPatient] = useState<Patient | null>(null)
  const router = useRouter()
  const { toast } = useToast()

  const fetchPatients = async (currentPage: number, query: string = '') => {
    setIsLoading(true)
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      let response: PaginatedResponse<Patient>;
      if (isSearchMode && query) {
        response = await api.searchPatients(query, currentPage, 10, 'id', false, token)
      } else {
        response = await api.getPatients(currentPage, 10, 'id', false, token)
      }
      setPatients(response.results)
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      console.error('Failed to fetch patients', error)
      toast({
        title: "Error",
        description: "Failed to load patients.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchPatients(page, currentQuery)
  }, [page, isSearchMode, currentQuery])

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSearchMode(true)
    setCurrentQuery(searchQuery)
    setPage(1)
    fetchPatients(1, searchQuery)
  }

  const handleClearSearch = () => {
    setSearchQuery('')
    setCurrentQuery('')
    setIsSearchMode(false)
    setPage(1)
    fetchPatients(1, '')
  }

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
  }

  const handleCreatePatient = async (patientData: Omit<Patient, 'id' | 'created_at' | 'updated_at'>) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.createPatient(patientData, token)
      toast({
        title: "Success",
        description: "Patient created successfully.",
      })
      fetchPatients(page, currentQuery)
    } catch (error) {
      console.error('Failed to create patient', error)
      toast({
        title: "Error",
        description: "Failed to create patient.",
        variant: "destructive",
      })
    }
  }

  const handleUpdatePatient = async (patientId: number, patientData: Partial<Patient>) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.updatePatient(patientId, patientData, token)
      toast({
        title: "Success",
        description: "Patient updated successfully.",
      })
      fetchPatients(page, currentQuery)
    } catch (error) {
      console.error('Failed to update patient', error)
      toast({
        title: "Error",
        description: "Failed to update patient.",
        variant: "destructive",
      })
    }
  }

  const handleDeletePatient = async (patientId: number) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.deletePatient(patientId, token)
      toast({
        title: "Success",
        description: "Patient deleted successfully.",
      })
      fetchPatients(page, currentQuery)
    } catch (error) {
      console.error('Failed to delete patient', error)
      toast({
        title: "Error",
        description: "Failed to delete patient.",
        variant: "destructive",
      })
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Patient Management</h1>
      <div className="mb-4 flex justify-between items-center">
        <form onSubmit={handleSearch} className="flex-1 mr-4">
          <div className="flex">
            <Input
              placeholder="Search patients..."
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
            <Button>Create Patient</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Patient</DialogTitle>
            </DialogHeader>
            <form onSubmit={(e) => {
              e.preventDefault()
              const formData = new FormData(e.currentTarget)
              handleCreatePatient(Object.fromEntries(formData) as any)
            }}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="user_id" className="text-right">
                    User ID
                  </Label>
                  <Input id="user_id" name="user_id" type="number" className="col-span-3" required />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">
                    Name
                  </Label>
                  <Input id="name" name="name" className="col-span-3" required />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="gender" className="text-right">
                    Gender
                  </Label>
                  <Select name="gender" required>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select gender" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Male</SelectItem>
                      <SelectItem value="female">Female</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="birthday" className="text-right">
                    Birthday
                  </Label>
                  <Input id="birthday" name="birthday" type="date" className="col-span-3" required />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="phone_number" className="text-right">
                    Phone Number
                  </Label>
                  <Input id="phone_number" name="phone_number" className="col-span-3" required />
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
            <TableHead>User ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Gender</TableHead>
            <TableHead>Birthday</TableHead>
            <TableHead>Phone Number</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {patients.map((patient) => (
            <TableRow key={patient.id}>
              <TableCell>{patient.id}</TableCell>
              <TableCell>{patient.user_id}</TableCell>
              <TableCell>{patient.name}</TableCell>
              <TableCell>{patient.gender}</TableCell>
              <TableCell>{new Date(patient.birthday).toLocaleDateString()}</TableCell>
              <TableCell>{patient.phone_number}</TableCell>
              <TableCell>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="mr-2" onClick={() => setEditingPatient(patient)}>Edit</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Edit Patient</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={(e) => {
                      e.preventDefault()
                      const formData = new FormData(e.currentTarget)
                      handleUpdatePatient(patient.id, Object.fromEntries(formData) as any)
                    }}>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-user_id" className="text-right">
                            User ID
                          </Label>
                          <Input id="edit-user_id" name="user_id" type="number" defaultValue={editingPatient?.user_id} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-name" className="text-right">
                            Name
                          </Label>
                          <Input id="edit-name" name="name" defaultValue={editingPatient?.name} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-gender" className="text-right">
                            Gender
                          </Label>
                          <Select name="gender" defaultValue={editingPatient?.gender} required>
                            <SelectTrigger className="col-span-3">
                              <SelectValue placeholder="Select gender" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="male">Male</SelectItem>
                              <SelectItem value="female">Female</SelectItem>
                              <SelectItem value="other">Other</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-birthday" className="text-right">
                            Birthday
                          </Label>
                          <Input id="edit-birthday" name="birthday" type="date" defaultValue={editingPatient?.birthday.split('T')[0]} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-phone_number" className="text-right">
                            Phone Number
                          </Label>
                          <Input id="edit-phone_number" name="phone_number" defaultValue={editingPatient?.phone_number} className="col-span-3" required />
                        </div>
                      </div>
                      <div className="flex justify-end">
                        <Button type="submit">Update</Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
                <Button variant="destructive" onClick={() => handleDeletePatient(patient.id)}>Delete</Button>
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