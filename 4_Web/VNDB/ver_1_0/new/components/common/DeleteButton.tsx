import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Trash2 } from "lucide-react"

interface DeleteButtonProps {
  loading: boolean
  onClick: () => void
  className?: string
}

export function DeleteButton({ loading, onClick, className }: DeleteButtonProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      disabled={loading}
      onClick={onClick}
      className={cn(
        "text-base md:text-lg font-bold",
        "transition-all duration-300",
        "text-red-400 hover:text-white", 
        "bg-transparent hover:bg-red-400",
        "border-red-400/40 hover:border-red-400/60",
        loading && "animate-pulse"
      )}
    >
      <Trash2 className="w-4 h-4" />
    </Button>
  )
}