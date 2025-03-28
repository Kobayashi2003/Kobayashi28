"use client"

import { useState, useEffect, useMemo } from "react"

import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"

import { FULL_FORM } from "@/lib/fullForm"

interface BaseField {
  value: string
  label: string
  disabled?: boolean
}

interface TextField extends BaseField {
  allowEmpty?: boolean
  placeholder?: string
}

interface NumberField extends BaseField {
  integer?: boolean
  comparable?: boolean
  placeholder?: string
}

interface SelectField extends BaseField {
  default?: string
  options: {
    value: string
    label: string
  }[]
}

interface DateField extends BaseField {
  avaliableFormats: string[]
  comparable?: boolean
  placeholder?: string
  formatter?: (value: string) => any
}


const DATE_FORMAT_REGEX: Record<string, RegExp> = {
  'yyyy-mm-dd': /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$/,
  'yyyy-mm': /^\d{4}-(0[1-9]|1[0-2])$/,
  'yyyy': /^\d{4}$/,
  'mm-dd': /^(0[1-9]|1[0-2])-(0[1-9]|[12][0-2]|3[01])$/,
  'mm': /^(0[1-9]|1[0-2])$/
}

const OPERATORS = ["=", "<", ">", "<=", ">="]

const isValidNumberInput = (input: string, integer?: boolean): boolean =>
  input === "" ? true : integer ? /^\d+$/.test(input) : /^\d*\.?\d+$/.test(input)

const isValidDateInput = (input: string): boolean =>
  input === "" ? true : /[\d-]*/.test(input)


function TextFilter({ filter, value, onChange }: { 
  filter: TextField, 
  value: string, 
  onChange: (field: string, value: string) => void 
}) {
  return (
    <div className="flex flex-col gap-2">
      <Label
        htmlFor={`text-filter-${filter.value}`}
        className="text-white/80 font-bold text-sm md:text-base"
      >
        {filter.label}
      </Label>
      <Input
        id={`text-filter-${filter.value}`}
        value={value}
        onChange={(e) => onChange(filter.value, e.target.value)}
        placeholder={filter.placeholder}
        className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50"
      />
    </div>
  )
}

function NumberFilter({ filter, value, onChange }: { 
  filter: NumberField, 
  value: string, 
  onChange: (field: string, value: string) => void 
}) {
  return (
    <div className="flex flex-col gap-2">
      <Label
        htmlFor={`number-filter-${filter.value}`}
        className="text-white/80 font-bold text-sm md:text-base"
      >
        {filter.label}
      </Label>
      <Input
        id={`number-filter-${filter.value}`}
        value={value}
        onChange={(e) => {
          if (isValidNumberInput(e.target.value, filter.integer)) {
            onChange(filter.value, e.target.value)
          }
        }}
        placeholder={filter.placeholder}
        className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50"
      />
    </div>
  )
}

