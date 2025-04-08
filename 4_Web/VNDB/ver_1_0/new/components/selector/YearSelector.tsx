import { cn } from "@/lib/utils";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";

interface YearSelectorProps {
  selectedYear: string
  setSelectedYear: (year: string) => void
  disabled?: boolean
  className?: string
}

export function YearSelector({ selectedYear, setSelectedYear, disabled, className }: YearSelectorProps) {

  const currentYear = new Date().getFullYear()

  const yearsSelectable = [
    { value: "00", label: "ALL" },
    ...Array.from({ length: currentYear - 1985 + 2 }, (_, i) => ({
      value: (1985 + i).toString(),
      label: (1985 + i).toString()
    }))
  ]

  return (
    <Select value={selectedYear} onValueChange={setSelectedYear} disabled={disabled}>
      <SelectTrigger className={cn(
        "bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white font-bold",
        className
      )}>
        <SelectValue placeholder="Year" />
      </SelectTrigger>
      <SelectContent className="bg-[#0F2942]/80 border-white/10 hover:border-white/20 text-white font-bold">
        {yearsSelectable.map((year) => (
          <SelectItem key={year.value} value={year.value}>{year.label}</SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}