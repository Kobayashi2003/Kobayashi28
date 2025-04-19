import { cn } from "@/lib/utils";
import { SwitchButton } from "../button/SwitchButton";
import { SortAsc, SortDesc } from "lucide-react";

interface OrderSwitchProps {
  order: string
  setOrder: (order: string) => void
  disabled?: boolean
  className?: string
}

export function OrderSwitch({ order, setOrder, disabled, className }: OrderSwitchProps) {

  const options = [
    { value: "asc", icon: <SortAsc className="w-4 h-4" />, tooltip: "Ascending" },
    { value: "desc", icon: <SortDesc className="w-4 h-4" />, tooltip: "Descending" },
  ]

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <SwitchButton 
      options={options}
      selected={order}
      onSelect={(value) => setOrder(value)}
      disabled={disabled}
      className={cn( buttonBgColor, className )}
    />
  )
}