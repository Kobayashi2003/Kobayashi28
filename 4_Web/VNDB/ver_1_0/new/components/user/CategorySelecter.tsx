"use client"

import { useEffect } from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Trash2 } from "lucide-react"

interface CategoryOption {
  key: string
  value: number
  label: string
  labelSmall?: string
}

interface CategorySelecterProps {
  loading: boolean
  categoryOptions: CategoryOption[]
  selectedValue?: number
  deleteMode: boolean
  setToDeleteId: (id: number) => void
  handleDeleteCategory: () => void
  onChange: (value: number) => void
  className?: string
}

export function CategorySelecter({ loading, categoryOptions, selectedValue, deleteMode, setToDeleteId, handleDeleteCategory, onChange, className }: CategorySelecterProps) {

  useEffect(() => {
    if (!selectedValue && categoryOptions.length > 0) {
      onChange(categoryOptions[0].value)
    }
  }, [categoryOptions])

  return (
    <div className={cn(
      "bg-[#0F2942]/80 hover:bg-[#0F2942] flex flex-col gap-2 p-4",
      "border border-white/10 hover:border-white/20 rounded-lg",
      "transition-all duration-300",
      className
    )}>
      {categoryOptions.map(categoryOption => (
        <div key={categoryOption.key} className="flex flex-row gap-2">
          <Button
            variant="outline"
            onClick={() => onChange(categoryOption.value)}
            className={cn(
              "flex-1",
              "border-white/10 hover:border-white/20 hover:bg-white/20",
              "text-white hover:text-white/80 text-base md:text-lg font-bold",
              "transition-all duration-300",
              selectedValue === categoryOption.value && "bg-white/10"
            )}
          >
            {categoryOption.label}
          </Button>
          {deleteMode && (
            <Button
              size="icon"
              variant="outline"
              disabled={loading}
              onClick={() => {
                setToDeleteId(categoryOption.value)
                handleDeleteCategory()
              }}
              className={cn(
                "border-white/10 hover:border-white/20 hover:bg-white/20",
                "text-base md:text-lg font-bold",
                "transition-all duration-300",
                "text-red-400 hover:text-red-500 border-red-400/40 hover:border-red-400/60",
                loading && "animate-pulse"
              )}
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          )}
        </div>
      ))}
    </div>
  )
}