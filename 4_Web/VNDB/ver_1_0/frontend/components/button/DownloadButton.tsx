import { cn } from "@/lib/utils";
import { IconButton } from "@/components/button/IconButton";
import { Download } from "lucide-react";

interface DownloadButtonProps {
  handleDownload: () => void
  disabled?: boolean
  className?: string
}

export function DownloadButton({ handleDownload, disabled, className }: DownloadButtonProps) {

  const buttonBgColor = "bg-[#0F2942]/80 hover:bg-[#0F2942]"

  return (
    <IconButton
      icon={<Download className="w-4 h-4 group-hover:animate-bounce" />}
      variant="outline"
      onClick={handleDownload}
      disabled={disabled}
      className={cn("group", buttonBgColor, className)}
    />
  )
}