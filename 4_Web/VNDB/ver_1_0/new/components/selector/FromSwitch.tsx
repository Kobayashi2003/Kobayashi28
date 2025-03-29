import { cn } from "@/lib/utils";
import { SwitchButton } from "../button/SwitchButton";

interface FromSwitchProps {
  selected: string
  setSelected: (selected: string) => void
  disabled?: boolean
  className?: string
}

export function FromSwitch({ selected, setSelected, disabled, className }: FromSwitchProps) {

  const options = [
    { value: "remote", icon: <span className="font-bold font-serif italic">R</span>, tooltip: "Remote" },
    { value: "local", icon: <span className="font-bold font-serif italic">L</span>, tooltip: "Local" },
    { value: "both", icon: <span className="font-bold font-serif italic">B</span>, tooltip: "Both" },
  ]

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <SwitchButton 
      options={options}
      selected={selected}
      onSelect={(value) => setSelected(value)}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}