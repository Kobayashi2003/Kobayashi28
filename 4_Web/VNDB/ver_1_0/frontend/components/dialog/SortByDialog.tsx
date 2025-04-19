import { RadioGroupDialog } from "@/components/dialog/RadioGroupDialog"

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
  additionalOptions?: { value: string, label: string }[]
  className?: string
}

export function SortByDialog({ open, setOpen, type, from, sortBy, setSortBy, additionalOptions, className }: SortByDialogProps) {

  let showSortByOptions = {
    both: sortByOptions[type]?.both || [],
    remote: [...(sortByOptions[type]?.both || []), ...(sortByOptions[type]?.remote || [])],
    local: [...(sortByOptions[type]?.both || []), ...(sortByOptions[type]?.local || [])],
  }[from] ?? []

  if (additionalOptions) {
    showSortByOptions = [...showSortByOptions, ...additionalOptions]
  }

  return (
    <RadioGroupDialog
      open={open}
      setOpen={setOpen}
      title="Sort By"
      options={showSortByOptions}
      selected={sortBy}
      setSelected={setSortBy}
      className={className}
    />
  )
}
