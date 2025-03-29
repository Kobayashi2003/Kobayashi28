import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { Settings } from "lucide-react";

interface SettingsButtonProps {
  onClick?: () => void
  disabled?: boolean
  className?: string
}

export function SettingsButton({ onClick, disabled, className }: SettingsButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <IconButton
      icon={<Settings className="w-4 h-4" />}
      tooltip="Settings"
      variant="outline"
      onClick={onClick}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}