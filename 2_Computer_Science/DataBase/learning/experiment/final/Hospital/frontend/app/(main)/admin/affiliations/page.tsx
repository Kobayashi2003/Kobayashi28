'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Department, Doctor, PaginatedResponse } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useToast } from "@/hooks/use-toast"

export default function AffiliationManagementPage() {
  const [mode, setMode] = useState<'department' | 'doctor'>('department')
  const [departments, setDepartments] = useState<Department[]>([])
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [selectedItemId, setSelectedItemId] = useState<number | null>(null)
  const [affiliatedItems, setAffiliatedItems] = useState<(Department | Doctor)[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [affiliatedPage, setAffiliatedPage] = useState(1)
  const [affiliatedTotalPages, setAffiliatedTotalPages] = useState(1)
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [selectedItemToAdd, setSelectedItemToAdd] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)
  const [availableItemsToAdd, setAvailableItemsToAdd] = useState<(Department | Doctor)[]>([])
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    fetchItems()
  }, [mode, page])

  useEffect(() => {
    if (selectedItemId) {
      fetchAffiliatedItems()
    }
  }, [mode, selectedItemId, affiliatedPage])

  const fetchItems = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    setIsLoading(true)
    try {
      let response: PaginatedResponse<Department | Doctor>
      if (mode === 'department') {
        response = await api.getDepartments(page, 10, 'id', false, token)
        setDepartments(response.results as Department[])
      } else {
        response = await api.getDoctors(page, 10, 'id', false, token)
        setDoctors(response.results as Doctor[])
      }
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      console.error(`Failed to fetch ${mode}s`, error)
      toast({
        title: "Error",
        description: `Failed to load ${mode}s.`,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const fetchAffiliatedItems = async () => {
    if (!selectedItemId) return

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    setIsLoading(true)
    try {
      let response: PaginatedResponse<Department | Doctor>
      if (mode === 'department') {
        response = await api.getDoctorsByDepartment(selectedItemId, affiliatedPage, 10, 'id', false, token)
      } else {
        response = await api.getDepartmentsByDoctor(selectedItemId, affiliatedPage, 10, 'id', false, token)
      }
      setAffiliatedItems(response.results)
      setAffiliatedTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      console.error(`Failed to fetch affiliated ${mode === 'department' ? 'doctors' : 'departments'}`, error)
      toast({
        title: "Error",
        description: `Failed to load affiliated ${mode === 'department' ? 'doctors' : 'departments'}.`,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const fetchAvailableItems = async () => {
    const token = localStorage.getItem('token')
    if (!token || !selectedItemId) {
      router.push('/login')
      return
    }

    setIsLoading(true)
    try {
      // Fetch all items first
      const response = await (mode === 'department'
        ? api.getDoctors(1, 100, 'name', false, token)
        : api.getDepartments(1, 100, 'name', false, token))

      // Get the IDs of already affiliated items
      const affiliatedIds = new Set(affiliatedItems.map(item => item.id))

      // Filter out already affiliated items
      const availableItems = response.results.filter(item => !affiliatedIds.has(item.id))
      
      setAvailableItemsToAdd(availableItems)
    } catch (error) {
      console.error(`Failed to fetch available ${mode === 'department' ? 'doctors' : 'departments'}`, error)
      toast({
        title: "Error",
        description: `Failed to load available ${mode === 'department' ? 'doctors' : 'departments'}.`,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleModeChange = (checked: boolean) => {
    setMode(checked ? 'doctor' : 'department')
    setSelectedItemId(null)
    setAffiliatedItems([])
    setPage(1)
    setAffiliatedPage(1)
  }

  const handleItemClick = (id: number) => {
    setSelectedItemId(id)
    setAffiliatedPage(1)
  }

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
  }

  const handleAffiliatedPageChange = (newPage: number) => {
    setAffiliatedPage(newPage)
  }

  const handleAddAffiliation = async () => {
    if (!selectedItemId || !selectedItemToAdd) return

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    setIsLoading(true)
    try {
      const affiliationData = mode === 'department'
        ? { department_id: selectedItemId, doctor_id: parseInt(selectedItemToAdd) }
        : { doctor_id: selectedItemId, department_id: parseInt(selectedItemToAdd) }

      await api.createAffiliation(affiliationData, token)
      toast({
        title: "Success",
        description: "Affiliation created successfully.",
      })
      fetchAffiliatedItems()
      setIsAddDialogOpen(false)
      setSelectedItemToAdd('')
    } catch (error) {
      console.error('Failed to create affiliation', error)
      toast({
        title: "Error",
        description: "Failed to create affiliation.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteAffiliation = async (affiliatedItemId: number) => {
    if (!selectedItemId) return

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    setIsLoading(true)
    try {
      const doctorId = mode === 'department' ? affiliatedItemId : selectedItemId
      const departmentId = mode === 'department' ? selectedItemId : affiliatedItemId

      await api.deleteAffiliation(doctorId, departmentId, token)
      toast({
        title: "Success",
        description: "Affiliation deleted successfully.",
      })
      fetchAffiliatedItems()
      // Refresh available items after deletion
      fetchAvailableItems()
    } catch (error) {
      console.error('Failed to delete affiliation', error)
      toast({
        title: "Error",
        description: "Failed to delete affiliation.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Affiliation Management</h1>
      <div className="flex items-center space-x-2 mb-4">
        <Switch id="mode-switch" checked={mode === 'doctor'} onCheckedChange={handleModeChange} />
        <Label htmlFor="mode-switch">
          {mode === 'department' ? 'Department-centric' : 'Doctor-centric'} view
        </Label>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>{mode === 'department' ? 'Departments' : 'Doctors'}</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Name</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {(mode === 'department' ? departments : doctors).map((item) => (
                  <TableRow
                    key={item.id}
                    className={`cursor-pointer ${selectedItemId === item.id ? 'bg-muted' : ''}`}
                    onClick={() => handleItemClick(item.id)}
                  >
                    <TableCell>{item.id}</TableCell>
                    <TableCell>{item.name}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <div className="mt-4 flex justify-between">
              <Button onClick={() => handlePageChange(page - 1)} disabled={page === 1 || isLoading}>Previous</Button>
              <span>Page {page} of {totalPages}</span>
              <Button onClick={() => handlePageChange(page + 1)} disabled={page === totalPages || isLoading}>Next</Button>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="flex justify-between items-center">
              <span>{mode === 'department' ? 'Affiliated Doctors' : 'Affiliated Departments'}</span>
              {selectedItemId && (
                <Dialog open={isAddDialogOpen} onOpenChange={(open) => {
                  setIsAddDialogOpen(open)
                  if (open) {
                    fetchAvailableItems()
                  }
                }}>
                  <DialogTrigger asChild>
                    <Button>Add Affiliation</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Add Affiliation</DialogTitle>
                    </DialogHeader>
                    <Select onValueChange={setSelectedItemToAdd} value={selectedItemToAdd}>
                      <SelectTrigger>
                        <SelectValue placeholder={`Select ${mode === 'department' ? 'Doctor' : 'Department'}`} />
                      </SelectTrigger>
                      <SelectContent>
                        {availableItemsToAdd.map((item) => (
                          <SelectItem key={item.id} value={item.id.toString()}>{item.name}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Button 
                      onClick={handleAddAffiliation} 
                      disabled={isLoading || !selectedItemToAdd}
                    >
                      Add
                    </Button>
                  </DialogContent>
                </Dialog>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {selectedItemId ? (
              <>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Name</TableHead>
                      <TableHead>Action</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {affiliatedItems.map((item) => (
                      <TableRow key={item.id}>
                        <TableCell>{item.id}</TableCell>
                        <TableCell>{item.name}</TableCell>
                        <TableCell>
                          <Button variant="destructive" onClick={() => handleDeleteAffiliation(item.id)} disabled={isLoading}>Remove</Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                <div className="mt-4 flex justify-between">
                  <Button onClick={() => handleAffiliatedPageChange(affiliatedPage - 1)} disabled={affiliatedPage === 1 || isLoading}>Previous</Button>
                  <span>Page {affiliatedPage} of {affiliatedTotalPages}</span>
                  <Button onClick={() => handleAffiliatedPageChange(affiliatedPage + 1)} disabled={affiliatedPage === affiliatedTotalPages || isLoading}>Next</Button>
                </div>
              </>
            ) : (
              <p>Select a {mode === 'department' ? 'department' : 'doctor'} to view affiliations</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}