import { cn } from "@/lib/utils"
import { LetterButton } from "@/components/button/LetterButton"

interface TypeSelector2Props {
  selected: string
  onSelect: (value: string) => void
  disabled?: boolean
  className?: string
}

const typeOptions = [
  { value: "v", letter: "V" },
  { value: "r", letter: "R" },
  { value: "c", letter: "C" },
  { value: "p", letter: "P" },
  { value: "s", letter: "S" },
  { value: "g", letter: "G" },
  { value: "i", letter: "I" },
]

export function TypeSelector2({ selected, onSelect, disabled, className }: TypeSelector2Props) {
  return (
    <div className={(cn("flex flex-row flex-wrap gap-1", className))}>
      {typeOptions.map((typeOption) => (
        <LetterButton
          key={typeOption.value}
          letter={typeOption.letter}
          onClick={() => onSelect(typeOption.value)}
          disabled={disabled}
          className={cn(
            selected === typeOption.value && "border-2 border-white/40 hover:border-white/40"
          )}
        />
      ))}
    </div>
  )
}