function NumberFilterComparable({ filter, value, onChange }: { 
  filter: NumberField, 
  value: { operator: string, number: string }, 
  onChange: (field: string, value: { operator: string, number: string }) => void 
}) {
  return (
    <div className="flex flex-col gap-2">
      <Label
        htmlFor={`number-filter-${filter.value}`}
        className="text-white/80 font-bold text-sm md:text-base"
      >
        {filter.label}
      </Label>
      <div className="flex flex-row gap-2">
        <Select
          value={value.operator}
          onValueChange={(v) => onChange(filter.value, { operator: v, number: value.number })}
        >
          <SelectTrigger className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white">
            <SelectValue placeholder="Operator" />
          </SelectTrigger>
          <SelectContent className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white">
            {OPERATORS.map((operator) => (
              <SelectItem
                key={`select-number-filter-${filter.value}-${operator}`}
                value={operator}
                className="text-white/80 data-[state=checked]:bg-white/10"
              >
                <span className="w-5 inline-block text-center">{operator}</span>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Input
          id={`number-filter-${filter.value}`}
          value={value.number}
          onChange={(e) => {
            if (isValidNumberInput(e.target.value, filter.integer)) {
              onChange(filter.value, { operator: value.operator, number: e.target.value })
            }
          }}
          placeholder={filter.placeholder}
          className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50"
        />
      </div>
    </div>
  )
}

function SelectFilter({ filter, value, onChange }: { 
  filter: SelectField, 
  value: string, 
  onChange: (field: string, value: string) => void 
}) {
  return (
    <div className="flex flex-col gap-2">
      <Label
        htmlFor={`select-filter-${filter.value}`}
        className="text-white/80 font-bold text-sm md:text-base"
      >
        {filter.label}
      </Label>
      <Select
        value={value}
        defaultValue={filter.default}
        onValueChange={(value) => onChange(filter.value, value)}
      >
        <SelectTrigger
          id={`select-filter-${filter.value}`}
          className="w-full bg-[#0A1929] border-white/10 hover:border-white/20 text-white"
        >
          <SelectValue placeholder={filter.default} />
        </SelectTrigger>
        <SelectContent className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white">
          {filter.options.map((option) => (
            <SelectItem
              key={`select-filter-${filter.value}-${option.value}`}
              value={option.value}
              className="text-white/80 data-[state=checked]:bg-white/10"
            >
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}

function DateFilter({ filter, value, onChange }: { 
  filter: DateField, 
  value: string, 
  onChange: (field: string, value: string) => void 
}) {
  return (
    <div className="flex flex-col gap-2">
      <Label 
        htmlFor={`date-filter-${filter.value}`} 
        className="text-white/80 font-bold text-sm md:text-base"
      >
        {filter.label}
      </Label>
      <Input
        id={`date-filter-${filter.value}`}
        value={value}
        onChange={(e) => {
          if (isValidDateInput(e.target.value)) {
            onChange(filter.value, e.target.value)
          }
        }}
        placeholder={filter.placeholder}
        className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50"
      />
    </div>
  )
}

function DateFilterComparable({ filter, value, onChange }: { 
  filter: DateField, 
  value: { operator: string, date: string }, 
  onChange: (field: string, value: { operator: string, date: string }) => void 
}) {
  return (
    <div className="flex flex-col gap-2">
      <Label
        htmlFor={`date-filter-${filter.value}`}
        className="text-white/80 font-bold text-sm md:text-base"
      >
        {filter.label}
      </Label>
      <div className="flex flex-row gap-2">
        <Select
          value={value.operator}
          onValueChange={(v) => onChange(filter.value, { operator: v, date: value.date })}
        >
          <SelectTrigger className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white">
            <SelectValue placeholder="Operator" />
          </SelectTrigger>
          <SelectContent className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white">
            {OPERATORS.map((operator) => (
              <SelectItem
                key={`select-date-filter-${filter.value}-${operator}`}
                value={operator}
                className="text-white/80 data-[state=checked]:bg-white/10"
              >
                <span className="w-5 inline-block text-center">{operator}</span>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Input
          id={`date-filter-${filter.value}`}
          value={value.date}
          onChange={(e) => {
            if (isValidDateInput(e.target.value)) {
              onChange(filter.value, { operator: value.operator, date: e.target.value })
            }
          }}
          placeholder={filter.placeholder}
          className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50"
        />
      </div>
    </div>
  )
}

const searchFilters: Record<string, {
  text?: TextField[]
  number?: NumberField[]
  select?: SelectField[]
  date?: DateField[]
}> = {
  vn: {
    text: [
      { value: "tag", label: "Tag" },
      { value: "release", label: "Release" },
      { value: "character", label: "Character" },
      { value: "staff", label: "Staff" },
      { value: "developer", label: "Developer" },
    ],
    number: [
      {
        value: "rating", label: "Rating", integer: true, comparable: true,
        placeholder: "Bayesian Rating, integer between 10 and 100."
      },
      {
        value: "votecount", label: "Vote Count", integer: true, comparable: true,
        placeholder: "Integer, number of votes."
      },
    ],
    select: [
      {
        value: "lang", label: "Language", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "olang", label: "Original Language", default: "ja",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "platform", label: "Platform", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.PLATFORM).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "length", label: "Length", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.LENGTH).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "devstatus", label: "Development Status", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.DEVSTATUS).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "has_description", label: "Has Description", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      },
      {
        value: "has_anime", label: "Has Anime", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      },
      {
        value: "has_screenshot", label: "Has Screenshot", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      },
      {
        value: "has_review", label: "Has Review", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      }
    ],
    date: [
      {
        value: "released", label: "Release Date", avaliableFormats: ["YYYY-MM-DD", "YYYY-MM", "YYYY"],
        comparable: true, placeholder: "Date, format: YYYY-MM-DD, YYYY-MM, YYYY."
      },
    ]
  },
  release: {
    text: [
    ],
    number: [
      {
        value: "minage", label: "Minimum Age", integer: true, comparable: true,
        placeholder: "Integer, minimum age."
      },
    ],
    select: [
      {
        value: "lang", label: "Language", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "platform", label: "Platform", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.PLATFORM).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      }
    ],
    date: [
      {
        value: "released", label: "Release Date", avaliableFormats: ["YYYY-MM-DD", "YYYY-MM", "YYYY"],
        comparable: true, placeholder: "Date, format: YYYY-MM-DD, YYYY-MM, YYYY."
      },
    ]
  },
  character: {
    text: [
      { value: "seiyuu", label: "Seiyuu" },
      { value: "vn", label: "Visual Novel" },
    ],
    number: [
      {
        value: "height", label: "Height", integer: true, comparable: true,
        placeholder: "Integer, height in cm."
      },
      {
        value: "weight", label: "Weight", integer: true, comparable: true,
        placeholder: "Integer, weight in kg."
      },
      {
        value: "bust", label: "Bust", integer: true, comparable: true,
        placeholder: "Integer, bust size in cm."
      },
      {
        value: "waist", label: "Waist", integer: true, comparable: true,
        placeholder: "Integer, waist size in cm."
      },
      {
        value: "hips", label: "Hips", integer: true, comparable: true,
        placeholder: "Integer, hips size in cm."
      },
      {
        value: "age", label: "Age", integer: true, comparable: true,
        placeholder: "Integer, age in years."
      },
    ],
    select: [
      {
        value: "role", label: "Role", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.CHARACTER_ROLE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "bloodtype", label: "Blood Type", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "a", label: "A" },
          { value: "b", label: "B" },
          { value: "ab", label: "AB" },
          { value: "o", label: "O" },
        ]
      },
      {
        value: "sex", label: "Sex", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "m", label: "Male" },
          { value: "f", label: "Female" },
          { value: "b", label: "Both" },
          { value: "n", label: "Sexless" },
        ]
      },
      {
        value: "sex_spoil", label: "Sex Spoil", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "m", label: "Male" },
          { value: "f", label: "Female" },
          { value: "b", label: "Both" },
          { value: "n", label: "Sexless" },
        ]
      },
      {
        value: "cup", label: "Cup Size", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "AAA", label: "AAA" },
          { value: "AA", label: "AA" },
          ...Array.from({ length: 26 }, (_, i) => ({
            value: String.fromCharCode(65 + i),
            label: String.fromCharCode(65 + i),
          })),
        ]
      },
    ],
    date: [
      {
        value: "birthday", label: "Birthday", avaliableFormats: ["MM-DD", "MM"],
        placeholder: "Date, format: MM-DD, MM.",
      },
    ]
  },
  producer: {
    text: [
      { value: "extlink", label: "External Link" },
    ],
    number: [
    ],
    select: [
      {
        value: "lang", label: "Language", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "type", label: "Type", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.PRODUCER_TYPE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      }
    ]
  },
  staff: {
    text: [

    ],
    number: [

    ],
    select: [

    ]
  },
  tag: {
    text: [
    ],
    number: [
    ],
    select: [
      {
        value: "category", label: "Category", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(FULL_FORM.TAG_CATEGORY).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      }
    ]
  },
  trait: {
    text: [
    ],
    number: [
    ],
    select: [
    ]
  }
}


