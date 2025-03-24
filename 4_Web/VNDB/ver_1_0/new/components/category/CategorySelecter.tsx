import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { DeleteButton } from "@/components/common/DeleteButton"

interface CategoryOption {
  key: string
  value: number
  label: string
  labelSmall?: string
}

interface CategorySelecterProps {
  loading: boolean
  categoryOptions: CategoryOption[]
  selectedValue?: number | undefined
  deleteMode: boolean
  setToDeleteId: (id: number) => void
  handleDeleteCategory: () => void
  onChange: (value: number | undefined) => void
  className?: string
}

export function CategorySelecter({ loading, categoryOptions, selectedValue, deleteMode, setToDeleteId, handleDeleteCategory, onChange, className }: CategorySelecterProps) {
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
            disabled={loading}
            onClick={() => {
              if (selectedValue === categoryOption.value) {
                onChange(undefined)
              } else {
                onChange(categoryOption.value)
              }
            }}
            className={cn(
              "flex-1",
              "border-white/10 hover:border-white/20 hover:bg-white/20",
              "text-white hover:text-white/80 text-base md:text-lg font-bold",
              "transition-all duration-300",
              selectedValue === categoryOption.value && "bg-white/10",
              loading && "animate-pulse"
            )}
          >
            {categoryOption.label}
          </Button>
          {deleteMode && (
            <DeleteButton
              loading={loading}
              onClick={() => {
                setToDeleteId(categoryOption.value)
                handleDeleteCategory()
              }}
            />
          )}
        </div>
      ))}
    </div>
  )
}