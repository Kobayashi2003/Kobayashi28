import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

interface CancelButtonProps {
  handleCancel: () => void
  disabled?: boolean
  className?: string
}

export function CancelButton({ handleCancel, disabled, className }: CancelButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-red-500 hover:text-red-600"
  const buttonBorderColor = "border-red-500/20 hover:border-red-500/40"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={handleCancel}
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
      <X className="w-4 h-4" />
    </Button>
  )
}
