import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface GhostButtonProps {
  className?: string
}

export function GhostButton({ className }: GhostButtonProps) {
  return <Button variant="ghost" size="icon" className={cn("bg-[#0F2942] border-white/10 animate-pulse", className)} />
}
