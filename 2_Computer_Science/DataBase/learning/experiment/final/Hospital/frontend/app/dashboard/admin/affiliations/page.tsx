'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Affiliation, Doctor, Department, PaginatedResponse } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { useToast } from '@/hooks/use-toast'

export default function AffiliationManagementPage() {
  const [affiliations, setAffiliations] = useState<Affiliation[]>([])
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [departments, setDepartments] = useState<Department[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [currentQuery, setCurrentQuery] = useState('')
  const [isSearchMode, setIsSearchMode] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [editingAffiliation, setEditingAffiliation] = useState<Affiliation | null>(null)
  const router = useRouter()
  const { toast } = useToast()

  const fetchAffiliations = async (currentPage: number, query: string = '') => {
    setIsLoading(true)
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      let response: PaginatedResponse<Affiliation>;
      if (isSearchMode && query) {
        response = await api.searchAffiliations(query, currentPage, 10, 'id', false, token)
      } else {
        response = await api.getAffiliations(currentPage, 10, 'id', false, token)
      }
      setAffiliations(response.results)
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      console.error('Failed to fetch affiliations', error)
      toast({
        title: "Error",
        description: "Failed to load affiliations.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const fetchDoctorsAndDepartments = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const [doctorsResponse, departmentsResponse] = await Promise.all([
        api.getDoctors(1, 1000, 'id', false, token),
        api.getDepartments(1, 1000, 'id', false, token)
      ])
      setDoctors(doctorsResponse.results)
      setDepartments(departmentsResponse.results)
    } catch (error) {
      console.error('Failed to fetch doctors and departments', error)
      toast({
        title: "Error",
        description: "Failed to load doctors and departments.",
        variant: "destructive",
      })
    }
  }

  useEffect(() => {
    fetchAffiliations(page, currentQuery)
    fetchDoctorsAndDepartments()
  }, [page, isSearchMode, currentQuery])

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSearchMode(true)
    setCurrentQuery(searchQuery)
    setPage(1)
    fetchAffiliations(1, searchQuery)
  }

  const handleClearSearch = () => {
    setSearchQuery('')
    setCurrentQuery('')
    setIsSearchMode(false)
    setPage(1)
    fetchAffiliations(1, '')
  }

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
    fetchAffiliations(newPage, currentQuery)
  }

  const handleCreateAffiliation = async (affiliationData: { doctor_id: number; department_id: number }) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.createAffiliation(affiliationData, token)
      toast({
        title: "Success",
        description: "Affiliation created successfully.",
      })
      fetchAffiliations(page, currentQuery)
    } catch (error) {
      console.error('Failed to create affiliation', error)
      toast({
        title: "Error",
        description: "Failed to create affiliation.",
        variant: "destructive",
      })
    }
  }

  const handleUpdateAffiliation = async (affiliationId: number, affiliationData: { doctor_id: number; department_id: number }) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.updateAffiliation(affiliationId, affiliationData, token)
      toast({
        title: "Success",
        description: "Affiliation updated successfully.",
      })
      fetchAffiliations(page, currentQuery)
    } catch (error) {
      console.error('Failed to update affiliation', error)
      toast({
        title: "Error",
        description: "Failed to update affiliation.",
        variant: "destructive",
      })
    }
  }

  const handleDeleteAffiliation = async (affiliationId: number) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      await api.deleteAffiliation(affiliationId, token)
      toast({
        title: "Success",
        description: "Affiliation deleted successfully.",
      })
      fetchAffiliations(page, currentQuery)
    } catch (error) {
      console.error('Failed to delete affiliation', error)
      toast({
        title: "Error",
        description: "Failed to delete affiliation.",
        variant: "destructive",
      })
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Affiliation Management</h1>
      <div className="mb-4 flex justify-between items-center">
        <form onSubmit={handleSearch} className="flex-1 mr-4">
          <div className="flex">
            <Input
              placeholder="Search affiliations..."
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
            <Button>Create Affiliation</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Affiliation</DialogTitle>
            </DialogHeader>
            <form onSubmit={(e) => {
              e.preventDefault()
              const formData = new FormData(e.currentTarget)
              handleCreateAffiliation({
                doctor_id: Number(formData.get('doctor_id')),
                department_id: Number(formData.get('department_id'))
              })
            }}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="doctor_id" className="text-right">
                    Doctor
                  </Label>
                  <Select name="doctor_id">
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select a doctor" />
                    </SelectTrigger>
                    <SelectContent>
                      {doctors.map((doctor) => (
                        <SelectItem key={doctor.id} value={doctor.id.toString()}>
                          {doctor.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="department_id" className="text-right">
                    Department
                  </Label>
                  <Select name="department_id">
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select a department" />
                    </SelectTrigger>
                    <SelectContent>
                      {departments.map((department) => (
                        <SelectItem key={department.id} value={department.id.toString()}>
                          {department.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
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
            <TableHead>Doctor</TableHead>
            <TableHead>Department</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {affiliations.map((affiliation) => (
            <TableRow key={`${affiliation.doctor.id}-${affiliation.department.id}`}>
              <TableCell>{`${affiliation.doctor.id}-${affiliation.department.id}`}</TableCell>
              <TableCell>{affiliation.doctor.name}</TableCell>
              <TableCell>{affiliation.department.name}</TableCell>
              <TableCell>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="mr-2" onClick={() => setEditingAffiliation(affiliation)}>Edit</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Edit Affiliation</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={(e) => {
                      e.preventDefault()
                      const formData = new FormData(e.currentTarget)
                      handleUpdateAffiliation(
                        Number(`${affiliation.doctor.id}${affiliation.department.id}`),
                        {
                          doctor_id: Number(formData.get('doctor_id')),
                          department_id: Number(formData.get('department_id'))
                        }
                      )
                    }}>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-doctor_id" className="text-right">
                            Doctor
                          </Label>
                          <Select name="doctor_id" defaultValue={affiliation.doctor.id.toString()}>
                            <SelectTrigger className="col-span-3">
                              <SelectValue placeholder="Select a doctor" />
                            </SelectTrigger>
                            <SelectContent>
                              {doctors.map((doctor) => (
                                <SelectItem key={doctor.id} value={doctor.id.toString()}>
                                  {doctor.name}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="edit-department_id" className="text-right">
                            Department
                          </Label>
                          <Select name="department_id" defaultValue={affiliation.department.id.toString()}>
                            <SelectTrigger className="col-span-3">
                              <SelectValue placeholder="Select a department" />
                            </SelectTrigger>
                            <SelectContent>
                              {departments.map((department) => (
                                <SelectItem key={department.id} value={department.id.toString()}>
                                  {department.name}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      <div className="flex justify-end">
                        <Button type="submit">Update</Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
                <Button variant="destructive" onClick={() => handleDeleteAffiliation(Number(`${affiliation.doctor.id}${affiliation.department.id}`))}>Delete</Button>
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