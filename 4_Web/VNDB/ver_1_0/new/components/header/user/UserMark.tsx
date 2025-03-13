"use client"

import { useState, useEffect } from "react"
import { usePathname } from "next/navigation"
import { useUserContext } from "@/context/UserContext"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Star, StarIcon, Loader2, Trash } from "lucide-react"
import { Category } from "@/lib/types"
import { api } from "@/lib/api"

interface UserMarkButtonProps {
  setOpen: (open: boolean) => void
}

interface UserMarkDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
}

function analyzePathname(pathname: string) {
  const match = pathname.match(/^\/(v|c|p|s)\/(\d+)/)
  if (match) {
    return { type: match[1], id: Number.parseInt(match[2], 10) }
  }
  return { type: "", id: 0 }
}

export function UserMarkButton({ setOpen }: UserMarkButtonProps) {
  const { user } = useUserContext()
  const pathname = usePathname()
  const [isMarked, setIsMarked] = useState(false)

  const checkIfMarked = async () => {
    if (user && pathname) {
      const { type, id } = analyzePathname(pathname)
      if (type && id) {
        const { isMarked } = await api.mark.isMarked(type, id)
        setIsMarked(isMarked)
      }
    } else {
      setIsMarked(false)
    }
  }

  useEffect(() => {
    checkIfMarked()
  }, [user, pathname])

  return (
    <Button
      onClick={() => setOpen(true)}
      variant="ghost"
      size="icon"
      className="text-yellow-400 hover:text-yellow-100 hover:bg-white/10 transition-colors"
    >
      {isMarked ? <StarIcon className="w-4 h-4 fill-current" /> : <Star className="w-4 h-4" />}
    </Button>
  )
}

export function UserMarkDialog({ open, setOpen }: UserMarkDialogProps) {
  const { user } = useUserContext()
  const pathname = usePathname()

  const [isLoading, setisLoading] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [toggledCategoryIds, setToggledCategoryIds] = useState<number[]>([])
  const [newCategoryName, setNewCategoryName] = useState("")

  const fetchData = async () => {
    if (user && pathname) {
      const { type, id } = analyzePathname(pathname)
      if (type && id) {
        const fetchedCategories = await api.category.get(type)
        const fetchedToggledCategoryIds = await api.mark.getCategories(type, id)
        // sort categories by updated_at and move toggled categories to the top
        const sortedCategories = fetchedCategories.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
        const toggledCategories = sortedCategories.filter((category) => fetchedToggledCategoryIds.categoryIds.includes(category.id))
        const otherCategories = sortedCategories.filter((category) => !fetchedToggledCategoryIds.categoryIds.includes(category.id))
        setCategories([...toggledCategories, ...otherCategories])
        setToggledCategoryIds(fetchedToggledCategoryIds.categoryIds)
      }
    }
  }

  const handleCategoryToggle = async (categoryId: number) => {
    if (user && pathname) {
      const { type, id } = analyzePathname(pathname)
      if (type && id) {
        try {
          setisLoading(true)
          if (toggledCategoryIds.includes(categoryId)) {
            await api.category.removeMark(type, categoryId, id)
          } else {
            await api.category.addMark(type, categoryId, id)
          }
          setisLoading(false)
        } catch (error) {
          console.error("Failed to toggle category:", error)
        } finally {
          fetchData()
          setisLoading(false)
        }
      }
    }
  }

  const handleCreateCategory = async () => {
    if (user && pathname) {
      if (!newCategoryName.trim()) return
      const { type, id } = analyzePathname(pathname)
      if (type && id) {
        try {
          setisLoading(true)
          await api.category.create(type, newCategoryName)
          setNewCategoryName("")
        } catch (error) {
          console.error("Failed to create category:", error)
        } finally {
          fetchData()
          setisLoading(false)
        }
      }
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    if (user && pathname) {
      const { type, id } = analyzePathname(pathname)
      if (type && id) {
        await api.category.delete(type, categoryId)
        fetchData()
      }
    }
  }

  useEffect(() => {
    fetchData()
  }, [user, pathname])

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="bg-[#0F2942]/80 border-white/10">
        <DialogHeader>
          <DialogTitle className="text-xl text-white">Mark Resource</DialogTitle>
        </DialogHeader>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-1">
          {categories.map((category) => (
            <div key={`category-${category.id}`} className="flex flex-row items-center justify-between border-b sm:border-r border-white/10">
              <div className="h-full flex-grow min-w-0 flex flex-row items-center group truncate">
                <Checkbox
                  id={`category-${category.id}`}
                  checked={toggledCategoryIds.includes(category.id)}
                  onCheckedChange={() => handleCategoryToggle(category.id)}
                  disabled={isLoading}
                  className="flex-shrink-0 border-white/60 group-hover:border-white data-[state=checked]:bg-white data-[state=checked]:text-[#0F2942]"
                />
                <Label htmlFor={`category-${category.id}`} className="w-full h-full text-white group-hover:font-bold cursor-pointer ml-1">
                  {category.category_name}
                </Label>
              </div>
              <Button
                // onClick={() => handleDeleteCategory(category.id)}
                onClick={() => {
                  if (confirm("Are you sure you want to delete this category?")) {
                    handleDeleteCategory(category.id)
                  }
                }}
                variant="ghost"
                size="icon"
                className="text-red-400 hover:text-red-100 hover:bg-white/10 transition-colors"
              >
                <Trash className="w-4 h-4" />
              </Button>
            </div>
          ))}
        </div>
        <div className="flex items-center gap-1">
          <Input
            value={newCategoryName}
            onChange={(e) => setNewCategoryName(e.target.value)}
            placeholder="New category name"
            disabled={isLoading}
            className="bg-[#0A1929] border-white/10 text-white placeholder:text-white/50"
          />
          <Button
            onClick={handleCreateCategory}
            disabled={isLoading}
            className="bg-white hover:bg-white/90 text-[#0A1929] transition-all duration-300"
          >
            {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Create"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}

export function UserMark() {
  const [open, setOpen] = useState(false)
  const [hidden, setHidden] = useState(false)

  const { user } = useUserContext()
  const pathname = usePathname()
  const { type, id } = analyzePathname(pathname)

  useEffect(() => {
    if (user && type && id) {
      setHidden(false)
    } else {
      setHidden(true)
    }
  }, [user, type, id])

  return (
    <>
      {hidden ? (
        <></>
      ) : (
        <>
          <UserMarkButton setOpen={setOpen} />
          <UserMarkDialog open={open} setOpen={setOpen} />
        </>
      )}
    </>
  )
}
