import { cn } from "@/lib/utils"
import { SwitchButton } from "@/components/button/SwitchButton"
import { LayoutGrid, AlignJustify } from "lucide-react"

interface GridLayoutSwitchProps {
  layout: "single" | "grid"
  setLayout: (layout: "single" | "grid") => void
  disabled?: boolean
  className?: string
}

export function GridLayoutSwitch({ layout, setLayout, disabled, className }: GridLayoutSwitchProps) {
  const options = [
    { value: "single", icon: <AlignJustify className="w-4 h-4" />, tooltip: "Single Row" },
    { value: "grid", icon: <LayoutGrid className="w-4 h-4" />, tooltip: "Grid Layout" },
  ]

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <SwitchButton 
      options={options}
      selected={layout}
      onSelect={(value) => setLayout(value as "single" | "grid")}
      disabled={disabled}
      className={cn(buttonBgColor, className)}
    />
  )
} 