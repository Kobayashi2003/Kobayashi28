import { Check } from "lucide-react"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import type { SearchType } from "@/lib/types"

interface SortOptionsProps {
  searchType: SearchType
  sortBy: string
  sortOrder: "asc" | "desc"
  onSortByChange: (value: string) => void
  onSortOrderChange: (value: "asc" | "desc") => void
}

interface SortOption {
  value: string
  label: string
}

const sortOptions: Record<SearchType, SortOption[]> = {
  vn: [
    { value: "id", label: "Id" },
    { value: "title", label: "Title" },
    { value: "released", label: "Release Date" },
  ],
  release: [
    { value: "id", label: "Id" },
    { value: "title", label: "Title" },
    { value: "released", label: "Release Date" },
  ],
  character: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name" },
  ],
  producer: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name" },
  ],
  staff: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name" },
  ],
  tag: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name" },
  ],
  trait: [
    { value: "id", label: "Id" },
    { value: "name", label: "Name" },
    { value: "group_id", label: "Group Id" },
    { value: "group_name", label: "Group Name" },
  ],
}

const orderOptions: SortOption[] = [
  { value: "asc", label: "Ascending" },
  { value: "desc", label: "Descending" },
]

function SortByGrid({
  options,
  value,
  onValueChange,
}: {
  options: SortOption[]
  value: string
  onValueChange: (value: string) => void
}) {
  return (
    <RadioGroup
      value={value}
      onValueChange={onValueChange}
      className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2"
    >
      {options.map((option) => (
        <div
          key={option.value}
          className={`relative flex items-center justify-between rounded-lg border border-white/10 p-4 transition-colors hover:bg-white/5 ${
            value === option.value ? "bg-white/10" : ""
          }`}
        >
          <Label htmlFor={option.value} className="block w-full cursor-pointer font-medium">
            {option.label}
          </Label>
          <RadioGroupItem value={option.value} id={option.value} className="hidden" />
          {value === option.value && <Check className="h-4 w-4 text-white absolute right-4" />}
        </div>
      ))}
    </RadioGroup>
  )
}

function OrderOptions({
  value,
  onValueChange,
}: {
  value: "asc" | "desc"
  onValueChange: (value: "asc" | "desc") => void
}) {
  return (
    <RadioGroup value={value} onValueChange={onValueChange} className="grid grid-cols-1 sm:grid-cols-2 gap-2">
      {orderOptions.map((option) => (
        <div
          key={option.value}
          className={`relative flex items-center justify-between rounded-lg border border-white/10 p-4 transition-colors hover:bg-white/5 ${
            value === option.value ? "bg-white/10" : ""
          }`}
        >
          <Label htmlFor={option.value} className="block w-full cursor-pointer font-medium">
            {option.label}
          </Label>
          <RadioGroupItem value={option.value} id={option.value} className="hidden" />
          {value === option.value && <Check className="h-4 w-4 text-white absolute right-4" />}
        </div>
      ))}
    </RadioGroup>
  )
}

export function SortOptions({ searchType, sortBy, sortOrder, onSortByChange, onSortOrderChange }: SortOptionsProps) {
  return (
    <div className="space-y-8">
      <div>
        <Label className="mb-4 block text-lg font-semibold">Sort By</Label>
        <SortByGrid options={sortOptions[searchType]} value={sortBy} onValueChange={onSortByChange} />
      </div>
      <div>
        <Label className="mb-4 block text-lg font-semibold">Order</Label>
        <OrderOptions value={sortOrder} onValueChange={onSortOrderChange} />
      </div>
    </div>
  )
}