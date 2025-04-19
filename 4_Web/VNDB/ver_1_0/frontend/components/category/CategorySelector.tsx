import { cn } from "@/lib/utils";
import { BarButton } from "@/components/button/BarButton";
import { DeleteButton } from "@/components/button/DeleteButton";

interface CategoryOption {
  value: number
  label: string
}

interface CategorySelectorProps {
  categoryOptions: CategoryOption[]
  selectedValue: number | undefined
  setSelectedValue: (value: number | undefined) => void
  deleteMode?: boolean
  handleDelete: (value: number) => void
  disabled?: boolean
  className?: string
}

export function CategorySelector({ categoryOptions, selectedValue, setSelectedValue, deleteMode, handleDelete, disabled, className }: CategorySelectorProps) {
  return (
    <div className={cn(
      "p-4",
      "flex flex-col gap-2",
      "bg-[#0F2942]/80 hover:bg-[#0F2942]",
      "border border-white/10 hover:border-white/20 rounded-lg",
      "transition-all duration-300",
      className
    )}>
      {categoryOptions.map(option => (
        <div key={option.value} className="flex flex-row gap-2">
          <BarButton
            content={option.label}
            variant="outline"
            onClick={() => {
              if (selectedValue === option.value) {
                setSelectedValue(undefined)
              } else {
                setSelectedValue(option.value)
              }
            }}
            disabled={disabled}
            className={cn(
              "flex-1",
              selectedValue === option.value && "bg-white/10"
            )}
          />
          {deleteMode && (
            <DeleteButton handleDelete={() => handleDelete(option.value)} />
          )}
        </div>
      ))}
    </div>
  )
}
