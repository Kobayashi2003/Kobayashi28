import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { Plus } from "lucide-react";

interface AddButtonProps {
  handleAdd?: () => void
  disabled?: boolean
  className?: string
}

export function AddButton({ handleAdd, disabled, className }: AddButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <IconButton
      icon={<Plus className="w-4 h-4" />}
      variant="outline"
      tooltip="Add"
      onClick={handleAdd}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}
