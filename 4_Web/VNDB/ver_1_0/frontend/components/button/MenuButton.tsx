"use client"

import { useState } from "react"

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Menu } from "lucide-react";

interface Option {
  name: string
  onClick: () => void
  disabled?: boolean
  className?: string
}

interface MenuButtonProps {
  options: Option[]
  disabled?: boolean
  className?: string
}

export function MenuButton({ options, disabled, className }: MenuButtonProps) {

  const [open, setOpen] = useState(false)

  return (
    <Popover open={open && !disabled} onOpenChange={setOpen}>
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
          <Menu className="w-4 h-4" />
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
        {options.map((option) => (
          <Button
            key={option.name}
            variant="ghost"
            disabled={option.disabled}
            className={cn(
              "w-full",
              "text-white hover:text-white",
              "font-normal hover:font-bold",
              "text-xs sm:text-sm md:text-base",
              "w-full justify-center",
              "hover:bg-white/10",
              option.className
            )}
            onClick={() => {
              option.onClick()
              setOpen(false)
            }}
          >
            {option.name}
          </Button>
        ))}
      </PopoverContent>
    </Popover>
  )
}