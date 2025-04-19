import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { Settings2 } from "lucide-react";

interface Settings2ButtonProps {
  onClick?: () => void
  disabled?: boolean
  className?: string
}

export function Settings2Button({ onClick, disabled, className }: Settings2ButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <IconButton
      icon={<Settings2 className="w-4 h-4" />}
      tooltip="Settings"
      variant="outline"
      onClick={onClick}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}
