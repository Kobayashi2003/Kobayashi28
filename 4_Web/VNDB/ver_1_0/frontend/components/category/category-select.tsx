"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Lock, Plus, Trash2 } from "lucide-react"
import { useState } from "react"

interface Category {
  id: number
  category_name: string
}

interface CategorySelectProps {
  categories: Category[]
  activeCategory: number | null
  onCategoryChange: (id: number) => void
  onCategoryCreate: (name: string) => void
  onCategoryDelete: (id: number) => void
}

export function CategorySelect({
  categories,
  activeCategory,
  onCategoryChange,
  onCategoryCreate,
  onCategoryDelete,
}: CategorySelectProps) {
  const [newCategoryName, setNewCategoryName] = useState("")

  const handleCreateCategory = () => {
    if (!newCategoryName.trim()) return
    onCategoryCreate(newCategoryName)
    setNewCategoryName("")
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-white mb-2">Categories</h2>
      {categories.length > 0 ? (
        [...categories]
          .sort((a, b) => a.id - b.id)
          .map((category) => (
            <div key={category.id} className="flex items-center">
              <Button
                variant={activeCategory === category.id ? "outline" : "default"}
                onClick={() => onCategoryChange(category.id)}
                className={`w-full justify-between font-bold text-lg ${activeCategory === category.id
                    ? "bg-[#1A3A5A] text-white"
                    : "bg-[#0F2942] text-white/90 hover:bg-[#1A3A5A] hover:text-white"
                  }`}
              >
                <span>{category.category_name}</span>
                {category.category_name === "Default" && (
                  <Lock className="h-4 w-4 text-white/60 group-hover:text-white/80" />
                )}
              </Button>
              {category.category_name !== "Default" && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onCategoryDelete(category.id)}
                  className="ml-2 hover:bg-white/30"
                >
                  <Trash2 className="h-4 w-4 text-white/60 hover:text-white/80" />
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
        <Button onClick={handleCreateCategory} variant="ghost" size="icon" className="hover:bg-[#1A3A5A] text-white">
          <Plus className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}