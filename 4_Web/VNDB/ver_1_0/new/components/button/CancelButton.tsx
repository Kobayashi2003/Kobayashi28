import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { X } from "lucide-react";

interface CancelButtonProps {
  handleCancel?: () => void
  disabled?: boolean
  className?: string
}

export function CancelButton({ handleCancel, disabled, className }: CancelButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const buttonTextColor = "text-red-500 hover:text-red-600"
  const buttonBorderColor = "border-red-500/20 hover:border-red-500/40"

  return (
    <IconButton
      icon={<X className="w-4 h-4" />}
      variant="outline"
      onClick={handleCancel}
      disabled={disabled}
      className={cn(
        buttonBgColor,
        buttonTextColor,
        buttonBorderColor,
        className
      )}
    />
  )
}
