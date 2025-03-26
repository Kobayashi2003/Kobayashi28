import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Image, Text } from "lucide-react"

interface CardTypeButtonProps {
  cardType: "image" | "text"
  setCardType: (cardType: "image" | "text") => void
  disabled?: boolean
  className?: string
}

export function CardTypeButton({ cardType, setCardType, disabled, className }: CardTypeButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const buttonFont = "font-bold font-serif italic"
  const buttonTextSize = "text-base md:text-lg"
  const buttonTextColor = "text-white hover:text-white/80"
  const buttonBorderColor = "border-white/10 hover:border-white/20"
  const buttonAnimation = "transition-all duration-300"

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setCardType(cardType === "image" ? "text" : "image")}
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
      {cardType === "image" ? <Image className="w-4 h-4" /> : <Text className="w-4 h-4" />}
    </Button>
  )
}

