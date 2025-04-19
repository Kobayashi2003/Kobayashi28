import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog"

interface ConfirmDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
  title: string
  description: string
  confirmText: string
  cancelText: string
  onConfirm: () => void
  onCancel: () => void
  className?: string
}

export function ConfirmDialog({ open, setOpen, title, description, confirmText, cancelText, onConfirm, onCancel, className }: ConfirmDialogProps) {
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
          <DialogTitle className="text-white">{title}</DialogTitle>
          <DialogDescription className="text-white/60">{description}</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button 
            variant="outline" 
            onClick={onCancel}
            className="text-white/60 hover:text-white"
          >
            {cancelText}
          </Button>
          <Button 
            variant="outline"
            onClick={onConfirm}
            className="text-white hover:text-white"
          >
            {confirmText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}