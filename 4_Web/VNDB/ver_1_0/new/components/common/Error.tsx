import { AlertTriangle } from "lucide-react";

interface ErrorProps {
  message?: string;
  className?: string;
}

export function Error({
  message = "Something went wrong",
  className = "",
}: ErrorProps) {
  return (
    <div className={`flex flex-col items-center justify-center gap-4 ${className}`}>
      <div className="p-4 bg-red-500/20 rounded-full">
        <AlertTriangle className="w-12 h-12 text-red-400" />
      </div>
      <div className="space-y-2 text-center">
        <h3 className="text-lg font-medium text-red-300">{message}</h3>
        <p className="text-sm text-gray-400">
          Please try again later or contact support
        </p>
      </div>
    </div>
  );
}