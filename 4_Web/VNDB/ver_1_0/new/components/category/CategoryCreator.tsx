"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import { InputBar } from "@/components/input/InputBar"
import { AddButton } from "@/components/button/AddButton"

interface CategoryCreatorProps {
  handleCreateCategory: (input: string) => void
  disabled?: boolean
  className?: string
}

export function CategoryCreator({ handleCreateCategory, disabled, className }: CategoryCreatorProps) {

  const [input, setInput] = useState("")

  const containerFlex = "flex flex-row justify-between items-center gap-2"
  const containerBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"
  const containerBorder = "border border-white/10 hover:border-white/20 rounded-lg"
  const containerTransition = "transition-all duration-300"

  return (
    <form onSubmit={(e) => {
      e.preventDefault()
      if (input.trim() === "") return
      handleCreateCategory(input.trim())
      setInput("")
    }} className={cn(
      "p-4",
      containerFlex,
      containerBgColor,
      containerBorder,
      containerTransition,
      className
    )}>
      <InputBar
        input={input}
        setInput={setInput}
        placeholder="New Category Name"
        disabled={disabled}
        className="w-full"
      />
      <AddButton
        handleAdd={() => { 
          if (input.trim() === "") return
          handleCreateCategory(input.trim())
          setInput("")
        }}
        disabled={disabled}
      />
    </form>
  )
}