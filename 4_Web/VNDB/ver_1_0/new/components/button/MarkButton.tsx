"use client"

import { useState, useEffect } from "react"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Star, StarIcon } from "lucide-react"
import { api } from "@/lib/api"

interface MarkButtonProps {
  onClick: () => void
  disabled?: boolean
  className?: string
}

function analyzePathname(pathname: string) {
  const match = pathname.match(/^\/(v|c|p|s)\/(\d+)/)
  if (match) {
    return { type: match[1], id: Number.parseInt(match[2], 10) }
  }
  return { type: "", id: 0 }
}

export function MarkButton({ onClick, disabled, className }: MarkButtonProps) {

  const pathname = usePathname()
  const { type, id } = analyzePathname(pathname)

  const buttonVisible = (!type || !id) ? "hidden" : ""
  const buttonBgColor = "bg-transparent"
  const buttonTextColor = "text-yellow-400 hover:text-yellow-300"
  const buttonAnimation = "transition-all duration-300"

  const [marked, setMarked] = useState(false)

  useEffect(() => {
    setMarked(false)
    if (type && id) {
      api.mark.isMarked(type, id).then((res) => {
        setMarked(res.isMarked)
      })
    }
  }, [type, id])

  return (
    <Button
      variant="ghost"
      size="icon"
      className={cn(
        "select-none",
        buttonVisible,
        buttonBgColor, 
        buttonTextColor, 
        buttonAnimation, 
        className
      )}
      onClick={onClick}
      disabled={disabled}
    >
      {marked ? <StarIcon className="w-4 h-4 fill-current" /> : <Star className="w-4 h-4" />}
    </Button>
  )
}
