import { cn } from "@/lib/utils"
import { InputBar } from "@/components/input/InputBar"
import { AddButton } from "@/components/button/AddButton"

interface CategoryCreatorProps {
  newCategoryName: string
  setNewCategoryName: (newCategoryName: string) => void
  handleCreateCategory: () => void
  disabled?: boolean
  className?: string
}

export function CategoryCreator({ newCategoryName, setNewCategoryName, handleCreateCategory, disabled, className }: CategoryCreatorProps) {

  const containerFlex = "flex flex-row justify-between items-center gap-2"
  const containerBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const containerBorder = "border border-white/10 hover:border-white/20 rounded-lg"
  const containerTransition = "transition-all duration-300"

  return (
    <form onSubmit={handleCreateCategory} className={cn(
      "p-4",
      containerFlex,
      containerBgColor,
      containerBorder,
      containerTransition,
      className
    )}>
      <InputBar
        input={newCategoryName}
        setInput={setNewCategoryName}
        placeholder="New Category Name"
        disabled={disabled}
        className="w-full"
      />
      <AddButton
        handleAdd={() => { setNewCategoryName(""); handleCreateCategory() }}
        disabled={disabled}
      />
    </form>
  )
}