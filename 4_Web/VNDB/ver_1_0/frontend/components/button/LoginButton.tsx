import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { LogIn } from "lucide-react";

interface LoginButtonProps {
  handleLogin?: () => void
  disabled?: boolean
  className?: string
}

export function LoginButton({ handleLogin, disabled, className }: LoginButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <IconButton 
      icon={<LogIn className="w-4 h-4" />}
      variant="outline"
      tooltip="Login"
      onClick={handleLogin}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}
