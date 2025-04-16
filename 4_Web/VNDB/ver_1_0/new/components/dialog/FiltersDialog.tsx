"use client"

import { useState, useEffect, useMemo } from "react"

import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"

import { ENUMS } from "@/lib/enums"

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
  comparable?: boolean
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
  // YYYY-MM-DD format
  // Year: 1900-2099
  // Month: 01-12
  // Day: 01-31 (simplified, not checking specific month's max days)
  'yyyy-mm-dd': /^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,

  // YYYY-MM format
  // Year: 1900-2099
  // Month: 01-12
  'yyyy-mm': /^(19|20)\d{2}-(0[1-9]|1[0-2])$/,

  // YYYY format
  // Year: 1900-2099
  'yyyy': /^(19|20)\d{2}$/,

  // MM-DD format
  // Month: 01-12
  // Day: 01-31 (simplified, not checking specific month's max days)
  'mm-dd': /^(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,

  // MM format
  // Month: 01-12
  'mm': /^(0[1-9]|1[0-2])$/,
}

const OPERATORS = ["=", "<", ">", "<=", ">=", "!="]

const isValidNumberInput = (input: string, integer?: boolean): boolean =>
  input === "" ? true : integer ? /^\d+$/.test(input) : /^\d*\.?\d+$/.test(input)

const isValidDateInput = (input: string): boolean =>
  input === "" ? true : /^[\d-]*$/.test(input)

const isValidNumber = (input: string, comparable?: boolean, integer?: boolean): boolean => {
  if (comparable) {
    return integer ?
      /^(=|<|>|<=|>=|!=)?\d+$/.test(input.replace(/\s/g, '')) :
      /^(=|<|>|<=|>=|!=)?\d*\.?\d+$/.test(input.replace(/\s/g, ''))
  }
  return integer ?
    /^\d+$/.test(input.replace(/\s/g, '')) :
    /^\d*\.?\d+$/.test(input.replace(/\s/g, ''))
}

const isValidDate = (input: string, format: string, comparable?: boolean): boolean => {

  if (comparable) {
    const operatorMatch = input.replace(/\s/g, '').match(/^(=|<|>|<=|>=|!=)(.*)$/);
    if (!operatorMatch) {
      return isValidDate(input, format, false)
    }
    const [, operator, dateValue] = operatorMatch;
    if (!dateValue.trim()) {
      return false
    }
    return isValidDate(dateValue.trim(), format, false);
  }

  const nextYear = new Date().getFullYear() + 1

  if (format.toLowerCase() === 'yyyy-mm-dd') {
    if (!DATE_FORMAT_REGEX['yyyy-mm-dd'].test(input)) {
      return false
    }
    const [year, month, day] = input.replace(/\s/g, '').split('-').map(Number)
    if (year < 1900 || year > nextYear || month < 1 || month > 12 || day < 1 || day > 31) {
      return false
    }
    const lastDayOfMonth = new Date(year, month, 0).getDate()
    if (day > lastDayOfMonth) {
      return false
    }
    return true
  }

  if (format.toLowerCase() === 'yyyy-mm') {
    if (!DATE_FORMAT_REGEX['yyyy-mm'].test(input)) {
      return false
    }
    const [year, month] = input.replace(/\s/g, '').split('-').map(Number)
    if (year < 1900 || year > nextYear || month < 1 || month > 12) {
      return false
    }
    return true
  }

  if (format.toLowerCase() === 'yyyy') {
    if (!DATE_FORMAT_REGEX['yyyy'].test(input)) {
      return false
    }
    const year = Number(input.replace(/\s/g, ''))
    if (year < 1900 || year > nextYear) {
      return false
    }
    return true
  }

  if (format.toLowerCase() === 'mm-dd') {
    if (!DATE_FORMAT_REGEX['mm-dd'].test(input)) {
      return false
    }
    const [month, day] = input.replace(/\s/g, '').split('-').map(Number)
    if (month < 1 || month > 12 || day < 1 || day > 31) {
      return false
    }
    const lastDayOfMonth = new Date(2000, month, 0).getDate()
    if (day > lastDayOfMonth) {
      return false
    }
    return true
  }

  if (format.toLowerCase() === 'mm') {
    if (!DATE_FORMAT_REGEX['mm'].test(input)) {
      return false
    }
    const month = Number(input.replace(/\s/g, ''))
    if (month < 1 || month > 12) {
      return false
    }
    return true
  }

  return false
}

