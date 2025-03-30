import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { Menu } from "lucide-react";

interface MenuButtonProps {
  onClick: () => void
  disabled?: boolean
  className?: string
}

export function MenuButton({ onClick, disabled, className }: MenuButtonProps) {

  const buttonBgColor = "bg-transparent hover:bg-white/10"

  return (
    <IconButton
      icon={<Menu className="w-4 h-4" />}
      tooltip="Menu"
      variant="ghost"
      onClick={onClick}
      disabled={disabled}
      className={cn(buttonBgColor, className)}
    />
  )
}