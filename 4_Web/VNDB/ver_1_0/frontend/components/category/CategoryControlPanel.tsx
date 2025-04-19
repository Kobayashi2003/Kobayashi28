"use client"

import { cn } from "@/lib/utils";
import { TypeSelector1 } from "@/components/selector/TypeSelector1";
import { TypeSelector2 } from "@/components/selector/TypeSelector2";
import { ReloadButton } from "@/components/button/ReloadButton";
import { DeleteModeButton } from "@/components/button/DeleteModeButton";
import { TogglePanelButton } from "@/components/button/TogglePanelButton";
import { CategorySelector } from "@/components/category/CategorySelector";
import { CategoryCreator } from "@/components/category/CategoryCreator";
import { CategorySearcher } from "@/components/category/CategorySearcher";

interface CategoryOption {
  value: number
  label: string
}

interface CategoryControlPanelProps {
  open: boolean
  type: string
  categoryOptions: CategoryOption[]
  selectedCategoryId: number | undefined
  deleteMode: boolean
  isSearching: boolean
  setOpen: (open: boolean) => void
  setType: (type: string) => void
  setSelectedCategoryId: (id: number | undefined) => void
  setDeleteMode: (deleteMode: boolean) => void
  handleReloadCategories: () => void
  handleDeleteCategory: (categoryId: number) => void
  handleCreateCategory: (newCategoryName: string) => void
  handleSearch: (query: string) => void
  disabled?: boolean
  className?: string
}

export function CategoryControlPanel({ open, type, categoryOptions, selectedCategoryId, deleteMode, isSearching, setOpen, setType, setSelectedCategoryId, setDeleteMode, handleDeleteCategory, handleCreateCategory, handleSearch, handleReloadCategories, disabled, className }: CategoryControlPanelProps) {
  return (
    <div className={cn(
      "w-full md:w-100 lg:w-120 xl:w-140",
      "flex flex-col gap-2",
      "transition-all duration-300",
      !open && "scale-0 absolute origin-top-left",
      className
    )}>
      <div className={"flex flex-row justify-between gap-2"}>
        <div className="flex flex-row justify-center gap-2">
          <TogglePanelButton
            open={open}
            setOpen={setOpen}
            direction="left"
            disabled={disabled}
          />
          <DeleteModeButton
            deleteMode={deleteMode}
            setDeleteMode={setDeleteMode}
            disabled={disabled}
          />
          <ReloadButton
            handleReload={handleReloadCategories}
            disabled={disabled}
          />
        </div>
        <TypeSelector1
          selected={type}
          onSelect={setType}
          disabled={disabled}
          className="sm:hidden"
        />
        <TypeSelector2
          selected={type}
          onSelect={setType}
          disabled={disabled}
          className="max-sm:hidden"
        />
      </div>
      <div className="flex flex-col justify-center gap-2">
        <CategorySelector
          categoryOptions={categoryOptions}
          selectedValue={selectedCategoryId}
          setSelectedValue={setSelectedCategoryId}
          deleteMode={deleteMode}
          handleDelete={handleDeleteCategory}
          disabled={disabled}
          className="w-full"
        />
        <CategoryCreator
          handleCreateCategory={handleCreateCategory}
          disabled={disabled}
          className="w-full"
        />
        <CategorySearcher
          isSearching={isSearching}
          handleSearch={handleSearch}
          disabled={disabled}
          className={cn(
            "w-full",
            !selectedCategoryId && "opacity-0"
          )}
        />
      </div>
    </div>
  )
}
