import { cn } from "@/lib/utils"
import { IconButton } from "@/components/button/IconButton"
import { Trash2 } from "lucide-react"

interface DeleteButtonProps {
  handleDelete?: () => void
  disabled?: boolean
  className?: string
}

export function DeleteButton({ handleDelete, disabled, className }: DeleteButtonProps) {

  const buttonBgColor = "bg-transparent hover:bg-red-400/10"
  const buttonTextColor = "text-red-400 hover:text-white"
  const buttonBorderColor = "border-red-400/40 hover:border-red-400/60"

  return (
    <IconButton
      icon={<Trash2 className="w-4 h-4" />}
      variant="outline"
      onClick={handleDelete}
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