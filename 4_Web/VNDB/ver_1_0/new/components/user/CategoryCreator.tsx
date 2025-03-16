import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"

interface CategoryCreatorProps {
  loading: boolean
  name: string
  setName: (name: string) => void
  handleCreateCategory: () => void
  className?: string
}

export function CategoryCreator({ loading, name, setName, handleCreateCategory, className }: CategoryCreatorProps) {
  return (
    <form onSubmit={handleCreateCategory} className={cn(
      "bg-[#0F2942]/80 hover:bg-[#0F2942] flex flex-row gap-2 p-4",
      "border border-white/10 hover:border-white/20 rounded-lg",
      "transition-all duration-300",
      className
    )}>
      <Input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="New Category Name"
        className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20 text-white placeholder:text-white/60"
      />
      <Button
        variant="outline"
        size="icon"
        disabled={loading}
        onClick={handleCreateCategory}
        className={cn(
          "bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20",
          "text-white hover:text-white/80 font-bold text-base md:text-lg transition-all duration-300",
          loading && "animate-pulse"
        )}
      >
        <Plus className="w-4 h-4" />
      </Button>
    </form>
  )
}