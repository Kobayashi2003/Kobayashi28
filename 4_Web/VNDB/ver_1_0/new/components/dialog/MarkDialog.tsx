"use client"

import { useState, useEffect } from "react"
import { usePathname } from "next/navigation"

import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

import { InputBar } from "@/components/input/InputBar"
import { AddButton } from "@/components/button/AddButton"

import { useUserContext } from "@/context/UserContext"
import { Category } from "@/lib/types"
import { api } from "@/lib/api"

interface MarkDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  className?: string
}

function MarkDialog({ open, setOpen, className }: MarkDialogProps) {

  const { user } = useUserContext()
  const pathname = usePathname()

  const [loading, setLoading] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [toggledCategoryIds, setToggledCategoryIds] = useState<number[]>([])
  const [newCategoryName, setNewCategoryName] = useState("")

  const fetchCategories = async () => {
  }

  const handleMark = async () => {
  }

  const handleUnMark = async () => {
  }
  
  const handleCreateCategory = async () => {
  }

  const handleDeleteCategory = async () => {
  }
  
  useEffect(() => {
    fetchCategories()
  }, [user, pathname])
  
  return (
    <></>
  )
}
