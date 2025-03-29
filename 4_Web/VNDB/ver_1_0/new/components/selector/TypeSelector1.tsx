import { PopoverButton } from "@/components/button/PopoverButton"

interface TypeSelector1Props {
  selected: string
  onSelect: (value: string) => void
  disabled?: boolean
  className?: string
}

const typeOptions = [
  { value: "vn", label: "Visual Novels", letter: "V" },
  { value: "release", label: "Releases", letter: "R" },
  { value: "character", label: "Characters", letter: "C" },
  { value: "producer", label: "Producers", letter: "P" },
  { value: "staff", label: "Staff", letter: "S" },
  { value: "tag", label: "Tags", letter: "G" },
  { value: "trait", label: "Traits", letter: "I" },
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
