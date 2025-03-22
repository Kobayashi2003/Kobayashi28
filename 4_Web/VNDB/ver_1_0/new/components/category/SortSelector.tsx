"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { SlidersHorizontal } from "lucide-react"

interface SortSelectorProps {
  type: string
  sortBy: string
  sortOrder: string
  setSortBy: (sortBy: string) => void
  setSortOrder: (sortOrder: string) => void
}

interface SelectorButtonProps {
  setOpen: (open: boolean) => void
}

interface SelectorPanelProps {
  type: string
  open: boolean
  sortBy: string
  sortOrder: string
  setOpen: (open: boolean) => void
  setSortBy: (sortBy: string) => void
  setSortOrder: (sortOrder: string) => void
} 

const sortByOptions: Record<string, {value: string, label: string, sortable?: boolean}[]> = {
  v: [
    {value: "id", label: "Id"},
    {value: "title", label: "Title"},
    {value: "released", label: "Release Date"},
    {value: "rating", label: "Bayesian Rating"},
    {value: "average", label: "Raw Vote Average", sortable: false},
    {value: "votecount", label: "Vote Count"},
    {value: "marked_at", label: "Marked At"},
  ],
  c: [
    {value: "id", label: "Id"},
    {value: "name", label: "Name"},
    {value: "birthday", label: "Birthday", sortable: false},
    {value: "age", label: "Age", sortable: false},
    {value: "height", label: "Height", sortable: false},
    {value: "weight", label: "Weight", sortable: false},
    {value: "bust", label: "Bust", sortable: false},
    {value: "waist", label: "Waist", sortable: false},
    {value: "hips", label: "Hips", sortable: false},
    {value: "marked_at", label: "Marked At"},
  ],
  p: [
    {value: "id", label: "Id"},
    {value: "name", label: "Name"},
    {value: "marked_at", label: "Marked At"},
  ],
  s: [
    {value: "id", label: "Id"},
    {value: "name", label: "Name"},
    {value: "marked_at", label: "Marked At"},
  ]
}

const sortOrderOptions: {value: string, label: string}[] = [
  {value: "asc", label: "Ascending"},
  {value: "desc", label: "Descending"},
]

function SortSelectorButton({ setOpen } : SelectorButtonProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setOpen(true)}
      className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 
      text-white hover:text-white/80 text-base md:text-lg font-bold font-serif italic transition-all duration-300"
    >
      <SlidersHorizontal className="h-4 w-4" />
    </Button>
  )
}

function SortSelectorPanel({ type, open, sortBy, sortOrder, setOpen, setSortBy, setSortOrder } : SelectorPanelProps ) {
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="bg-[#0F2942]/80 border-white/10">
        <DialogHeader>
          <DialogTitle className="text-xl text-white/80">Sort By</DialogTitle>
        </DialogHeader>
        <RadioGroup
          defaultValue={sortBy}
          onValueChange={(value) => setSortBy(value)}
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-1">
            {sortByOptions[type].map((option) => (
              <div key={`sortBy-option-${option.value}`} className={`flex flex-row items-center justify-between border-b sm:border-r border-white/10 ${option.sortable === false ? "pointer-events-none" : ""}`}>
                <div className="h-full flex-grow min-w-0 flex flex-row items-center group truncate">
                  <RadioGroupItem 
                    id={`sortBy-option-${option.value}`} 
                    value={option.value} 
                    className={`flex-shrink-0 border-white/60 group-hover:border-white data-[state=checked]:bg-white data-[state=checked]:text-[#0F2942] ${option.sortable === false ? "text-white/30" : ""}`}
                  />
                  <Label htmlFor={`sortBy-option-${option.value}`} className={`w-full h-full text-white text-base sm:text-lg group-hover:font-bold cursor-pointer ml-1 ${option.sortable === false ? "text-white/30" : ""}`}>
                    {option.label}
                  </Label>
                </div>
              </div>
            ))}
          </div>
        </RadioGroup>
        <DialogHeader>
          <DialogTitle className="text-xl text-white/80">Sort Order</DialogTitle>
        </DialogHeader>
        <RadioGroup
          defaultValue={sortOrder}
          onValueChange={(value) => setSortOrder(value)}
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-1">
            {sortOrderOptions.map((option) => (
              <div key={`sortOrder-option-${option.value}`} className="flex flex-row items-center justify-between border-b sm:border-r border-white/10">
                <div className="h-full flex-grow min-w-0 flex flex-row items-center group truncate">
                  <RadioGroupItem 
                    id={`sortOrder-option-${option.value}`} 
                    value={option.value} 
                    className="flex-shrink-0 border-white/60 group-hover:border-white data-[state=checked]:bg-white data-[state=checked]:text-[#0F2942]"
                  />
                  <Label htmlFor={`sortOrder-option-${option.value}`} className="w-full h-full text-white text-base sm:text-lg group-hover:font-bold cursor-pointer ml-1">
                    {option.label}
                  </Label>
                </div>
              </div>
            ))}
          </div>
        </RadioGroup>
      </DialogContent>
    </Dialog>
  )
}

export function SortSelector({ type, sortBy, sortOrder, setSortBy, setSortOrder } : SortSelectorProps) {

  const [open, setOpen] = useState(false)

  return (
    <>
      <SortSelectorButton 
        setOpen={setOpen}
      />
      <SortSelectorPanel 
        type={type}
        open={open}
        sortBy={sortBy}
        sortOrder={sortOrder}
        setOpen={setOpen}
        setSortBy={setSortBy}
        setSortOrder={setSortOrder}
      />
    </>
  )
}