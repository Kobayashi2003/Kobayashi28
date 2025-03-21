import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { PanelLeftOpen, PanelLeftClose } from "lucide-react"


interface ShowPanelButtonProps {
  open: boolean
  setOpen: (open: boolean) => void
}

export function ShowPanelButton({ open, setOpen }: ShowPanelButtonProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setOpen(!open)}
      className={cn(
        "bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 select-none",
        "text-white hover:text-white/80 text-base md:text-lg font-bold transition-all duration-300",
        open ? "border-2 border-white/40" : "border-white/10 hover:border-white/20"
      )}
    >
      {open ? <PanelLeftClose className="w-4 h-4" /> : <PanelLeftOpen className="w-4 h-4" />}
    </Button>
  )
}
