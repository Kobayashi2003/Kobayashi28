import { Button } from "@/components/ui/button";
import { ArrowRight, Loader2 } from "lucide-react";

interface SearchSubmitButtonProps {
  isLoading: boolean
  handleSubmit: (e: React.FormEvent) => void
}

export function SearchSubmitButton({ isLoading, handleSubmit }: SearchSubmitButtonProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      className="bg-[#0F2942]/80 hover:bg-[#0F2942] border-white/10 hover:border-white/20
      text-white hover:text-white/80 text-base md:text-lg font-bold transition-all duration-300"
      onClick={handleSubmit}
    >
      {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
    </Button>
  )
}
