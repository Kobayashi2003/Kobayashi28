import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { RefreshCw } from "lucide-react"

interface ReloadButtonProps {
  onClick: () => void
  className?: string
}

export function ReloadButton({ onClick, className }: ReloadButtonProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={onClick}
      className={cn(
        "text-base md:text-lg font-bold",
        "transition-all duration-300",
        "text-blue-400 hover:text-white", 
        "bg-transparent hover:bg-blue-400",
        "border-blue-400/40 hover:border-blue-400/60",
        "group",
        className
      )}
    >
      <RefreshCw className="w-4 h-4 group-hover:animate-spin" />
    </Button>
  )
}