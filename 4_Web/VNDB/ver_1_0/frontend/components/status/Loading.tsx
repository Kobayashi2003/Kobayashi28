import { cn } from "@/lib/utils"
import { Loader2 } from "lucide-react"

interface LoadingProps {
  message?: string
  className?: string
}

export function Loading({ message = "Loading...", className }: LoadingProps) {

  const containerStyle = "flex flex-col justify-center items-center gap-4"
  const iconContainerStyle = "p-4 bg-primary-500/20 rounded-full"
  const iconStyle = "w-12 h-12 animate-spin text-primary-400"
  const textContainerStyle = "text-center"
  const messageStyle = "text-lg font-bold text-gray-200"
  const subMessageStyle = "text-sm font-medium text-gray-400"

  return (
    <div className={cn(containerStyle, className)}>
      <div className={cn(iconContainerStyle)}>
        <Loader2 className={cn(iconStyle)} />
      </div>
      <div className={cn(textContainerStyle)}>
        <h3 className={cn(messageStyle)}>{message}</h3>
        <p className={cn(subMessageStyle)}>Please wait a moment</p>
      </div>
    </div>
  )
}