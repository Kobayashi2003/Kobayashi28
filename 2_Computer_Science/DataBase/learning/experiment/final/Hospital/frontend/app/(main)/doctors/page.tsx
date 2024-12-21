'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Search } from 'lucide-react'
import { api } from '@/lib/api'
import { Doctor, PaginatedResponse } from '@/lib/types'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function DoctorsPage() {
  // State for doctors data, pagination, search, and loading
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  const router = useRouter()
  const { toast } = useToast()

  // Fetch doctors data
  const fetchDoctors = async (currentPage: number, query: string = '') => {
    setIsLoading(true)
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      let response: PaginatedResponse<Doctor>
      if (query) {
        response = await api.searchDoctors(query, currentPage, 10, 'name', false, token)
      } else {
        response = await api.getDoctors(currentPage, 10, 'name', false, token)
      }
      setDoctors(response.results)
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load doctors.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  // Fetch doctors on component mount and when page or search query changes
  useEffect(() => {
    fetchDoctors(page, searchQuery)
  }, [page, searchQuery])

  // Handle search form submission
  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setPage(1)
    fetchDoctors(1, searchQuery)
  }

  // Handle page change
  const handlePageChange = (newPage: number) => {
    setPage(newPage)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Our Doctors</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all doctors available for appointments
          </p>
        </div>
      </div>

      <div className="mt-6">
        <form onSubmit={handleSearch} className="max-w-md">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search doctors..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-8"
            />
          </div>
        </form>
      </div>

      {isLoading ? (
        <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader className="space-y-2">
                <div className="h-4 bg-gray-200 rounded w-1/3"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="h-4 bg-gray-200 rounded"></div>
                <div className="h-4 bg-gray-200 rounded"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {doctors.map((doctor) => (
            <Card key={doctor.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>{doctor.name}</CardTitle>
                <CardDescription>
                  {doctor.description || 'Specialist'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <dl className="space-y-2 text-sm">
                  <div>
                    <dt className="text-gray-500">Gender</dt>
                    <dd className="font-medium">{doctor.gender}</dd>
                  </div>
                  <div>
                    <dt className="text-gray-500">Email</dt>
                    <dd className="font-medium">{doctor.email}</dd>
                  </div>
                  <div>
                    <dt className="text-gray-500">Phone</dt>
                    <dd className="font-medium">{doctor.phone_number}</dd>
                  </div>
                  <div className="pt-4">
                    <Button 
                      className="w-full"
                      onClick={() => router.push(`/doctors/${doctor.id}`)}
                    >
                      View Details
                    </Button>
                  </div>
                </dl>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <div className="mt-6 flex items-center justify-between border-t border-gray-200 pt-6">
        <Button
          onClick={() => handlePageChange(page - 1)}
          disabled={page === 1}
          variant="outline"
        >
          Previous
        </Button>
        <p className="text-sm text-gray-700">
          Page {page} of {totalPages}
        </p>
        <Button
          onClick={() => handlePageChange(page + 1)}
          disabled={page === totalPages}
          variant="outline"
        >
          Next
        </Button>
      </div>
    </div>
  )
}