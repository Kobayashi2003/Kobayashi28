'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Search } from 'lucide-react'
import { api } from '@/lib/api'
import { Department, PaginatedResponse } from '@/lib/types'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function DepartmentsPage() {
  // State for departments data, pagination, search, and loading
  const [departments, setDepartments] = useState<Department[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()
  const { toast } = useToast()

  // Fetch departments data
  const fetchDepartments = async (currentPage: number, query: string = '') => {
    setIsLoading(true)
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      let response: PaginatedResponse<Department>
      if (query) {
        response = await api.searchDepartments(query, currentPage, 10, 'name', false, token)
      } else {
        response = await api.getDepartments(currentPage, 10, 'name', false, token)
      }
      setDepartments(response.results)
      setTotalPages(Math.ceil(response.count / 10))
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load departments.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  // Fetch departments on component mount and when page or search query changes
  useEffect(() => {
    fetchDepartments(page, searchQuery)
  }, [page, searchQuery])

  // Handle search form submission
  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setPage(1)
    fetchDepartments(1, searchQuery)
  }

  // Handle page change
  const handlePageChange = (newPage: number) => {
    setPage(newPage)
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Our Departments</h1>
      <form onSubmit={handleSearch} className="mb-6">
        <div className="relative max-w-md">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search departments..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-8"
          />
        </div>
      </form>
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
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {departments.map((department) => (
            <Card key={department.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>{department.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>{department.description || 'No description available'}</CardDescription>
                <Button 
                  className="mt-4" 
                  onClick={() => router.push(`/departments/${department.id}`)}
                >
                  View Details
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
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