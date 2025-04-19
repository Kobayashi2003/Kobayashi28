import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { ArrowRight, Loader2 } from "lucide-react";

interface SubmitButtonProps {
  handleSubmit?: () => void
  disabled?: boolean
  className?: string
}

export function SubmitButton({ handleSubmit, disabled, className }: SubmitButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const icon = disabled ? <Loader2 className="w-4 h-4 animate-spin" /> : <ArrowRight className="w-4 h-4" />

  return (
    <IconButton
      icon={icon}
      variant="outline"
      onClick={handleSubmit}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}
