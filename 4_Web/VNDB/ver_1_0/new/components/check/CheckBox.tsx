import { cn } from "@/lib/utils"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"

interface CheckBoxProps {
  id: string
  label: string
  checked: boolean
  onChange: (checked: boolean) => void
  disabled?: boolean
  className?: string
}

export function CheckBox({ id, label, checked, onChange, disabled, className }: CheckBoxProps) {

  const containerStyle = cn(
    "flex flex-row justify-start items-center",
    "group",
    className
  )

  const checkboxStyle = cn(
    "border-white/60 group-hover:border-white",
    "data-[state=checked]:bg-white data-[state=checked]:text-[#0F2942]"
  )

  const labelStyle = cn(
    "w-full h-full",
    "ml-1",
    "text-white",
    "font-normal group-hover:font-bold",
    "cursor-pointer"
  )

  return (
    <div className={containerStyle}>
      <Checkbox id={id} checked={checked} onCheckedChange={onChange} disabled={disabled} className={checkboxStyle} />
      <Label htmlFor={id} className={labelStyle}>{label}</Label>
    </div>
  )
}
