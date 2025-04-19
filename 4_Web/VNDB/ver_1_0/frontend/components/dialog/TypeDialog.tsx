import { RadioGroupDialog } from "@/components/dialog/RadioGroupDialog"

const typeOptions = [
  { value: "v", label: "Visual Novel" },
  { value: "r", label: "Release" },
  { value: "c", label: "Character" },
  { value: "p", label: "Producer" },
  { value: "s", label: "Staff" },
  { value: "g", label: "Tag" },
  { value: "i", label: "Trait" },
]

interface TypeDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  type: string
  setType: (type: string) => void
  className?: string
}

export function TypeDialog({ open, setOpen, type, setType, className }: TypeDialogProps) {
  return (
    <RadioGroupDialog
      open={open}
      setOpen={setOpen}
      title="Type"
      options={typeOptions}
      selected={type}
      setSelected={setType}
      className={className}
    />
  )
}