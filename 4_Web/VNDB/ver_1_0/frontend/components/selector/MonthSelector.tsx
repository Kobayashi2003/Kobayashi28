import { cn } from "@/lib/utils";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";

interface MonthSelectorProps {
  selectedMonth: string
  setSelectedMonth: (month: string) => void
  disabled?: boolean
  className?: string
}

export function MonthSelector({ selectedMonth, setSelectedMonth, disabled, className }: MonthSelectorProps) {

  const monthsSelectable = [
    { value: "00", label: "ALL" },
    { value: "01", label: "JAN" },
    { value: "02", label: "FEB" },
    { value: "03", label: "MAR" },
    { value: "04", label: "APR" },
    { value: "05", label: "MAY" },
    { value: "06", label: "JUN" },
    { value: "07", label: "JUL" },
    { value: "08", label: "AUG" },
    { value: "09", label: "SEP" },
    { value: "10", label: "OCT" },
    { value: "11", label: "NOV" },
    { value: "12", label: "DEC" }
  ]

  return (
    <Select value={selectedMonth} onValueChange={setSelectedMonth} disabled={disabled}>
      <SelectTrigger className={cn(
        "bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white font-bold",
        className
      )}>
        <SelectValue placeholder="Month" />
      </SelectTrigger>
      <SelectContent className="bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white font-bold">
        {monthsSelectable.map((month) => (
          <SelectItem key={month.value} value={month.value}>{month.label}</SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}

