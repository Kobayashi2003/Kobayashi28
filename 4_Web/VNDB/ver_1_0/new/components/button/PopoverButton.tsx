"use client"

import { useState } from "react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

interface Option {
  value: string
  label: string
  letter: string
}

interface PopoverButtonProps {
  options: Option[]
  selected: string
  onSelect: (value: string) => void
  disabled?: boolean
  className?: string
}

export function PopoverButton({ options, selected, onSelect, disabled, className }: PopoverButtonProps) {
  const [open, setOpen] = useState(false)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          disabled={disabled}
          className={cn(
            "select-none",
            "bg-[#0F2942]/80 hover:bg-[#0F2942]",
            "font-bold font-serif italic",
            "text-base md:text-lg",
            "text-white hover:text-white/80",
            "border-white/10 hover:border-white/20",
            "transition-all duration-300",
            className
          )}
        >
          {options.find(option => option.value === selected)?.letter || ""}
        </Button>
      </PopoverTrigger>
      <PopoverContent className={cn(
        "select-none",
        "p-1",
        "min-w-0 w-fit",
        "bg-[#0F2942]/80 hover:bg-[#0F2942]",
        "border-white/10 hover:border-white/20",
        "transition-all duration-300",
      )} align="start">
        <div className={cn(
          "flex flex-col gap-1",
        )}>
          {options.map((option) => (
            <Button
              key={option.value}
              variant="ghost"
              className={cn(
                "text-white hover:text-white",
                "font-normal hover:font-bold",
                "text-xs sm:text-sm md:text-base",
                "w-full justify-start",
                "hover:bg-white/10",
                selected === option.value ? "bg-white/10" : "",
              )}
              onClick={() => {
                onSelect(option.value)
                setOpen(false)
              }}
            >
              <span className={cn(
                "mr-2",
                "font-serif font-black italic",
              )}>
                {option.letter}
              </span>
              {option.label}
            </Button>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  )
}