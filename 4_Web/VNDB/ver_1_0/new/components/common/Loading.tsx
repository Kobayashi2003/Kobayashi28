import { Loader2 } from "lucide-react"

interface LoadingProps {
  message?: string
  className?: string
}

export function Loading({ 
  message = "Loading...", 
  className = "" 
}: LoadingProps) {
  return (
    <div className={`flex flex-col items-center justify-center gap-4 ${className}`}>
      <Loader2 
        className="w-12 h-12 animate-spin text-primary-400"
        style={{ animationDuration: "1.2s" }}
      />
      <div className="space-y-2 text-center">
        <h3 className="text-lg font-medium text-gray-100">{message}</h3>
        <p className="text-sm text-gray-400">Please wait a moment</p>
      </div>
    </div>
  )
}