'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription,
         AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog"
import { useToast } from '@/hooks/use-toast'

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null)
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const fetchUserData = async () => {
      try {
        const userData = await api.getCurrentUser(token)
        setUser(userData)
      } catch (error) {
        console.error('Failed to fetch user data', error)
        toast({
          title: "Error",
          description: "Failed to load user profile. Please try logging in again.",
          variant: "destructive",
        })
        router.push('/login')
      }
    }

    fetchUserData()
  }, [router, toast])

  const handleUpdateProfile = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const token = localStorage.getItem('token')
    if (!token || !user) return

    const formData = new FormData(e.currentTarget)
    const updatedData = {
      username: formData.get('username') as string,
      phone_number: formData.get('phone_number') as string,
      bio: formData.get('bio') as string,
    }

    try {
      const updatedUser = await api.updateCurrentUser(updatedData, token)
      setUser(updatedUser)
      toast({
        title: "Profile Updated",
        description: "Your profile has been successfully updated.",
      })
    } catch (error) {
      console.error('Failed to update profile', error)
      toast({
        title: "Error",
        description: "Failed to update profile. Please try again.",
        variant: "destructive",
      })
    }
  }

  const handleChangePassword = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const token = localStorage.getItem('token')
    if (!token) return

    const formData = new FormData(e.currentTarget)
    const oldPassword = formData.get('oldPassword') as string
    const newPassword = formData.get('newPassword') as string

    try {
      await api.changeCurrentUserPassword(oldPassword, newPassword, token)
      toast({
        title: "Password Changed",
        description: "Your password has been successfully changed.",
      })
    } catch (error) {
      console.error('Failed to change password', error)
      toast({
        title: "Error",
        description: "Failed to change password. Please check your old password and try again.",
        variant: "destructive",
      })
    }
  }

  const handleDeleteAccount = async () => {
    const token = localStorage.getItem('token')
    if (!token) return

    try {
      await api.deleteCurrentUser(token)
      localStorage.removeItem('token')
      toast({
        title: "Account Deleted",
        description: "Your account has been successfully deleted.",
      })
      router.push('/')
    } catch (error) {
      console.error('Failed to delete account', error)
      toast({
        title: "Error",
        description: "Failed to delete account. Please try again.",
        variant: "destructive",
      })
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/login')
    toast({
      title: "Logged Out",
      description: "You have been successfully logged out.",
    })
  }

  if (!user) {
    return <div>Loading...</div>
  }

  return (
    <div className="container mx-auto py-10">
      <div className="max-w-4xl mx-auto">
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Profile</h1>
            <p className="text-muted-foreground">
              Manage your account settings and preferences.
            </p>
          </div>
          
          <Separator />

          <section className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <h2 className="text-lg font-semibold">Personal Information</h2>
                <div className="mt-4 space-y-3">
                  <div>
                    <span className="text-sm text-muted-foreground">Username</span>
                    <p className="text-base font-medium">{user.username}</p>
                  </div>
                  <div>
                    <span className="text-sm text-muted-foreground">Phone Number</span>
                    <p className="text-base font-medium">{user.phone_number}</p>
                  </div>
                  <div>
                    <span className="text-sm text-muted-foreground">Role</span>
                    <p className="text-base font-medium">{user.is_admin ? 'Administrator' : 'User'}</p>
                  </div>
                  <div>
                    <span className="text-sm text-muted-foreground">Bio</span>
                    <p className="text-base font-medium">{user.bio || 'No bio provided'}</p>
                  </div>
                </div>
              </div>
              
              <div>
                <h2 className="text-lg font-semibold">Account Details</h2>
                <div className="mt-4 space-y-3">
                  <div>
                    <span className="text-sm text-muted-foreground">Account Created</span>
                    <p className="text-base font-medium">{new Date(user.created_at).toLocaleString()}</p>
                  </div>
                  <div>
                    <span className="text-sm text-muted-foreground">Last Updated</span>
                    <p className="text-base font-medium">{new Date(user.updated_at).toLocaleString()}</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <Separator />

          <section className="space-y-4">
            <h2 className="text-lg font-semibold">Actions</h2>
            <div className="flex flex-wrap gap-4">
              <Dialog>
                <DialogTrigger asChild>
                  <Button>Edit Profile</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Edit Profile</DialogTitle>
                  </DialogHeader>
                  <form onSubmit={handleUpdateProfile}>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="username" className="text-right">
                          Username
                        </Label>
                        <Input id="username" name="username" defaultValue={user.username} className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="phone_number" className="text-right">
                          Phone Number
                        </Label>
                        <Input id="phone_number" name="phone_number" defaultValue={user.phone_number} className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="bio" className="text-right">
                          Bio
                        </Label>
                        <Input id="bio" name="bio" defaultValue={user.bio} className="col-span-3" />
                      </div>
                    </div>
                    <div className="flex justify-end">
                      <Button type="submit">Update Profile</Button>
                    </div>
                  </form>
                </DialogContent>
              </Dialog>
              
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant="outline">Change Password</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Change Password</DialogTitle>
                  </DialogHeader>
                  <form onSubmit={handleChangePassword}>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="oldPassword" className="text-right">
                          Old Password
                        </Label>
                        <Input id="oldPassword" name="oldPassword" type="password" className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="newPassword" className="text-right">
                          New Password
                        </Label>
                        <Input id="newPassword" name="newPassword" type="password" className="col-span-3" />
                      </div>
                    </div>
                    <div className="flex justify-end">
                      <Button type="submit">Change Password</Button>
                    </div>
                  </form>
                </DialogContent>
              </Dialog>

              <Button variant="outline" onClick={handleLogout}>
                Logout
              </Button>

              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="destructive">Delete Account</Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                    <AlertDialogDescription>
                      This action cannot be undone. This will permanently delete your
                      account and remove your data from our servers.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction onClick={handleDeleteAccount}>
                      Yes, delete my account
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

