"use client"

import { cn } from "@/lib/utils"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { ArrowLeft, ArrowRight, ArrowUp, ArrowDown } from "lucide-react"

type Position = "top" | "bottom" | "left" | "right"

interface NavOption {
  key: string
  value: string
  label: string
  onClick?: () => void
}

interface NavBarProps {
  options: NavOption[]
  selectedValue: string
  position?: Position
  panelSize?: number
  className?: string
}

interface NavButtonProps {
  open: boolean
  position: Position
  setOpen: (open: boolean) => void
  className?: string
}

interface NavPanelProps {
  open: boolean
  options: NavOption[]
  selectedValue: string
  position: Position
  panelSize?: number
  setOpen: (open: boolean) => void
  className?: string
}

function NavButton({ open, position, setOpen, className }: NavButtonProps) {
  return (
    <Button
      variant="ghost"
      className={cn(
        "min-w-5 min-h-5",
        open ? "bg-white/2 hover:bg-white/5" : "bg-white/5 hover:bg-white/10",
        "text-white hover:text-white/80 font-bold text-base md:text-lg",
        "transition-all duration-300",
        (position === "top" || position === "bottom") && "w-full",
        (position === "left" || position === "right") && "h-full",
        position === "top" && "rounded-t-none",
        position === "bottom" && "rounded-b-none",
        position === "left" && "rounded-l-none",
        position === "right" && "rounded-r-none",
        className
      )}
      onClick={() => setOpen(!open)}
    >
    </Button>
  )
}

function NavPanel({ open, options, selectedValue, position, panelSize, setOpen, className }: NavPanelProps) {

  const minWidthWhenVertical = position === "left" || position === "right" ? panelSize : "auto"
  const minHeightWhenHorizontal = position === "top" || position === "bottom" ? panelSize : "auto"

  return (
    <div className={
      cn(
        "flex items-center select-none bg-[#0F2942]/60 hover:bg-[#0F2942]/80 backdrop-blur-sm rounded-lg font-bold text-base md:text-lg transition-all duration-300",
        (position === "top" || position === "bottom") && "w-full justify-between",
        (position === "left" || position === "right") && "h-full justify-between",
        !open ? "opacity-50 border-2 border-white/30 hover:border-white/40" : "gap-2 opacity-100 border border-white/10 hover:border-white/20",
        position === "top" && "border-t-0 flex-col h-full rounded-t-none",
        position === "bottom" && "border-b-0 flex-col-reverse h-full rounded-b-none",
        position === "left" && "border-l-0 flex-row h-full rounded-l-none",
        position === "right" && "border-r-0 flex-row-reverse h-full rounded-r-none",
        className
      )
    }>
      <div className={
        cn(
          "flex flex-col gap-4 justify-center items-center overflow-hidden",
          (position === "left" || position === "right") && "pt-4 pb-4",
          "transition-all duration-300",
          !open && "gap-0"
        )
      } style={{
        minWidth: minWidthWhenVertical,
        minHeight: minHeightWhenHorizontal,
      }}>
        {options.map((option) => (
          <Button
            key={option.key}
            variant={selectedValue === option.value ? "ghost" : "outline"}
            onClick={() => {
              option.onClick?.()
              // setOpen(false)
            }}
            className={cn(
              "flex flex-row justify-center items-center gap-2 w-full transition-all duration-300",
              selectedValue === option.value ?
                "bg-white/10 hover:bg-white/20" :
                "bg-transparent hover:bg-[#0F2942]/80 border-white/10 hover:border-white/20",
              "transition-all duration-300",
              !open && "p-0 opacity-0"
            )}
          >
            {open && selectedValue === option.value && (
              <>
                {position === "left" && <ArrowRight className="w-4 h-4" />}
                {position === "right" && <ArrowLeft className="w-4 h-4" />}
                {position === "top" && <ArrowDown className="w-4 h-4" />}
                {position === "bottom" && <ArrowUp className="w-4 h-4" />}
              </>
            )}
            {open && option.label}
          </Button>
        ))}
      </div>
      <NavButton
        open={open}
        position={position || "top"}
        setOpen={setOpen}
      />
    </div>
  )
}

export function NavBar({ options, selectedValue, position, panelSize, className }: NavBarProps) {

  const [open, setOpen] = useState(false)

  return (
    <div className={cn(
      (position === "left" || position === "right") && "h-full",
      (position === "top" || position === "bottom") && "w-full",
      className
    )}>
      <NavPanel
        open={open}
        options={options}
        selectedValue={selectedValue}
        position={position || "left"}
        panelSize={panelSize}
        setOpen={setOpen}
      />
    </div>
  )
}
