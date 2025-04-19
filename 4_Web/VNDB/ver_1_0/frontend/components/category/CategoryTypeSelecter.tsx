import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { TypeSelector2 } from "@/components/selector/TypeSelector2"

interface TypeOption {
  key: string
  value: string
  label: string
}

interface CategoryTypeSelecterProps {
  typeOptions: TypeOption[]
  selectedValue: string
  onChange: (value: string) => void
  size?: "default" | "sm" | "lg" | "icon" | null | undefined
  className?: string
}

export function CategoryTypeSelecter({ typeOptions, selectedValue, onChange, size, className }: CategoryTypeSelecterProps) {

  return (
    <TypeSelector2
      selected={selectedValue}
      onSelect={onChange}
      // disabled={disabled}
      className={className}
    />
  )

  return (
    <div className={cn(
      "flex flex-row flex-wrap gap-2",
      className
    )}>
      {typeOptions.map(typeOption => (
        <Button
          key={`category-type-${typeOption.key}`}
          size={size}
          variant="outline"
          onClick={() => onChange(typeOption.value)}
          className={cn(
            "bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 select-none",
            "text-white hover:text-white/80 text-base md:text-lg font-bold transition-all duration-300",
            selectedValue === typeOption.value && "border-2 border-white/40"
          )}
        >
          <span>{typeOption.label}</span>
        </Button>
      ))}
    </div>
  )
}