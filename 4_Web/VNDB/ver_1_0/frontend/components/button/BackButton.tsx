import { IconButton } from "@/components/button/IconButton"
import { ArrowBigLeft } from "lucide-react"

interface BackButtonProps {
  handleBack?: () => void
  disabled?: boolean
  className?: string
}

export function BackButton({ handleBack, disabled, className }: BackButtonProps) {
  return (
    <IconButton
      icon={<ArrowBigLeft className="w-4 h-4" />}
      variant="ghost"
      tooltip="Back"
      onClick={handleBack}
      disabled={disabled}
      className={className}
    />
  )
}