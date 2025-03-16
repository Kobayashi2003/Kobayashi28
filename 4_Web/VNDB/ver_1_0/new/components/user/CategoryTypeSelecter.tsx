"use client"

import { useEffect } from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

interface TypeOption {
  key: string
  value: string
  label: string
  labelSmall?: string
}

interface CategoryTypeSelecterProps {
  typeOptions: TypeOption[]
  selectedValue?: string
  onChange: (value: string) => void
  className?: string
}

export function CategoryTypeSelecter({ typeOptions, selectedValue, onChange, className }: CategoryTypeSelecterProps) {

  useEffect(() => {
    if (!selectedValue && typeOptions.length > 0) {
      onChange(typeOptions[0].value)
    }
  }, [typeOptions])

  return (
    <div className={cn(
      "flex flex-row flex-wrap gap-2",
      className
    )}>
      {typeOptions.map(typeOption => (
        <Button
          key={`category-type-${typeOption.key}`}
          size="default"
          variant="outline"
          onClick={() => onChange(typeOption.value)}
          className={cn(
            "bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 select-none",
            "text-white hover:text-white/80 text-base md:text-lg font-bold transition-all duration-300",
            selectedValue === typeOption.value && "border-2 border-white/40"
          )}
        >
          {typeOption.labelSmall ? (
            <>
              <span className="text-lg hidden sm:block">{typeOption.label}</span>
              <span className="text-sm block sm:hidden">{typeOption.labelSmall}</span>
            </>
          ) : (
            <span>{typeOption.label}</span>
          )}
        </Button>
      ))}
    </div>
  )
}