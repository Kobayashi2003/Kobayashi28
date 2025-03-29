import { cn } from "@/lib/utils"
import { SwitchButton } from "@/components/button/SwitchButton"
import { Image, Text } from "lucide-react"

interface CardTypeSwitchProps {
  cardType: "image" | "text"
  setCardType: (cardType: "image" | "text") => void
  disabled?: boolean
  className?: string
}

export function CardTypeSwitch({ cardType, setCardType, disabled, className }: CardTypeSwitchProps) {

  const options = [
    { value: "image", icon: <Image className="w-4 h-4" />, tooltip: "Image" },
    { value: "text", icon: <Text className="w-4 h-4" />, tooltip: "Text" },
  ]

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <SwitchButton 
      options={options}
      selected={cardType}
      onSelect={(value) => setCardType(value as "image" | "text")}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}