import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { LogIn } from "lucide-react";

interface LoginButtonProps {
  handleLogin: () => void
  disabled?: boolean
  className?: string
}

export function LoginButton({ handleLogin, disabled, className }: LoginButtonProps) {

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
      onClick={handleLogin}
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
      <LogIn className="w-4 h-4" />
    </Button>
  )
}
