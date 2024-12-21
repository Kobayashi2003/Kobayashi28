'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { User } from '@/lib/types'
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"

export default function ProfilePage() {
  // State for user data, loading status, and edit mode
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [editedUser, setEditedUser] = useState<Partial<User>>({})

  const router = useRouter()
  const { toast } = useToast()

  // Fetch user data on component mount
  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
        return
      }

      try {
        const userData = await api.getCurrentUser(token)
        setUser(userData)
        setEditedUser(userData)
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to load user profile. Please try logging in again.",
          variant: "destructive",
        })
        router.push('/login')
      } finally {
        setIsLoading(false)
      }
    }

    fetchUserData()
  }, [router, toast])

  // Handle form input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEditedUser({ ...editedUser, [e.target.name]: e.target.value })
  }

  // Handle profile update
  const handleUpdateProfile = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!user) return

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const updatedUser = await api.updateCurrentUser(editedUser, token)
      setUser(updatedUser)
      setIsEditing(false)
      toast({
        title: "Success",
        description: "Your profile has been successfully updated.",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update profile. Please try again.",
        variant: "destructive",
      })
    }
  }

  // Handle account deletion
  const handleDeleteAccount = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      try {
        await api.deleteCurrentUser(token)
        localStorage.removeItem('token')
        toast({
          title: "Account Deleted",
          description: "Your account has been successfully deleted.",
        })
        router.push('/')
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to delete account. Please try again.",
          variant: "destructive",
        })
      }
    }
  }

  // Render loading skeleton
  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <Skeleton className="h-8 w-1/3" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-2/3" />
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Render error state if user data failed to load
  if (!user) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
            <CardDescription>Failed to load user profile.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/login')}>Return to Login</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Render user profile
  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Your Profile</CardTitle>
          <CardDescription>View and edit your personal information</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleUpdateProfile}>
            <div className="grid gap-4">
              <div>
                <Label htmlFor="username">Username</Label>
                <Input 
                  id="username" 
                  name="username" 
                  value={editedUser.username || ''} 
                  onChange={handleInputChange} 
                  disabled={!isEditing} 
                />
              </div>
              <div>
                <Label htmlFor="phone_number">Phone Number</Label>
                <Input 
                  id="phone_number" 
                  name="phone_number" 
                  value={editedUser.phone_number || ''} 
                  onChange={handleInputChange} 
                  disabled={!isEditing} 
                />
              </div>
              <div>
                <Label htmlFor="bio">Bio</Label>
                <Input 
                  id="bio" 
                  name="bio" 
                  value={editedUser.bio || ''} 
                  onChange={handleInputChange} 
                  disabled={!isEditing} 
                />
              </div>
              <div>
                <Label>Admin Status</Label>
                <Input 
                  value={user.is_admin ? 'Admin' : 'Regular User'} 
                  disabled 
                />
              </div>
              <div>
                <Label>Account Created</Label>
                <Input 
                  value={new Date(user.created_at).toLocaleString()} 
                  disabled 
                />
              </div>
              {isEditing ? (
                <div className="flex justify-end space-x-2">
                  <Button type="button" variant="outline" onClick={() => setIsEditing(false)}>Cancel</Button>
                  <Button type="submit">Save Changes</Button>
                </div>
              ) : (
                <Button type="button" onClick={() => setIsEditing(true)}>Edit Profile</Button>
              )}
            </div>
          </form>
          <div className="mt-6">
            <Button variant="destructive" onClick={handleDeleteAccount}>Delete Account</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}