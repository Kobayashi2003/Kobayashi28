import { RadioGroupDialog } from "@/components/dialog/RadioGroupDialog"

const fromOptions = [
  { value: "both", label: "Both" },
  { value: "remote", label: "Remote" },
  { value: "local", label: "Local" },
]

interface FromDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  from: string
  setFrom: (from: string) => void
  className?: string
}

export function FromDialog({ open, setOpen, from, setFrom, className }: FromDialogProps) {
  return (
    <RadioGroupDialog
      open={open}
      setOpen={setOpen}
      title="From"
      options={fromOptions}
      selected={from}
      setSelected={setFrom}
      className={className}
    />
  )
}