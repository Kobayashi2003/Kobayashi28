"use client"

import { useState, useEffect } from "react"
import { useUser } from "@/components/user/user-context"
import { api } from "@/lib/api"
import Image from "next/image"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Loader2, Plus, Trash2 } from "lucide-react"

type Category = {
  id: number
  user_id: number
  category_name: string
  marks: Mark[]
  type: "v" | "c" | "p" | "s"
  created_at: string
  updated_at: string
}

type Mark = {
  id: string
  title: string
  image?: {
    url: string
  }
}

const TYPES = [
  { code: "v", label: "Visual Novel" },
  { code: "c", label: "Character" },
  { code: "p", label: "Producer" },
  { code: "s", label: "Staff" },
]

export default function UserPage() {
  const { user } = useUser()
  const [activeType, setActiveType] = useState(TYPES[0].code)
  const [categories, setCategories] = useState<Category[] | null>(null)
  const [marks, setMarks] = useState<Mark[]>([])
  const [activeCategory, setActiveCategory] = useState<number | null>(null)
  const [newCategoryName, setNewCategoryName] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (user) {
      setActiveCategory(null) // Reset active category when type changes
      setMarks([]) // Clear marks when type changes
      fetchCategories()
    }
  }, [user]) // Removed activeType from dependencies

  useEffect(() => {
    if (activeCategory !== null) {
      fetchMarks()
    }
  }, [activeCategory, activeType])

  const fetchCategories = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const fetchedCategories = await api.getCategories(activeType)
      setCategories(fetchedCategories)
      if (fetchedCategories.length > 0 && activeCategory === null) {
        setActiveCategory(fetchedCategories[0].id)
      }
    } catch (error) {
      console.error("Failed to fetch categories:", error)
      setError("Failed to fetch categories. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const fetchMarks = async () => {
    if (activeCategory === null) return
    setIsLoading(true)
    setError(null)
    try {
      const fetchedMarks = await api.getMarks(activeType, activeCategory)
      setMarks(fetchedMarks)
    } catch (error) {
      console.error("Failed to fetch marks:", error)
      setError("Failed to fetch marks. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateCategory = async () => {
    if (!newCategoryName.trim()) return
    setIsLoading(true)
    setError(null)
    try {
      await api.createCategory(activeType, newCategoryName)
      setNewCategoryName("")
      fetchCategories()
    } catch (error) {
      console.error("Failed to create category:", error)
      setError("Failed to create category. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    setIsLoading(true)
    setError(null)
    try {
      await api.deleteCategory(activeType, categoryId)
      fetchCategories()
      if (activeCategory === categoryId) {
        setActiveCategory(null)
      }
    } catch (error) {
      console.error("Failed to delete category:", error)
      setError("Failed to delete category. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  if (!user) {
    return <div className="text-center text-white mt-8">Please log in to view your profile.</div>
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-white mb-6">User Profile</h1>

      <div className="flex space-x-4 mb-6">
        {TYPES.map((type) => (
          <Button
            key={type.code}
            onClick={() => setActiveType(type.code)}
            variant={activeType === type.code ? "default" : "outline"}
            className="capitalize"
          >
            {type.label}
          </Button>
        ))}
      </div>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-white" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="md:col-span-1 space-y-4">
            <h2 className="text-xl font-semibold text-white mb-2">Categories</h2>
            {categories && categories.length > 0 ? (
              categories.map((category) => (
                <div key={category.id} className="flex items-center justify-between">
                  <Button
                    variant={activeCategory === category.id ? "default" : "outline"}
                    onClick={() => setActiveCategory(category.id)}
                    className="w-full justify-start text-white"
                  >
                    {category.category_name}
                  </Button>
                  {category.category_name !== "Default" && (
                    <Button variant="ghost" size="icon" onClick={() => handleDeleteCategory(category.id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              ))
            ) : (
              <p className="text-white">No categories found.</p>
            )}
            <div className="flex items-center space-x-2">
              <Input
                value={newCategoryName}
                onChange={(e) => setNewCategoryName(e.target.value)}
                placeholder="New category name"
                className="bg-[#0F2942] border-white/10 text-white placeholder:text-white/60"
              />
              <Button onClick={handleCreateCategory} variant="ghost" size="icon">
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          </div>

          <div className="md:col-span-3">
            <h2 className="text-xl font-semibold text-white mb-4">Marked Items</h2>
            {marks.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {marks.map((mark) => (
                  <Link
                    key={mark.id}
                    href={`/${TYPES.find((t) => t.code === activeType)?.label.toLowerCase()}/${mark.id}`}
                    className="block group"
                  >
                    <div className="bg-[#0F2942] rounded-lg overflow-hidden shadow-lg transition-all duration-300 ease-in-out group-hover:shadow-xl group-hover:scale-105">
                      <div className="relative w-full" style={{ paddingBottom: "133.33%" }}>
                        {mark.image?.url ? (
                          <Image
                            src={mark.image.url || "/placeholder.svg"}
                            alt={mark.title}
                            layout="fill"
                            objectFit="cover"
                            className="transition-transform duration-300 ease-in-out group-hover:scale-110"
                          />
                        ) : (
                          <div className="absolute inset-0 flex items-center justify-center bg-gray-200 text-gray-500">
                            No image
                          </div>
                        )}
                      </div>
                      <div className="p-4 transition-colors duration-300 ease-in-out group-hover:bg-[#1A3A5A]">
                        <h3 className="text-lg font-semibold text-white truncate">{mark.title}</h3>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-white">No items marked in this category.</p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

