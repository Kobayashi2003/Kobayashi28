import { cn } from "@/lib/utils"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { CheckBox } from "@/components/check/CheckBox"
import { DeleteButton } from "@/components/button/DeleteButton"
import { CategoryCreator } from "@/components/category/CategoryCreator"
import { Loader2, RefreshCw } from "lucide-react"

import { Category } from "@/lib/types"

interface MarkDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  state: "loading" | "error" | "notFound" | null
  categories: Category[]
  toggledCategoryIds: number[]
  handleRefreshCategories: () => void
  handleCreateCategory: (categoryName: string) => void
  handleDeleteCategory: (categoryId: number) => void
  handleToggleCategory: (categoryId: number) => void
  className?: string
}

export function MarkDialog({ open, setOpen, state, categories, toggledCategoryIds, handleRefreshCategories, handleCreateCategory, handleDeleteCategory, handleToggleCategory, className }: MarkDialogProps) {

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
        {state !== null && (
          <div className="flex flex-col justify-center items-center gap-4">
            {state === "loading" && <Loader2 className="w-10 h-10 animate-spin" />}
            {state === "error" && <p className="text-red-500/80 font-bold">Something went wrong</p>}
            {state === "notFound" && <p className="text-yellow-500/80 font-bold">No categories found</p>}
            {state === "error" || state === "notFound" && (
              <button onClick={handleRefreshCategories}>
                <RefreshCw className="w-10 h-10 hover:animate-spin" />
              </button>)}
          </div>
        )}
        {state === null && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-1">
            {categories.map((category, index) => (
              <div key={`mark-dialog-category-${index}`} className={cn(
                "flex flex-row justify-between items-center",
                "border-b sm:border-r border-white/10",
              )}>
                <CheckBox
                  id={category.id.toString()}
                  label={category.category_name}
                  checked={toggledCategoryIds.includes(category.id)}
                  onChange={() => handleToggleCategory(category.id)}
                  className="truncate h-full w-full"
                />
                <DeleteButton
                  handleDelete={() => handleDeleteCategory(category.id)}
                />
              </div>
            ))}
          </div>
        )}
        {(state === null || state === "notFound") && (
          <CategoryCreator
            handleCreateCategory={handleCreateCategory}
            className="bg-transparent hover:bg-transparent border-none w-full p-0"
          />
        )}
      </DialogContent>
    </Dialog>
  )
}
