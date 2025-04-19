"use client"

import { useState, useEffect } from "react"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import type { SearchType } from "@/lib/types"

interface SearchFiltersProps {
  searchType: SearchType
  onChange: (params: Record<string, string>) => void
}

interface FilterField {
  id: string
  label: string
  type: "text" | "number" | "select"
  placeholder?: string
  helpText?: string
  options?: Array<{ value: string; label: string }>
}

const filterOptions: Record<SearchType, FilterField[]> = {
  vn: [
    {
      id: "search",
      label: "Search",
      type: "text",
      placeholder: "",
      helpText: ""
    },
    {
      id: "developer",
      label: "Developer",
      type: "text",
      placeholder: "",
      helpText: ""
    }
  ],
  character: [
    {
      id: "search",
      label: "Search",
      type: "text",
      placeholder: "",
      helpText: ""
    }
  ],
  release: [
    {
      id: "search",
      label: "Search",
      type: "text",
      placeholder: "",
      helpText: ""
    }
  ],
  producer: [
    {
      id: "search",
      label: "Search",
      type: "text",
      placeholder: "",
      helpText: ""
    }
  ],
  staff: [
    {
      id: "search",
      label: "Search",
      type: "text",
      placeholder: "",
      helpText: ""
    }
  ],
  tag: [
    {
      id: "search",
      label: "Search",
      type: "text",
      placeholder: "",
      helpText: ""
    }
  ],
  trait: [
    {
      id: "search",
      label: "Search",
      type: "text",
      placeholder: "",
      helpText: ""
    }
  ]
}

function FilterField({ 
  field, 
  value, 
  onChange 
}: {
  field: FilterField
  value: string,
  onChange: (value: string) => void
}) {
  if (field.type === "select" && field.options) {
    const options = [{ value: "any", label: "Any" }, ...field.options]
    return (
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger className="bg-[#0F2942]/80 border-white/10">
          <SelectValue placeholder={`Select ${field.label.toLowerCase()}`} />
        </SelectTrigger>
        <SelectContent>
          {options.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    )
  }

  return (
    <Input
      id={field.id}
      type={field.type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={field.placeholder}
      className="bg-[#0F2942]/80 border-white/10"
    />
  )
}

export function SearchFilters({ searchType, onChange }: SearchFiltersProps) {
  const [params, setParams] = useState<Record<string, string>>({})
  const fields = filterOptions[searchType]

  useEffect(() => {
    const filteredParams = Object.fromEntries(
      Object.entries(params).filter(([_, value]) => value !== "" && value !== "any"),
    )
    onChange(filteredParams)
  }, [params, onChange])

  const updateParam = (key: string, value: string) => {
    setParams((prev) => ({
      ...prev,
      [key]: value,
    }))
  }

  return (
    <div className="space-y-6">
      {fields.map((field) => (
        <div key={field.id} className="space-y-2">
          <Label htmlFor={field.id}>{field.label}</Label>
          <FilterField
            field={field}
            value={params[field.id] || (field.type === "select" ? "any" : "")}
            onChange={(value) => updateParam(field.id, value)}
          />
          {field.helpText && <p className="text-sm text-white/60">{field.helpText}</p>}
        </div>
      ))}
    </div>
  )
}