'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { api } from '@/lib/api'
import { Registration, PaginatedResponse } from '@/lib/types'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import { Search } from 'lucide-react'

export default function AppointmentsPage() {
  // State for appointments data, pagination, search, and loading
  const [appointments, setAppointments] = useState<Registration[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  
  const router = useRouter()
  const { toast } = useToast()

  // Fetch appointments data
  const fetchAppointments = async (currentPage: number, query: string = '') => {
    const userId = parseInt(localStorage.getItem('userId') || '0');

    setIsLoading(true)
    try {
      let response: PaginatedResponse<Registration>
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }
      
      // Use search API if query is provided, otherwise use regular get API
      if (query) {
        response = await api.searchUserRegistrations(userId, query, currentPage, 10, 'id', false, token)
      } else {
        response = await api.getUserRegistrations(userId, currentPage, 10, 'id', false, token)
      }
      setAppointments(response.results)
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load appointments.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  // Fetch appointments on component mount and when page or search query changes
  useEffect(() => {
    fetchAppointments(page, searchQuery)
  }, [page, searchQuery])

  // Handle search form submission
  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setPage(1)
    fetchAppointments(1, searchQuery)
  }

  // Handle page change
  const handlePageChange = (newPage: number) => {
    setPage(newPage)
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Your Appointments</h1>
      
      {/* Search form */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <div className="relative flex-grow">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search appointments..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-8"
            />
          </div>
          <Button type="submit">Search</Button>
        </div>
      </form>

      {/* Display appointments or loading state */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader>
                <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </CardHeader>
              <CardContent>
                <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : appointments.length === 0 ? (
        <p>You have no appointments scheduled.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {appointments.map((appointment) => (
            <Card key={appointment.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>Appointment {appointment.id}</CardTitle>
                <CardDescription>Status: {appointment.status}</CardDescription>
              </CardHeader>
              <CardContent>
                <p><strong>Notes:</strong> {appointment.notes || 'No notes'}</p>
                <Link href={`/appointments/${appointment.id}`}>
                  <Button className="mt-4">View Details</Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Pagination controls */}
      <div className="mt-6 flex justify-between">
        <Button onClick={() => handlePageChange(page - 1)} disabled={page === 1} variant="outline">
          Previous
        </Button>
        <span>Page {page} of {totalPages}</span>
        <Button onClick={() => handlePageChange(page + 1)} disabled={page === totalPages} variant="outline">
          Next
        </Button>
      </div>
    </div>
  )
}