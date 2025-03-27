import { cn } from "@/lib/utils"
import { InputBar } from "@/components/input/InputBar"
import { AddButton } from "@/components/button/AddButton"

interface CategoryCreatorProps {
  loading: boolean
  newCategoryName: string
  setNewCategoryName: (newCategoryName: string) => void
  handleCreateCategory: (e?: React.FormEvent) => void
  className?: string
}

export function CategoryCreator({ loading, newCategoryName, setNewCategoryName, handleCreateCategory, className }: CategoryCreatorProps) {
  return (
    <form onSubmit={handleCreateCategory} className={cn(
      "bg-[#0F2942]/80 hover:bg-[#0F2942] flex flex-row gap-2 p-4",
      "border border-white/10 hover:border-white/20 rounded-lg",
      "transition-all duration-300",
      className
    )}>
      <InputBar
        input={newCategoryName}
        setInput={setNewCategoryName}
        placeholder="New Category Name"
        disabled={loading}
        className="w-full"
      />
      <AddButton
        handleAdd={handleCreateCategory}
        disabled={loading}
      />
    </form>
  )
}