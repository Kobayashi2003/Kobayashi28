import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { 
  PanelLeftOpen, PanelLeftClose,
  PanelRightOpen, PanelRightClose,
  PanelTopOpen, PanelTopClose,
  PanelBottomOpen, PanelBottomClose
} from "lucide-react"

interface TogglePanelButtonProps {
  open: boolean
  setOpen: (open: boolean) => void
  direction: "left" | "right" | "top" | "bottom"
  disabled?: boolean
  className?: string
}

export function TogglePanelButton({ open, setOpen, direction, disabled, className }: TogglePanelButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const buttonFont = "font-bold font-serif italic"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-white hover:text-white/80"
  const buttonAnimation = "transition-all duration-300"
  const buttonBorderStyle = open ? "border-2 border-white/40" : "border-white/10 hover:border-white/20"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setOpen(!open)}
      disabled={disabled}
      className={cn(
        "select-none",
        buttonBgColor,
        buttonFont,
        buttonTextSize,
        buttonTextColor,
        buttonAnimation,
        buttonBorderStyle,
        className
      )}
    >
      {direction === "left" ? (
        open ? <PanelLeftClose className="w-4 h-4" /> : <PanelLeftOpen className="w-4 h-4" />
      ) : direction === "right" ? (
        open ? <PanelRightClose className="w-4 h-4" /> : <PanelRightOpen className="w-4 h-4" />
      ) : direction === "top" ? (
        open ? <PanelTopClose className="w-4 h-4" /> : <PanelTopOpen className="w-4 h-4" />
      ) : ( // bottom
        open ? <PanelBottomClose className="w-4 h-4" /> : <PanelBottomOpen className="w-4 h-4" />
      )}
    </Button>
  )
}
