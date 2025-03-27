import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { UserPlus } from "lucide-react";

interface RegisterButtonProps {
  handleRegister: () => void
  disabled?: boolean
  className?: string
}

export function RegisterButton({ handleRegister, disabled, className }: RegisterButtonProps) {
  
  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-white hover:text-white/80"
  const buttonBorderColor = "border-white/10 hover:border-white/20"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button 
      variant="outline"
      size="icon"
      onClick={handleRegister}
      disabled={disabled}
      className={cn(
        buttonBgColor,
        buttonFont,
        buttonTextSize,
        buttonTextColor,
        buttonBorderColor,
        buttonAnimation,
        className
      )}
    >
      <UserPlus className="w-4 h-4" />
    </Button>
  )
}
