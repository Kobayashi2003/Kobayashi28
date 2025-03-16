import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Trash, X } from "lucide-react";

interface DelectModeButtonProps {
	deleteMode: boolean
	setDeleteMode: (deleteMode: boolean) => void
	className?: string
}

export function DelectModeButton({ deleteMode, setDeleteMode, className }: DelectModeButtonProps) {
	return (
		<Button
			key={`delect-mode-button`}
			size="icon"
			variant="outline"
			onClick={() => setDeleteMode(!deleteMode)}
			className={cn(
				"bg-[#0F2942]/80 hover:bg-[#0F2942] select-none",
				"text-base md:text-lg font-bold transition-all duration-300",
				deleteMode ? 
					"text-red-400 hover:text-red-500 border-red-400/40 hover:border-red-400/60" : 
					"text-white hover:text-red-400 border-white/10 hover:border-white/20",
				className
			)}
		>
			{deleteMode ? <X className="w-4 h-4" /> : <Trash className="w-4 h-4" />}
		</Button>	
	)
}