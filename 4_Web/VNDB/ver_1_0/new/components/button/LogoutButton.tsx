import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { LogOut } from "lucide-react"

interface LogoutButtonProps {
  handleLogout: () => void
  disabled?: boolean
  className?: string
}

export function LogoutButton({ handleLogout, disabled, className }: LogoutButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-white hover:text-red-500"
  const buttonBorderColor = "border-white/10 hover:border-red-400/60"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={handleLogout}
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
      <LogOut className="w-4 h-4" />
    </Button>
  )
}
