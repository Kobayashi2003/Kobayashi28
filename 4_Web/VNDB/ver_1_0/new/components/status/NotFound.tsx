import { cn } from "@/lib/utils";
import { SearchX } from "lucide-react";

interface NotFoundProps {
  message?: string;
  className?: string;
}

export function NotFound({ message = "No results found", className }: NotFoundProps) {

  const containerStyle = "flex flex-col justify-center items-center gap-4"
  const iconContainerStyle = "p-4 bg-gray-700/20 rounded-full"
  const iconStyle = "w-12 h-12 text-gray-400"
  const textContainerStyle = "text-center"
  const messageStyle = "text-lg font-bold text-gray-200"
  const subMessageStyle = "text-sm font-medium text-gray-400"

  return (
    <div className={cn(containerStyle, className)}>
      <div className={cn(iconContainerStyle)}>
        <SearchX className={cn(iconStyle)} />
      </div>
      <div className={cn(textContainerStyle)}>
        <h3 className={cn(messageStyle)}>{message}</h3>
        <p className={cn(subMessageStyle)}>Try adjusting your search filters</p>
      </div>
    </div>
  );
}