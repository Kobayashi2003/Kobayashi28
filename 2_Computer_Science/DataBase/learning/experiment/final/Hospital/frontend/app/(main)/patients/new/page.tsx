'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Patient } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function NewPatientPage() {
  const [newPatient, setNewPatient] = useState<Omit<Patient, 'id' | 'user_id' | 'created_at' | 'updated_at'>>({
    name: '',
    gender: '',
    birthday: '',
    phone_number: '',
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewPatient({ ...newPatient, [e.target.name]: e.target.value })
  }

  const handleSelectChange = (value: string) => {
    setNewPatient({ ...newPatient, gender: value })
  }

  const handleCreatePatient = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const createdPatient = await api.createPatient(newPatient, token)
      toast({
        title: "Success",
        description: "Patient created successfully.",
      })
      router.push(`/patients/${createdPatient.id}`)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create patient. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Create New Patient</CardTitle>
          <CardDescription>Enter the patient's details below</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleCreatePatient} className="space-y-4">
            <div>
              <Label htmlFor="name">Name</Label>
              <Input id="name" name="name" value={newPatient.name} onChange={handleInputChange} required />
            </div>
            <div>
              <Label htmlFor="gender">Gender</Label>
              <Select onValueChange={handleSelectChange} required>
                <SelectTrigger>
                  <SelectValue placeholder="Select gender" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="male">Male</SelectItem>
                  <SelectItem value="female">Female</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="birthday">Birthday</Label>
              <Input id="birthday" name="birthday" type="date" value={newPatient.birthday} onChange={handleInputChange} required />
            </div>
            <div>
              <Label htmlFor="phone_number">Phone Number</Label>
              <Input id="phone_number" name="phone_number" value={newPatient.phone_number} onChange={handleInputChange} required />
            </div>
          </form>
        </CardContent>
        <CardFooter>
          <Button type="submit" onClick={handleCreatePatient} disabled={isSubmitting}>
            {isSubmitting ? 'Creating...' : 'Create Patient'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}