const isValidSelect = (value: string, comparable?: boolean): boolean => {
  if (comparable) {
    const operatorMatch = value.match(/^(=|<|>|<=|>=|!=)(.*)$/)
    if (!operatorMatch) {
      return isValidSelect(value, false)
    }
    const [, operator, selectValue] = operatorMatch
    if (!selectValue.trim()) {
      return false
    }
    return isValidSelect(selectValue.trim(), false)
  }
  return value.toLowerCase() !== "any"
}

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
        className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50 selection:bg-blue-500 selection:text-white selection:bg-blue-500 selection:text-white"
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
        className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50 selection:bg-blue-500 selection:text-white"
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
          className="bg-[#0A1929] border-white/10 hover:border-white/20 text-white placeholder:text-white/50 selection:bg-blue-500 selection:text-white"
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

function SelectFilterComparable({ filter, value, onChange }: {
  filter: SelectField,
  value: { operator: string, value: string },
  onChange: (field: string, value: { operator: string, value: string }) => void
}) {
  return (
    <div className="flex flex-col gap-2">
      <Label
        htmlFor={`select-filter-${filter.value}`}
        className="text-white/80 font-bold text-sm md:text-base"
      >
        {filter.label}
      </Label>
      <div className="flex flex-row gap-2">
        <Select
          value={value.operator}
          onValueChange={(v) => onChange(filter.value, { operator: v, value: value.value })}
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
        <Select
          value={value.value}
          onValueChange={(v) => onChange(filter.value, { operator: value.operator, value: v })}
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
    </div>
  )
}

function DateFilter({ filter, value, onChange }: {
  filter: DateField,
  value: string,
  onChange: (field: string, value: string) => void
}) {

  const isCurrentInputValid = value === "" || filter.avaliableFormats.some(format =>
    isValidDate(value, format, false)
  )

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
        className={cn(
          "text-white placeholder:text-white/50",
          "selection:bg-blue-500 selection:text-white",
          isCurrentInputValid ? "bg-[#0A1929]" : "bg-red-500/10",
          isCurrentInputValid ? "border-white/10" : "border-red-500",
          isCurrentInputValid ? "hover:border-white/20" : "hover:border-red-500",
          "transition-all duration-300"
        )}
      />
    </div>
  )
}

