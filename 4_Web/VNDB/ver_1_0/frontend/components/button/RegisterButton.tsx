import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { UserPlus } from "lucide-react";

interface RegisterButtonProps {
  handleRegister: () => void
  disabled?: boolean
  className?: string
}

export function RegisterButton({ handleRegister, disabled, className }: RegisterButtonProps) {
  
  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <IconButton
      icon={<UserPlus className="w-4 h-4" />}
      tooltip="Register"
      onClick={handleRegister}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}
