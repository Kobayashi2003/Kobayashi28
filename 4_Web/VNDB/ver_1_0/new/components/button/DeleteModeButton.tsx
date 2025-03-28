import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Trash } from "lucide-react";

interface DeleteModeButtonProps {
  deleteMode: boolean
  setDeleteMode: (deleteMode: boolean) => void
  disabled?: boolean
  className?: string
}

export function DeleteModeButton({ deleteMode, setDeleteMode, disabled, className }: DeleteModeButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = deleteMode ? "text-red-400 hover:text-red-500" : "text-white hover:text-red-400"
  const buttonBorderColor = deleteMode ? "border-red-400/40 hover:border-red-400/60" : "border-white/10 hover:border-white/20"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setDeleteMode(!deleteMode)}
      disabled={disabled}
      className={cn(
        "select-none",
        buttonBgColor,
        buttonFont,
        buttonTextSize,
        buttonTextColor,
        buttonBorderColor,
        buttonAnimation,
        className
      )}
    >
      <Trash className="w-4 h-4" />
    </Button>
  )
}