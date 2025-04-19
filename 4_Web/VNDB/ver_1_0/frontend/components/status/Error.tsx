import { cn } from "@/lib/utils";
import { AlertTriangle } from "lucide-react";

interface ErrorProps {
  message?: string;
  className?: string;
}

export function Error({ message = "Something went wrong", className }: ErrorProps) {

  const containerStyle = "flex flex-col justify-center items-center gap-4"
  const iconContainerStyle = "p-4 bg-red-500/20 rounded-full"
  const iconStyle = "w-12 h-12 text-red-400"
  const textContainerStyle = "text-center"
  const messageStyle = "text-lg font-bold text-red-300"
  const subMessageStyle = "text-sm font-medium text-gray-400"

  return (
    <div className={cn(containerStyle, className)}>
      <div className={cn(iconContainerStyle)}>
        <AlertTriangle className={cn(iconStyle)} />
      </div>
      <div className={cn(textContainerStyle)}>
        <h3 className={cn(messageStyle)}>{message}</h3>
        <p className={cn(subMessageStyle)}>Please try again later or contact support</p>
      </div>
    </div>
  );
}