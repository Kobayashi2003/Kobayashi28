import { SearchX } from "lucide-react";

interface NotFoundProps {
  message?: string;
  className?: string;
}

export function NotFound({
  message = "No results found",
  className = "",
}: NotFoundProps) {
  return (
    <div className={`flex flex-col items-center justify-center gap-4 ${className}`}>
      <div className="p-4 bg-gray-700/20 rounded-full">
        <SearchX className="w-12 h-12 text-gray-400" />
      </div>
      <div className="space-y-2 text-center">
        <h3 className="text-lg font-medium text-gray-200">{message}</h3>
        <p className="text-sm text-gray-400">
          Try adjusting your search filters
        </p>
      </div>
    </div>
  );
}