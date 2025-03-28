import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ArrowUp, ArrowDown } from "lucide-react";

interface OrderButtonProps {
  order: "asc" | "desc"
  setOrder: (order: "asc" | "desc") => void
  disabled?: boolean
  className?: string
}

export function OrderButton({ order, setOrder, disabled, className }: OrderButtonProps) {

  const buttonBgColor = "bg-transparent hover:bg-white/10"
  const buttonFont = "font-bold"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-white hover:text-white/80"
  const buttonBorderColor = "border-white/10 hover:border-white/20"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setOrder(order === "asc" ? "desc" : "asc")}
      disabled={disabled}
      className={cn(
        "select-none",
        buttonBgColor,
        buttonFont,
        buttonTextSize,
        buttonTextColor,
        buttonBorderColor,
        buttonAnimation,
        className
      )}
    >
      {order === "asc" ? <ArrowUp /> : <ArrowDown />}
    </Button>
  )
}
