import { Button } from "../ui/button"
import { Image, Text } from "lucide-react"

interface CardTypeSelecterProps {
  selected: "image" | "text"
  onSelect: (type: "image" | "text") => void
  className?: string
}

export function CardTypeSelecter({ selected, onSelect, className }: CardTypeSelecterProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => onSelect(selected === "image" ? "text" : "image")}
      className={`bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 
      text-white hover:text-white/80 text-base md:text-lg font-bold font-serif italic transition-all duration-300  ${className}`}
    >
      {selected === "image" ? <Image /> : <Text />}
    </Button>
  )
}
