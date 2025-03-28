"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog"
import { Settings2 } from "lucide-react"

import { FiltersDialog } from "@/components/dialog/FitlersDialog"

interface SearchFiltersProps {
  SearchType: string
  setSearchFilters: (filters: Record<string, string>) => void
}

interface FiltersButtonProps {
  setOpen: (open: boolean) => void
}

interface FiltersDialogProps {
  SearchType: string
  open: boolean
  setOpen: (open: boolean) => void
  setSearchFilters: (filters: Record<string, string>) => void
}

interface FilterField {
  value: string
  label: string
  type: "text" | "number" | "select"
  helpText?: string
  textField?: {
    placeholder?: string
  }
  numberField?: {
    placeholder?: string
  }
  selectField?: {
    default?: string
    options: {
      value: string,
      label: string,
    }[]
  }
}

const filterFields: Record<string, FilterField[]> = {
  vn: [
    {
      value: "developer",
      label: "Developer",
      type: "text",
    },
    {
      value: "lang",
      label: "Language",
      type: "text",
    },
    {
      value: "olang",
      label: "Original Language",
      type: "text",
    },
    {
      value: "platform",
      label: "Platform",
      type: "text",
    }
  ],
  release: [
  ],
  character: [
    {
      value: "cup",
      label: "Cup Size",
      type: "select",
      selectField: {
        default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Array.from({ length: 26 }, (_, i) => ({
            value: String.fromCharCode(65 + i),
            label: String.fromCharCode(65 + i),
          })),
        ],
      },
    },
    {
      value: "sex",
      label: "Sex",
      type: "select",
      selectField: {
        default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "m", label: "Male" },
          { value: "f", label: "Female" },
          { value: "b", label: "Both" },
          { value: "n", label: "Sexless" },
        ],
      },
    }
  ],
  producer: [
  ],
  staff: [
  ],
  tag: [
  ],
  trait: [
  ]
}


function SearchFiltersButton({ setOpen }: FiltersButtonProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20
      text-white hover:text-white/80 text-base md:text-lg font-bold transition-all duration-300"
      onClick={() => setOpen(true)}
    >
      <Settings2 className="h-4 w-4" />
    </Button>
  )
}

function SearchFiltersDialog({ SearchType, open, setOpen, setSearchFilters }: FiltersDialogProps) {
  const [params, setParams] = useState<Record<string, string>>({})

  useEffect(() => {
    const filteredParams: Record<string, string> = Object.fromEntries(
      // TODO: filter out the value "any" maybe is not a good way
      Object.entries(params).filter(([_, value]) => value !== "" && value !== "any")
    )
    setSearchFilters(filteredParams)
  }, [params, setSearchFilters])

  return (
    <FiltersDialog type={SearchType} open={open} setOpen={setOpen} setParams={setSearchFilters} />
  )

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="bg-[#0F2942]/80 border-white/10">
        <DialogHeader>
          <DialogTitle className="text-xl text-white/80">Filters</DialogTitle>
        </DialogHeader>
        <ScrollArea className="h-[50vh] pr-4">
          <div className="flex flex-col gap-2">
            {filterFields[SearchType].map(filter => (
              <div key={`${filter.type}-filter-${filter.value}`} className="flex flex-col justify-start items-start gap-1">
                {filter.type === "text" ? (
                  <>
                    <Label htmlFor={`text-filter-${filter.value}`} className="text-white/80 text-sm md:text-base">
                      {filter.label}
                    </Label>
                    <Input
                      id={`text-filter-${filter.value}`}
                      value={params[filter.value] || ""}
                      onChange={(e) => setParams({ ...params, [filter.value]: e.target.value })}
                      placeholder={filter.textField?.placeholder}
                      className="w-full bg-black/20 border-white/10 hover:border-white/20 text-white placeholder:text-white/60"
                    />
                  </>
                ) : filter.type === "number" ? (
                  <>
                    <Label htmlFor={`number-filter-${filter.value}`} className="text-white/80 text-sm md:text-base">
                      {filter.label}
                    </Label>
                    <Input
                      id={`number-filter-${filter.value}`}
                      value={params[filter.value] || ""}
                      onChange={(e) => setParams({ ...params, [filter.value]: e.target.value })}
                      placeholder={filter.numberField?.placeholder}
                      className="w-full bg-black/20 border-white/10 hover:border-white/20 text-white placeholder:text-white/60"
                    />
                  </>
                ) : filter.type === "select" ? (
                  <>
                    <div className="text-white/80 text-sm md:text-base">{filter.label}</div>
                    <Select
                      value={params[filter.value] || filter.selectField?.default}
                      onValueChange={(value) => setParams({ ...params, [filter.value]: value })}
                    >
                      <SelectTrigger className="w-full bg-black/20 border-white/10 hover:border-white/20 text-white placeholder:text-white/60">
                        <SelectValue placeholder={filter.selectField?.default} />
                      </SelectTrigger>
                      <SelectContent className="bg-[#0F2942]/95 border-white/10 hover:border-white/20 text-white placeholder:text-white/60">
                        {filter.selectField?.options.map((option) => (
                          <SelectItem
                            key={`select-filter-${filter.value}-${option.value}`}
                            value={option.value}
                            className={"text-white/80 hover:border-white/10 data-[state=checked]:bg-white/10"}
                          >
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </>
                ) : null}
              </div>
            ))}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  )
}

export function SearchFilters({ SearchType, setSearchFilters }: SearchFiltersProps) {
  const [open, setOpen] = useState(false)

  return (
    <>
      <SearchFiltersButton setOpen={setOpen} />
      <SearchFiltersDialog SearchType={SearchType} open={open} setOpen={setOpen} setSearchFilters={setSearchFilters} />
    </>
  )
}