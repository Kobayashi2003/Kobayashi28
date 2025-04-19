import { PopoverButton } from "@/components/button/PopoverButton"

interface TypeSelector1Props {
  selected: string
  onSelect: (value: string) => void
  disabled?: boolean
  className?: string
}

const typeOptions = [
  { value: "v", label: "Visual Novels", letter: "V" },
  { value: "r", label: "Releases", letter: "R" },
  { value: "c", label: "Characters", letter: "C" },
  { value: "p", label: "Producers", letter: "P" },
  { value: "s", label: "Staff", letter: "S" },
  { value: "g", label: "Tags", letter: "G" },
  { value: "i", label: "Traits", letter: "I" },
]

export function TypeSelector1({ selected, onSelect, disabled, className }: TypeSelector1Props) {
  return (
    <PopoverButton
      options={typeOptions}
      selected={selected}
      onSelect={onSelect}
      disabled={disabled}
      className={className}
    />
  )
}
