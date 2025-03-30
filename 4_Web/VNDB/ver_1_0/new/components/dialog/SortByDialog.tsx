import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

const sortByOptions: Record<string, {
  both?: { value: string, label: string }[],
  remote?: { value: string, label: string }[],
  local?: { value: string, label: string }[],
}> = {
  v: {
    both: [
      { value: "id", label: "Id" },
      { value: "title", label: "Title" },
      { value: "released", label: "Release Date" },
      { value: "rating", label: "Bayesian Rating" },
      { value: "votecount", label: "Vote Count" },
    ],
    remote: [
      { value: "searchrank", label: "Search Rank" },
    ],
    local: [
      { value: "average", label: "Raw Vote Average" },
      { value: "length_minutes", label: "Length (Minutes)" },
      { value: "length_votes", label: "Length (Votes)" },
      { value: "created_at", label: "Created At" },
      { value: "updated_at", label: "Updated At" },
    ],
  },
  r: {
    both: [
      { value: "id", label: "Id" },
      { value: "title", label: "Title" },
      { value: "released", label: "Release Date" },
    ],
    remote: [
      { value: "searchrank", label: "Search Rank" },
    ],
    local: [
      { value: "minage", label: "Minimum Age" },
      { value: "created_at", label: "Created At" },
      { value: "updated_at", label: "Updated At" },
    ],
  },
  c: {
    both: [
      { value: "id", label: "Id" },
      { value: "name", label: "Name" },
    ],
    remote: [
      { value: "searchrank", label: "Search Rank" },
    ],
    local: [
      { value: "original", label: "Original Name" },
      { value: "height", label: "Height" },
      { value: "weight", label: "Weight" },
      { value: "bust", label: "Bust" },
      { value: "waist", label: "Waist" },
      { value: "hips", label: "Hips" },
      { value: "age", label: "Age" },
      { value: "birthday", label: "Birthday" },
      { value: "created_at", label: "Created At" },
      { value: "updated_at", label: "Updated At" },
    ],
  },
  p: {
    both: [
      { value: "id", label: "Id" },
      { value: "name", label: "Name" },
    ],
    remote: [
      { value: "searchrank", label: "Search Rank" },
    ],
    local: [
      { value: "original", label: "Original Name" },
      { value: "created_at", label: "Created At" },
      { value: "updated_at", label: "Updated At" },
    ],
  },
  s: {
    both: [
      { value: "id", label: "Id" },
      { value: "name", label: "Name" },
    ],
    remote: [
      { value: "searchrank", label: "Search Rank" },
    ],
    local: [
      { value: "original", label: "Original Name" },
      { value: "created_at", label: "Created At" },
      { value: "updated_at", label: "Updated At" },
    ],
  },
  g: {
    both: [
      { value: "id", label: "Id" },
      { value: "name", label: "Name" },
      { value: "vn_count", label: "VN Count" },
    ],
    remote: [
      { value: "searchrank", label: "Search Rank" },
    ],
    local: [
      { value: "created_at", label: "Created At" },
      { value: "updated_at", label: "Updated At" },
    ],
  },
  i: {
    both: [
      { value: "id", label: "Id" },
      { value: "name", label: "Name" },
      { value: "char_count", label: "Character Count" },
    ],
    remote: [
      { value: "searchrank", label: "Search Rank" },
    ],
    local: [
      { value: "group_id", label: "Group Id" },
      { value: "group_name", label: "Group Name" },
      { value: "created_at", label: "Created At" },
      { value: "updated_at", label: "Updated At" },
    ],
  }
}

interface SortByDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  type: string
  from: string
  sortBy: string
  setSortBy: (sortBy: string) => void
  className?: string
}

export function SortByDialog({ open, setOpen, type, from, sortBy, setSortBy, className }: SortByDialogProps) {

  const showSortByOptions = {
    both: sortByOptions[type]?.both || [],
    remote: [...(sortByOptions[type]?.both || []), ...(sortByOptions[type]?.remote || [])],
    local: [...(sortByOptions[type]?.both || []), ...(sortByOptions[type]?.local || [])],
  }[from]

  const handleSortByChange = (value: string) => {
    setOpen(false)
    setSortBy(value)
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
          <DialogTitle className="text-xl text-white">Sort By</DialogTitle>
        </DialogHeader>
        <RadioGroup
          defaultValue={sortBy}
          onValueChange={handleSortByChange}
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-1">
            {showSortByOptions?.map((option) => (
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
