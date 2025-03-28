"use client"

import { useState, useEffect } from "react"
import { usePathname } from "next/navigation"

import { cn } from "@/lib/utils"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { CheckBox } from "@/components/check/CheckBox"
import { DeleteButton } from "@/components/button/DeleteButton"
import { CategoryCreator } from "@/components/category/CategoryCreator"

import { Loader2, RefreshCw } from "lucide-react"

import { useUserContext } from "@/context/UserContext"
import { Category } from "@/lib/types"
import { api } from "@/lib/api"

interface MarkDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  className?: string
}

function analyzePathname(pathname: string) {
  const match = pathname.match(/^\/(v|c|p|s)\/(\d+)/)
  if (match) {
    return { type: match[1], id: Number.parseInt(match[2], 10) }
  }
  return { type: "", id: 0 }
}

export function MarkDialog({ open, setOpen, className }: MarkDialogProps) {

  const { user } = useUserContext()
  const pathname = usePathname()
  const { type, id } = analyzePathname(pathname)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [toggledCategoryIds, setToggledCategoryIds] = useState<number[]>([])
  const [newCategoryName, setNewCategoryName] = useState("")

  const fetchCategories = async () => {
    if (user) {
      if (type && id) {
        try {
          setLoading(true)
          setError(null)
          setNotFound(false)
          const fetchedCategories = await api.category.get(type)
          const fetchedToggledCategoryIds = await api.mark.getCategoriesByMark(type, id)
          // sort categories by updated_at and move toggled categories to the top
          const sortedCategories = fetchedCategories.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
          const toggledCategories = sortedCategories.filter((category) => fetchedToggledCategoryIds.categoryIds.includes(category.id))
          const otherCategories = sortedCategories.filter((category) => !fetchedToggledCategoryIds.categoryIds.includes(category.id))
          setCategories([...toggledCategories, ...otherCategories])
          setToggledCategoryIds(fetchedToggledCategoryIds.categoryIds)
        } catch (error) {
          setError(error as string)
        } finally {
          setLoading(false)
          if (categories.length === 0) {
            setNotFound(true)
          }
        }
      }
    }
  }

  const handleToggleCategory = async (categoryId: number) => {
    if (user) {
      if (type && id) {
        try {
          setLoading(true)
          if (toggledCategoryIds.includes(categoryId)) {
            await api.category.removeMark(type, categoryId, id)
          } else {
            await api.category.addMark(type, categoryId, id)
          }
          setLoading(false)
        } catch (error) {
          setError(error as string)
        } finally {
          setLoading(false)
          fetchCategories()
        }
      }
    }
  }

  const handleCreateCategory = async () => {
    if (user) {
      if (!newCategoryName.trim()) return
      if (type && id) {
        try {
          setLoading(true)
          await api.category.create(type, newCategoryName)
          setNewCategoryName("")
        } catch (error) {
          setError(error as string)
        } finally {
          setLoading(false)
          fetchCategories()
        }
      }
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    if (user) {
      if (type && id) {
        try {
          const confirmed = confirm("Are you sure you want to delete this category?")
          if (!confirmed) return
          setLoading(true)
          await api.category.delete(type, categoryId)
          fetchCategories()
        } catch (error) {
          setError(error as string)
        } finally {
          setLoading(false)
          fetchCategories()
        }
      }
    }
  }

  useEffect(() => {
    fetchCategories()
  }, [user, pathname])

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className={cn(
        "bg-[#0F2942]/80 border-white/10",
        "data-[state=open]:animate-in data-[state=closed]:animate-out",
        "data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
        "data-[state=closed]:slide-out-to-bottom-1/2 data-[state=open]:slide-in-from-bottom-1/2",
        className
      )}>
        <DialogHeader>
          <DialogTitle className="text-xl text-white">Mark Resource</DialogTitle>
        </DialogHeader>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-1">
          {loading && <Loader2 className="w-4 h-4 animate-spin" />}
          {error && <p className="text-red-500">{error}</p>}
          {notFound && <p className="text-yellow-500">No categories found</p>}
          {(error || notFound) && <button onClick={fetchCategories}><RefreshCw className="w-4 h-4" /></button>}
          {!loading && !error && !notFound && categories.map((category, index) => (
            <div key={`mark-dialog-category-${index}`} className={cn(
              "flex flex-row justify-between items-center",
              "border-b sm:border-r border-white/10",
            )}>
              <CheckBox 
                id={category.id.toString()}
                label={category.category_name}
                checked={toggledCategoryIds.includes(category.id)}
                onChange={() => handleToggleCategory(category.id)}
                disabled={loading}
                className="truncate h-full w-full"
              />
              <DeleteButton
                handleDelete={() => handleDeleteCategory(category.id)}
                disabled={loading}
              />
            </div>
          ))}
        </div>
        <CategoryCreator
          newCategoryName={newCategoryName}
          setNewCategoryName={setNewCategoryName}
          handleCreateCategory={handleCreateCategory}
          disabled={loading}
          className="bg-transparent hover:bg-transparent border-none w-full p-0"
        />
      </DialogContent>
    </Dialog>
  )
}
