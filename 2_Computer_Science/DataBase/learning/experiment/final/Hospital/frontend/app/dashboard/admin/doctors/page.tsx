'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Doctor } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { useToast } from '@/hooks/use-toast'

export default function DoctorManagementPage() {
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [isSearchMode, setIsSearchMode] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [currentQuery, setCurrentQuery] = useState('')
  const [editingDoctor, setEditingDoctor] = useState<Doctor | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  const fetchDoctors = async (currentPage: number, query: string = '') => {
    setIsLoading(true)
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      let response;
      if (isSearchMode && query) {
        response = await api.searchDoctors(query, currentPage, 10, 'id', false, token)
      } else {
        response = await api.getDoctors(currentPage, 10, 'id', false, token)
      }
      setDoctors(response.results)
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      console.error('Failed to fetch doctors', error)
      toast({
        title: "Error",
        description: "Failed to load doctors.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchDoctors(page, currentQuery) // Using currentQuery instead of searchQuery
  }, [page, isSearchMode, currentQuery]) // Added currentQuery to dependency array

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSearchMode(true)
    setCurrentQuery(searchQuery) // Update currentQuery
    setPage(1)
    fetchDoctors(1, searchQuery)
  }

  const handleClearSearch = () => {
    setSearchQuery('')
    setCurrentQuery('') // Clear currentQuery
    setIsSearchMode(false)
    setPage(1)
    fetchDoctors(1, '')
  }

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
    fetchDoctors(newPage, currentQuery) // Using currentQuery
  }

  const handleCreateDoctor = async (doctorData: Omit<Doctor, 'id' | 'created_at' | 'updated_at'>) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.createDoctor(doctorData, token)
      toast({
        title: "Success",
        description: "Doctor created successfully.",
      })
      fetchDoctors(page, searchQuery)
    } catch (error) {
      console.error('Failed to create doctor', error)
      toast({
        title: "Error",
        description: "Failed to create doctor.",
        variant: "destructive",
      })
    }
  }

  const handleUpdateDoctor = async (doctorId: number, doctorData: Partial<Doctor>) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.updateDoctor(doctorId, doctorData, token)
      toast({
        title: "Success",
        description: "Doctor updated successfully.",
      })
      fetchDoctors(page, searchQuery)
    } catch (error) {
      console.error('Failed to update doctor', error)
      toast({
        title: "Error",
        description: "Failed to update doctor.",
        variant: "destructive",
      })
    }
  }

  const handleDeleteDoctor = async (doctorId: number) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.deleteDoctor(doctorId, token)
      toast({
        title: "Success",
        description: "Doctor deleted successfully.",
      })
      fetchDoctors(page, searchQuery)
    } catch (error) {
      console.error('Failed to delete doctor', error)
      toast({
        title: "Error",
        description: "Failed to delete doctor.",
        variant: "destructive",
      })
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Doctor Management</h1>
      <div className="mb-4 flex justify-between items-center">
        <form onSubmit={handleSearch} className="flex-1 mr-4">
          <div className="flex">
            <Input
              placeholder="Search doctors..."
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
            <Button>Create Doctor</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Doctor</DialogTitle>
            </DialogHeader>
            <form onSubmit={(e) => {
              e.preventDefault()
              const formData = new FormData(e.currentTarget)
              handleCreateDoctor(Object.fromEntries(formData) as any)
            }}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">
                    Name
                  </Label>
                  <Input id="name" name="name" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="gender" className="text-right">
                    Gender
                  </Label>
                  <Input id="gender" name="gender" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="email" className="text-right">
                    Email
                  </Label>
                  <Input id="email" name="email" type="email" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="phone_number" className="text-right">
                    Phone Number
                  </Label>
                  <Input id="phone_number" name="phone_number" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="description" className="text-right">
                    Description
                  </Label>
                  <Input id="description" name="description" className="col-span-3" />
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
            <TableHead>Name</TableHead>
            <TableHead>Gender</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Phone Number</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {doctors.map((doctor) => (
            <TableRow key={doctor.id}>
              <TableCell>{doctor.id}</TableCell>
              <TableCell>{doctor.name}</TableCell>
              <TableCell>{doctor.gender}</TableCell>
              <TableCell>{doctor.email}</TableCell>
              <TableCell>{doctor.phone_number}</TableCell>
              <TableCell>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="mr-2" onClick={() => setEditingDoctor(doctor)}>Edit</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Edit Doctor</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={(e) => {
                      e.preventDefault()
                      const formData = new FormData(e.currentTarget)
                      handleUpdateDoctor(doctor.id, Object.fromEntries(formData) as any)
                    }}>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-name" className="text-right">
                            Name
                          </Label>
                          <Input id="edit-name" name="name" defaultValue={editingDoctor?.name} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-gender" className="text-right">
                            Gender
                          </Label>
                          <Input id="edit-gender" name="gender" defaultValue={editingDoctor?.gender} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-email" className="text-right">
                            Email
                          </Label>
                          <Input id="edit-email" name="email" type="email" defaultValue={editingDoctor?.email} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-phone_number" className="text-right">
                            Phone Number
                          </Label>
                          <Input id="edit-phone_number" name="phone_number" defaultValue={editingDoctor?.phone_number} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-description" className="text-right">
                            Description
                          </Label>
                          <Input id="edit-description" name="description" defaultValue={editingDoctor?.description} className="col-span-3" />
                        </div>
                      </div>
                      <div className="flex justify-end">
                        <Button type="submit">Update</Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
                <Button variant="destructive" onClick={() => handleDeleteDoctor(doctor.id)}>Delete</Button>
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