interface FiltersDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  type: string
  setParams: (params: Record<string, string>) => void
  className?: string
}

interface FilterState {
  text: Record<string, string>
  number: Record<string, string>
  numberComparable: Record<string, string>
  select: Record<string, string>
  date: Record<string, string>
  dateComparable: Record<string, string>
}

export function FiltersDialog({ open, setOpen, type, setParams, className }: FiltersDialogProps) {

  const [filters, setFilters] = useState<FilterState>({
    text: {},
    number: {},
    numberComparable: {},
    select: {},
    date: {},
    dateComparable: {}
  })

  const handleFilterChange = {
    text: (field: string, value: string) => 
      setFilters(prev => ({ ...prev, text: { ...prev.text, [field]: value || "" } })),
    
    number: (field: string, value: string) => 
      setFilters(prev => ({ ...prev, number: { ...prev.number, [field]: value || "" } })),
    
    numberComparable: (field: string, value: { operator: string, number: string }) => 
      setFilters(prev => ({ 
        ...prev, 
        numberComparable: { 
          ...prev.numberComparable, 
          [field]: `${value.operator} ${value.number || ""}` 
        } 
      })),
    
    select: (field: string, value: string) => 
      setFilters(prev => ({ ...prev, select: { ...prev.select, [field]: value || "any" } })),
    
    date: (field: string, value: string) => 
      setFilters(prev => ({ ...prev, date: { ...prev.date, [field]: value || "" } })),
    
    dateComparable: (field: string, value: { operator: string, date: string }) => 
      setFilters(prev => ({ 
        ...prev, 
        dateComparable: { 
          ...prev.dateComparable, 
          [field]: `${value.operator} ${value.date || ""}` 
        } 
      }))
  }

  const handleApplyFilters = () => {
    const trimmedFilters = {
      text: Object.fromEntries(
        Object.entries(filters.text).map(([key, value]) => [key, value.trim()])
      ),
      number: Object.fromEntries(
        Object.entries(filters.number).map(([key, value]) => [key, value.trim()])
      ),
      numberComparable: Object.fromEntries(
        Object.entries(filters.numberComparable).map(([key, value]) => [key, value.trim()])
      ),
      select: Object.fromEntries(
        Object.entries(filters.select).map(([key, value]) => [key, value.trim()])
      ),
      date: Object.fromEntries(
        Object.entries(filters.date).map(([key, value]) => [key, value.trim()])
      ),
      dateComparable: Object.fromEntries(
        Object.entries(filters.dateComparable).map(([key, value]) => [key, value.trim()])
      )
    }

    // Validate and filter text inputs
    const validTextFilters = Object.entries(trimmedFilters.text)
      .filter(([key, value]) => {
        if (value === "") return false
        const field = searchFilters[type]?.text?.find(f => f.value === key)
        return field?.allowEmpty ? true : value !== ""
      })

    // Validate and filter number inputs
    const validNumberFilters = Object.entries(trimmedFilters.number)
      .filter(([key, value]) => {
        if (value === "") return false
        const field = searchFilters[type]?.number?.find(f => f.value === key)
        return field?.integer 
          ? /^\d+$/.test(value)
          : /^\d*\.?\d+$/.test(value)
      })

    // Validate and filter comparable number inputs
    const validNumberFiltersComparable = Object.entries(trimmedFilters.numberComparable)
      .filter(([key, value]) => {
        const parts = value.split(" ")
        if (parts.length !== 2) return false
        const [operator, number] = parts
        if (!OPERATORS.includes(operator) || number === "") return false
        
        const field = searchFilters[type]?.number?.find(f => f.value === key)
        return field?.integer 
          ? /^\d+$/.test(number)
          : /^\d*\.?\d+$/.test(number)
      })

    // Validate and filter select inputs
    const validSelectFilters = Object.entries(trimmedFilters.select)
      .filter(([key, value]) => {
        return value !== "any"
      })

    // Validate and filter date inputs
    const validDateFilters = Object.entries(trimmedFilters.date)
      .filter(([key, value]) => {
        if (value === "") return false
        const field = searchFilters[type]?.date?.find(f => f.value === key)
        const availableFormats = field?.avaliableFormats
        if (!availableFormats) return false

        return availableFormats.some(format => 
          DATE_FORMAT_REGEX[format.toLowerCase()].test(value)
        )
      })
      .map(([key, value]) => {
        const field = searchFilters[type]?.date?.find(f => f.value === key)
        return field?.formatter ? [key, field.formatter(value)] : [key, value]
      })

    // Validate and filter comparable date inputs
    const validDateFiltersComparable = Object.entries(trimmedFilters.dateComparable)
      .filter(([key, value]) => {
        const parts = value.split(" ")
        if (parts.length !== 2) return false
        const [operator, date] = parts
        if (!OPERATORS.includes(operator) || date === "") return false

        const field = searchFilters[type]?.date?.find(f => f.value === key)
        const availableFormats = field?.avaliableFormats
        if (!availableFormats) return false

        return availableFormats.some(format => 
          DATE_FORMAT_REGEX[format.toLowerCase()].test(date)
        )
      })

    // Combine all valid filters
    const filteredParams: Record<string, string> = Object.fromEntries([
      ...validTextFilters,
      ...validNumberFilters,
      ...validNumberFiltersComparable,
      ...validSelectFilters,
      ...validDateFilters,
      ...validDateFiltersComparable
    ])

    setParams(filteredParams)
    setOpen(false)
  }

  // Reset all filters to initial state
  const handleClearFilters = () => {
    const initialFilters: FilterState = {
      text: Object.fromEntries(
        (searchFilters[type]?.text || []).map(f => [f.value, ""])
      ),
      number: Object.fromEntries(
        (searchFilters[type]?.number || [])
          .filter(f => !f.comparable)
          .map(f => [f.value, ""])
      ),
      numberComparable: Object.fromEntries(
        (searchFilters[type]?.number || [])
          .filter(f => f.comparable)
          .map(f => [f.value, "= "])
      ),
      select: Object.fromEntries(
        (searchFilters[type]?.select || [])
          .map(f => [f.value, f.default || "any"])
      ),
      date: Object.fromEntries(
        (searchFilters[type]?.date || [])
          .filter(f => !f.comparable)
          .map(f => [f.value, ""])
      ),
      dateComparable: Object.fromEntries(
        (searchFilters[type]?.date || [])
          .filter(f => f.comparable)
          .map(f => [f.value, "= "])
      )
    }
    setFilters(initialFilters)
  }

  useEffect(() => {
    handleClearFilters()
  }, [type]);

  // Memoized filter elements
  const filterElements = {
    text: useMemo(() => (
      searchFilters[type]?.text?.map((filter) => (
        <TextFilter 
          key={filter.value} 
          filter={filter}
          value={filters.text[filter.value] || ""} 
          onChange={handleFilterChange.text} 
        />
      ))
    ), [type, filters.text]),

    number: useMemo(() => (
      searchFilters[type]?.number?.map((filter) => (
        filter.comparable ? (
          <NumberFilterComparable 
            key={filter.value} 
            filter={filter}
            value={{
              operator: filters.numberComparable[filter.value]?.split(" ")[0] || "=",
              number: filters.numberComparable[filter.value]?.split(" ")[1] || ""
            }}
            onChange={handleFilterChange.numberComparable} 
          />
        ) : (
          <NumberFilter 
            key={filter.value} 
            filter={filter}
            value={filters.number[filter.value] || ""} 
            onChange={handleFilterChange.number} 
          />
        )
      ))
    ), [type, filters.number, filters.numberComparable]),

    select: useMemo(() => (
      searchFilters[type]?.select?.map((filter) => (
        <SelectFilter 
          key={filter.value} 
          filter={filter}
          value={filters.select[filter.value] || filter.default || "any"} 
          onChange={handleFilterChange.select} 
        />
      ))
    ), [type, filters.select]),

    date: useMemo(() => (
      searchFilters[type]?.date?.filter(f => !f.comparable).map((filter) => (
        <DateFilter 
          key={filter.value} 
          filter={filter}
          value={filters.date[filter.value] || ""} 
          onChange={handleFilterChange.date} 
        />
      ))
    ), [type, filters.date]),

    dateComparable: useMemo(() => (
      searchFilters[type]?.date?.filter(f => f.comparable).map((filter) => (
        <DateFilterComparable 
          key={filter.value} 
          filter={filter}
          value={{
            operator: filters.dateComparable[filter.value]?.split(" ")[0] || "=",
            date: filters.dateComparable[filter.value]?.split(" ")[1] || ""
          }}
          onChange={handleFilterChange.dateComparable} 
        />
      ))
    ), [type, filters.dateComparable])
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
          <DialogTitle className="text-xl text-white">Search Filters</DialogTitle>
        </DialogHeader>
        <form onSubmit={(e: React.FormEvent) => {
          e.preventDefault()
          handleApplyFilters()
        }}>
          <ScrollArea className="h-[50vh] border-t border-b border-white/10">
            <div className="flex flex-col gap-2">
              {Object.values(filterElements).map((element, index) => (
                <div key={index}>{element}</div>
              ))}
            </div>
          </ScrollArea>
          <div className="flex flex-row gap-2">
            <Button type="button" onClick={handleClearFilters} className="flex-1 bg-[#1A3A5A] hover:bg-[#254B75] text-white font-bold transition-all duration-300">
              Clear All Filters
            </Button>
            <Button type="submit" className="flex-1 bg-[#1A3A5A] hover:bg-[#254B75] text-white font-bold transition-all duration-300">
              Apply Filters
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