function DateFilterComparable({ filter, value, onChange }: {
  filter: DateField,
  value: { operator: string, date: string },
  onChange: (field: string, value: { operator: string, date: string }) => void
}) {

  const isCurrentInputValid = value.date === "" || filter.avaliableFormats.some(format =>
    isValidDate(value.date, format, true)
  )

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
          className={cn(
            "text-white placeholder:text-white/50",
            "selection:bg-blue-500 selection:text-white",
            isCurrentInputValid ? "bg-[#0A1929]" : "bg-red-500/10",
            isCurrentInputValid ? "border-white/10" : "border-red-500",
            isCurrentInputValid ? "hover:border-white/20" : "hover:border-red-500",
            "transition-all duration-300"
          )}
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
  v: {
    text: [
      { value: "tag", label: "Tag" },
      { value: "dtag", label: "Directed Tag" },
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
          ...Object.entries(ENUMS.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "olang", label: "Original Language", default: "ja",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "platform", label: "Platform", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.PLATFORM).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "length", label: "Length", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.LENGTH).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "devstatus", label: "Development Status", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.DEVSTATUS).map(([key, value]) => ({
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
  r: {
    text: [
      { value: "engine", label: "Engine" },
      { value: "extlink", label: "External Link" },
      { value: "vn", label: "Visual Novel" },
      { value: "producer", label: "Producer" },
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
          ...Object.entries(ENUMS.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "platform", label: "Platform", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.PLATFORM).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "medium", label: "Medium", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.MEDIUM).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "voiced", label: "Voiced", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.VOICED).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "rtype", label: "Release Type", default: "any",
        options: [
          { value: "any", label: "Any" },
        ]
      },
      {
        value: "patch", label: "Patch", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      },
      {
        value: "freeware", label: "Freeware", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      },
      {
        value: "uncensored", label: "Uncensored", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      },
      {
        value: "official", label: "Official", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      },
      {
        value: "has_ero", label: "Has Ero", default: "any",
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
  c: {
    text: [
      { value: "trait", label: "Trait" },
      { value: "dtrait", label: "Directed Trait" },
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
          ...Object.entries(ENUMS.CHARACTER_ROLE).map(([key, value]) => ({
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
        value: "cup", label: "Cup Size", default: "any", comparable: true,
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
  p: {
    text: [
      { value: "extlink", label: "External Link" },
    ],
    select: [
      {
        value: "lang", label: "Language", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "type", label: "Type", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.TYPE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      }
    ]
  },
  s: {
    text: [
      { value: "extlink", label: "External Link" },
    ],
    select: [
      {
        value: "lang", label: "Language", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.LANGUAGE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "gender", label: "Gender", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "m", label: "Male" },
          { value: "f", label: "Female" },
        ]
      },
      {
        value: "role", label: "Role", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.STAFF_ROLE).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      },
      {
        value: "ismain", label: "Is Main", default: "any",
        options: [
          { value: "any", label: "Any" },
          { value: "1", label: "Yes" },
          { value: "0", label: "No" },
        ]
      }
    ]
  },
  g: {
    select: [
      {
        value: "category", label: "Category", default: "any",
        options: [
          { value: "any", label: "Any" },
          ...Object.entries(ENUMS.CATEGORY).map(([key, value]) => ({
            value: key, label: value
          }))
        ]
      }
    ]
  },
  i: {
  }
}


interface FiltersDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  type: string
  setFilters: (params: Record<string, string>) => void
  className?: string
}

interface FilterState {
  text: Record<string, string>
  number: Record<string, string>
  numberComparable: Record<string, string>
  select: Record<string, string>
  selectComparable: Record<string, string>
  date: Record<string, string>
  dateComparable: Record<string, string>
}

export function FiltersDialog({ open, setOpen, type, setFilters, className }: FiltersDialogProps) {

  const [filtersTemp, setFiltersTemp] = useState<FilterState>({
    text: {},
    number: {},
    numberComparable: {},
    select: {},
    selectComparable: {},
    date: {},
    dateComparable: {}
  })

  const handleFilterChange = {
    text: (field: string, value: string) =>
      setFiltersTemp(prev => ({ ...prev, text: { ...prev.text, [field]: value || "" } })),

    number: (field: string, value: string) =>
      setFiltersTemp(prev => ({ ...prev, number: { ...prev.number, [field]: value || "" } })),

    numberComparable: (field: string, value: { operator: string, number: string }) =>
      setFiltersTemp(prev => ({
        ...prev,
        numberComparable: {
          ...prev.numberComparable,
          [field]: `${value.operator} ${value.number || ""}`
        }
      })),

    select: (field: string, value: string) =>
      setFiltersTemp(prev => ({ ...prev, select: { ...prev.select, [field]: value || "any" } })),

    selectComparable: (field: string, value: { operator: string, value: string }) =>
      setFiltersTemp(prev => ({
        ...prev,
        selectComparable: {
          ...prev.selectComparable,
          [field]: `${value.operator} ${value.value || ""}`
        }
      })),

    date: (field: string, value: string) =>
      setFiltersTemp(prev => ({ ...prev, date: { ...prev.date, [field]: value || "" } })),

    dateComparable: (field: string, value: { operator: string, date: string }) =>
      setFiltersTemp(prev => ({
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
        Object.entries(filtersTemp.text).map(([key, value]) => [key, value.trim()])
      ),
      number: Object.fromEntries(
        Object.entries(filtersTemp.number).map(([key, value]) => [key, value.trim()])
      ),
      numberComparable: Object.fromEntries(
        Object.entries(filtersTemp.numberComparable).map(([key, value]) => [key, value.trim()])
      ),
      select: Object.fromEntries(
        Object.entries(filtersTemp.select).map(([key, value]) => [key, value.trim()])
      ),
      selectComparable: Object.fromEntries(
        Object.entries(filtersTemp.selectComparable).map(([key, value]) => [key, value.trim()])
      ),
      date: Object.fromEntries(
        Object.entries(filtersTemp.date).map(([key, value]) => [key, value.trim()])
      ),
      dateComparable: Object.fromEntries(
        Object.entries(filtersTemp.dateComparable).map(([key, value]) => [key, value.trim()])
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
        const field = searchFilters[type]?.number?.find(f => f.value === key)
        if (!field) return false
        return isValidNumber(value, field.comparable, field.integer)
      })

    // Validate and filter comparable number inputs
    const validNumberFiltersComparable = Object.entries(trimmedFilters.numberComparable)
      .filter(([key, value]) => {
        const field = searchFilters[type]?.number?.find(f => f.value === key)
        if (!field) return false
        return isValidNumber(value, field.comparable, field.integer)
      })

    // Validate and filter select inputs
    const validSelectFilters = Object.entries(trimmedFilters.select)
      .filter(([key, value]) => {
        const field = searchFilters[type]?.select?.find(f => f.value === key)
        if (!field) return false
        return isValidSelect(value, field.comparable)
      })

    // Validate and filter comparable select inputs
    const validSelectFiltersComparable = Object.entries(trimmedFilters.selectComparable)
      .filter(([key, value]) => {
        const field = searchFilters[type]?.select?.find(f => f.value === key)
        if (!field) return false
        return isValidSelect(value, field.comparable)
      })

    // Validate and filter date inputs
    const validDateFilters = Object.entries(trimmedFilters.date)
      .filter(([key, value]) => {
        const field = searchFilters[type]?.date?.find(f => f.value === key)
        const availableFormats = field?.avaliableFormats
        if (!availableFormats) return false
        return availableFormats.some(format =>
          isValidDate(value, format)
        )
      })
      .map(([key, value]) => {
        const field = searchFilters[type]?.date?.find(f => f.value === key)
        return field?.formatter ? [key, field.formatter(value)] : [key, value]
      })

    // Validate and filter comparable date inputs
    const validDateFiltersComparable = Object.entries(trimmedFilters.dateComparable)
      .filter(([key, value]) => {
        const field = searchFilters[type]?.date?.find(f => f.value === key)
        const availableFormats = field?.avaliableFormats
        if (!availableFormats) return false
        return availableFormats.some(format =>
          isValidDate(value, format, true)
        )
      })
      .map(([key, value]) => {
        const field = searchFilters[type]?.date?.find(f => f.value === key)
        return field?.formatter ? [key, field.formatter(value)] : [key, value]
      })


    // Combine all valid filters
    const filteredFilters: Record<string, string> = Object.fromEntries([
      ...validTextFilters,
      ...validNumberFilters,
      ...validNumberFiltersComparable,
      ...validSelectFilters,
      ...validSelectFiltersComparable,
      ...validDateFilters,
      ...validDateFiltersComparable
    ])

    setFilters(filteredFilters)
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
          .filter(f => !f.comparable)
          .map(f => [f.value, f.default || "any"])
      ),
      selectComparable: Object.fromEntries(
        (searchFilters[type]?.select || [])
          .filter(f => f.comparable)
          .map(f => [f.value, "= any"])
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
    setFiltersTemp(initialFilters)
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
          value={filtersTemp.text[filter.value] || ""}
          onChange={handleFilterChange.text}
        />
      ))
    ), [type, filtersTemp.text]),

    number: useMemo(() => (
      searchFilters[type]?.number?.map((filter) => (
        filter.comparable ? (
          <NumberFilterComparable
            key={filter.value}
            filter={filter}
            value={{
              operator: filtersTemp.numberComparable[filter.value]?.split(" ")[0] || "=",
              number: filtersTemp.numberComparable[filter.value]?.split(" ")[1] || ""
            }}
            onChange={handleFilterChange.numberComparable}
          />
        ) : (
          <NumberFilter
            key={filter.value}
            filter={filter}
            value={filtersTemp.number[filter.value] || ""}
            onChange={handleFilterChange.number}
          />
        )
      ))
    ), [type, filtersTemp.number, filtersTemp.numberComparable]),

    select: useMemo(() => (
      searchFilters[type]?.select?.map((filter) => (
        filter.comparable ? (
          <SelectFilterComparable
            key={filter.value}
            filter={filter}
            value={{
              operator: filtersTemp.selectComparable[filter.value]?.split(" ")[0] || "=",
              value: filtersTemp.selectComparable[filter.value]?.split(" ")[1] || ""
            }}
            onChange={handleFilterChange.selectComparable}
          />
        ) : (
          <SelectFilter
            key={filter.value}
            filter={filter}
            value={filtersTemp.select[filter.value] || filter.default || "any"}
            onChange={handleFilterChange.select}
          />
        )
      ))
    ), [type, filtersTemp.select, filtersTemp.selectComparable]),

    date: useMemo(() => (
      searchFilters[type]?.date?.filter(f => !f.comparable).map((filter) => (
        <DateFilter
          key={filter.value}
          filter={filter}
          value={filtersTemp.date[filter.value] || ""}
          onChange={handleFilterChange.date}
        />
      ))
    ), [type, filtersTemp.date]),

    dateComparable: useMemo(() => (
      searchFilters[type]?.date?.filter(f => f.comparable).map((filter) => (
        <DateFilterComparable
          key={filter.value}
          filter={filter}
          value={{
            operator: filtersTemp.dateComparable[filter.value]?.split(" ")[0] || "=",
            date: filtersTemp.dateComparable[filter.value]?.split(" ")[1] || ""
          }}
          onChange={handleFilterChange.dateComparable}
        />
      ))
    ), [type, filtersTemp.dateComparable])
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
            <Button type="button" onClick={handleClearFilters}
              className="flex-1 bg-[#1A3A5A] hover:bg-[#254B75] text-white font-bold transition-all duration-300">
              Clear All Filters
            </Button>
            <Button type="submit"
              className="flex-1 bg-[#1A3A5A] hover:bg-[#254B75] text-white font-bold transition-all duration-300">
              Apply Filters
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
