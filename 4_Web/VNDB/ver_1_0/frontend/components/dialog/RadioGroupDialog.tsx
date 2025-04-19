import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

interface Option {
  value: string
  label: string
}

interface RadioGroupDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  title: string
  options: Option[]
  selected: string
  setSelected: (selected: string) => void
  className?: string
}

export function RadioGroupDialog({ open, setOpen, title, options, selected, setSelected, className }: RadioGroupDialogProps) {

  const handleValueChange = (value: string) => {
    setSelected(value)
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className={cn(
        "bg-[#0F2942]/80 border-white/10",
        "data-[state=open]:animate-in data-[state=closed]:animate-out",
        "data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
        "data-[state=closed]:slide-out-to-bottom-1/2 data-[state=open]:slide-in-from-bottom-1/2",
        className
      )}>
        <DialogHeader>
          <DialogTitle className="text-xl text-white">{title}</DialogTitle>
        </DialogHeader>
        <RadioGroup
          defaultValue={selected}
          onValueChange={handleValueChange}
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-1">
            {options?.map((option) => (
              <div key={`sortBy-option-${option.value}`} className={cn(
                "group",
                "flex flex-row justify-start items-center",
                "border-b sm:border-r border-white/10",
              )}>
                <RadioGroupItem
                  id={`sortBy-option-${option.value}`}
                  value={option.value}
                  className={cn(
                    "border-white/60 group-hover:border-white",
                    "data-[state=checked]:bg-white data-[state=checked]:text-[#0F2942]"
                  )}
                />
                <Label
                  htmlFor={`sortBy-option-${option.value}`}
                  className={cn(
                    "ml-1",
                    "h-full w-full",
                    "text-white truncate",
                    "font-normal group-hover:font-bold",
                    "text-xs sm:text-sm md:text-base",
                    "cursor-pointer"
                  )}>
                  {option.label}
                </Label>
              </div>
            ))}
          </div>
        </RadioGroup>
      </DialogContent>
    </Dialog>
  )
}
