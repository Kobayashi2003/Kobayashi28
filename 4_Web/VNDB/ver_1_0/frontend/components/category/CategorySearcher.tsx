"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import { InputBar } from "../input/InputBar"
import { SubmitButton } from "../button/SubmitButton"
import { CancelButton } from "../button/CancelButton"


interface CategorySearcherProps {
  isSearching: boolean
  handleSearch: (input: string) => void
  disabled?: boolean
  className?: string
}

export function CategorySearcher({ isSearching, handleSearch, disabled, className }: CategorySearcherProps) {

  const [input, setInput] = useState("")

  const containerFlex = "flex flex-row justify-between items-center gap-2"
  const containerBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const containerBorder = "border border-white/10 hover:border-white/20 rounded-lg"
  const containerTransition = "transition-all duration-300"

  return (
    <div className={cn(
      "p-4",
      containerFlex,
      containerBgColor,
      containerBorder,
      containerTransition,
      className
    )}>
      <form onSubmit={(e) => {
        e.preventDefault()
        handleSearch(input.trim())
      }} className={cn("w-full")}>
        <InputBar
          input={input}
          setInput={setInput}
          placeholder="Search in current category"
          disabled={disabled}
          className="w-full"
        />
      </form>
      <SubmitButton
        handleSubmit={() => {
          handleSearch(input.trim())
        }}
        disabled={disabled}
      />
      {isSearching && (
        <CancelButton
          handleCancel={() => {
            setInput("")
            handleSearch("")
          }}
          disabled={disabled}
        />
      )}
    </div>
  )
}
