import { cn } from "@/lib/utils"
import { IconButton } from "./IconButton"
import { LogOut } from "lucide-react"

interface LogoutButtonProps {
  handleLogout?: () => void
  disabled?: boolean
  className?: string
}

export function LogoutButton({ handleLogout, disabled, className }: LogoutButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const buttonTextColor = "text-white hover:text-red-500"
  const buttonBorderColor = "border-white/10 hover:border-red-400/60"

  return (
    <IconButton
      icon={<LogOut className="w-4 h-4" />}
      variant="outline"
      tooltip="Logout"
      onClick={handleLogout}
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
