import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { Filter } from "lucide-react";

interface FilterButtonProps {
  onClick?: () => void
  disabled?: boolean
  className?: string
}

export function FilterButton({ onClick, disabled, className }: FilterButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <IconButton
      icon={<Filter className="w-4 h-4" />}
      tooltip="Filter"
      variant="outline"
      onClick={onClick}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}