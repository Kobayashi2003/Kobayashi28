"use client"

import { useState, useEffect } from "react"
import { usePathname } from "next/navigation"
import { Star, StarIcon, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { api } from "@/lib/api"
import type { Category } from "@/lib/types"
import { useUser } from "./user-context"


export function UserMark() {
  const { user } = useUser()
  const pathname = usePathname()
  const [showMark, setShowMark] = useState(false)
  const [isOpen, setIsOpen] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [markedCategories, setMarkedCategories] = useState<number[]>([])
  const [newCategoryName, setNewCategoryName] = useState("")
  const [loading, setLoading] = useState(false)
  const [type, setType] = useState<"v" | "c" | "p" | "s">("v")
  const [id, setId] = useState<number | null>(null)

  useEffect(() => {
    if (user && pathname) {
      const match = pathname.match(/^\/(v|c|p|s)(\d+)/)
      if (match) {
        setType(match[1] as "v" | "c" | "p" | "s")
        setId(Number.parseInt(match[2], 10))
        setShowMark(true)
      } else {
        setShowMark(false)
      }
    } else {
      setShowMark(false)
    }
  }, [user, pathname])

  useEffect(() => {
    if (showMark && id) {
      fetchCategories()
      checkIfMarked()
    }
  }, [showMark, id])

  const fetchCategories = async () => {
    try {
      const fetchedCategories = await api.getCategories(type)
      const sortedCategories = fetchedCategories.sort((a, b) => a.id - b.id)
      setCategories(sortedCategories)
    } catch (error) {
      console.error("Failed to fetch categories:", error)
    }
  }

  const checkIfMarked = async () => {
    if (id) {
      try {
        const response = await api.isMarked(type, id)
        setMarkedCategories(response.categoryIds || [])
      } catch (error) {
        console.error("Failed to check if marked:", error)
      }
    }
  }

  const handleMarkToggle = async (categoryId: number) => {
    setLoading(true)
    try {
      if (markedCategories.includes(categoryId)) {
        await api.removeMark(type, categoryId, id!)
        setMarkedCategories((prev) => prev.filter((id) => id !== categoryId))
      } else {
        await api.addMark(type, categoryId, id!)
        setMarkedCategories((prev) => [...prev, categoryId])
      }
    } catch (error) {
      console.error("Failed to toggle mark:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateCategory = async () => {
    if (!newCategoryName.trim()) return
    setLoading(true)
    try {
      const newCategory = await api.createCategory(type, newCategoryName)
      setCategories((prev) => [...prev, newCategory])
      setNewCategoryName("")
    } catch (error) {
      console.error("Failed to create category:", error)
    } finally {
      setLoading(false)
    }
  }

  if (!showMark) return null

  const isMarked = markedCategories.length > 0

  return (
    <>
      <Button
        onClick={() => setIsOpen(true)}
        variant="ghost"
        size="icon"
        className="text-white hover:text-yellow-400 transition-colors"
      >
        {isMarked ? <StarIcon className="h-5 w-5 fill-current" /> : <Star className="h-5 w-5" />}
      </Button>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="bg-[#0A1929] border-white/10">
          <DialogHeader>
            <DialogTitle className="text-white text-xl">Mark Resource</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            {categories.map((category) => (
              <div key={category.id} className="flex items-center space-x-2">
                <Checkbox
                  id={`category-${category.id}`}
                  checked={markedCategories.includes(category.id)}
                  onCheckedChange={() => handleMarkToggle(category.id)}
                  disabled={loading}
                  className="border-white/60 data-[state=checked]:bg-white data-[state=checked]:text-[#0A1929]"
                />
                <Label htmlFor={`category-${category.id}`} className="text-white cursor-pointer">
                  {category.category_name}
                </Label>
              </div>
            ))}
            <div className="flex items-center space-x-2">
              <Input
                value={newCategoryName}
                onChange={(e) => setNewCategoryName(e.target.value)}
                placeholder="New category name"
                disabled={loading}
                className="bg-[#0F2942] border-white/10 text-white placeholder:text-white/60"
              />
              <Button
                onClick={handleCreateCategory}
                disabled={loading}
                className="bg-white text-[#0A1929] hover:bg-white/90"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Create"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}