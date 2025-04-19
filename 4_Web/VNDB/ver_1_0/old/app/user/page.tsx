"use client"

import { useState, useEffect, useCallback } from "react"
import { Loader2 } from "lucide-react"
import { Marks } from "@/components/category/marks"
import { TypeSelect } from "@/components/category/type-select"
import { CategorySelect } from "@/components/category/category-select"
import { useUser } from "@/components/user/user-context"
import type { Category } from "@/lib/types"
import { api } from "@/lib/api"


export default function UserPage() {
  const { user } = useUser()
  const [activeType, setActiveType] = useState<"v" | "c" | "p" | "s">("v")
  const [categories, setCategories] = useState<Category[]>([])
  const [activeCategory, setActiveCategory] = useState<number | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchCategories = useCallback(async () => {
    try {
      const fetchedCategories = await api.getCategories(activeType)
      setCategories(fetchedCategories)

      if (!activeCategory && fetchedCategories.length > 0) {
        setActiveCategory(fetchedCategories[0].id)
      }
    } catch (error) {
      setError("Failed to fetch categories. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }, [activeType])

  useEffect(() => {
    if (user) {
      fetchCategories()
    }
  }, [user, fetchCategories])

  const handleTypeChange = (type: "v" | "c" | "p" | "s") => {
    setActiveType(type)
    setActiveCategory(null)
  }

  const handleCreateCategory = async (name: string) => {
    try {
      await api.createCategory(activeType, name)
      fetchCategories()
    } catch (error) {
      setError("Failed to create category. Please try again.")
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    try {
      await api.deleteCategory(activeType, categoryId)
      if (activeCategory === categoryId) {
        setActiveCategory(null)
      }
      fetchCategories()
    } catch (error) {
      setError("Failed to delete category. Please try again.")
    }
  }

  if (!user) {
    return <div className="text-center text-white mt-8">Please log in to view your profile.</div>
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-white mb-6">User Profile</h1>
      <TypeSelect activeType={activeType} onTypeChange={handleTypeChange} />

      {error && <div className="text-red-500 mb-4">{error}</div>}

      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-white" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="md:col-span-1 space-y-4 bg-[#0A1929] p-4 rounded-lg border border-white/10">
            <CategorySelect
              categories={categories}
              activeCategory={activeCategory}
              onCategoryChange={setActiveCategory}
              onCategoryCreate={handleCreateCategory}
              onCategoryDelete={handleDeleteCategory}
            />
          </div>
          <div className="md:col-span-3">
            {activeCategory && <Marks type={activeType} categoryId={activeCategory} />}
          </div>
        </div>
      )}
    </div>
  )
}