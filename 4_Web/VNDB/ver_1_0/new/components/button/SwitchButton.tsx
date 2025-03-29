import { IconButton } from "@/components/button/IconButton"

interface Option {
  value: string
  icon: React.ReactNode
  tooltip?: string
}

interface SwitchButtonProps {
  options: Option[]
  selected: string
  onSelect: (value: string) => void
  disabled?: boolean
  className?: string
}

export function SwitchButton({ options, selected, onSelect, disabled, className }: SwitchButtonProps) {
  return (
    <IconButton 
      variant="outline"
      icon={options.find(option => option.value === selected)?.icon}
      tooltip={options.find(option => option.value === selected)?.tooltip}
      onClick={() => {
        const nextIndex = (options.findIndex(option => option.value === selected) + 1) % options.length
        onSelect(options[nextIndex].value)
      }}
      disabled={disabled}
      className={className}
    />
  )
}
