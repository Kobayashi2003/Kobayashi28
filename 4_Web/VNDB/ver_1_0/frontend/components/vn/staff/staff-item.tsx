import Link from "next/link"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface Staff {
  id?: string;
  name?: string;
  eid?: number;
  role?: string;
  note?: string;
}

interface StaffItemProps {
  staff: Staff
}

export function StaffItem({ staff }: StaffItemProps) {
  return (
    <div className="flex items-baseline gap-2 text-sm">
      <Link href={`/s${staff.id}`} className="text-[#88ccff] hover:text-white transition-colors shrink-0">
        {staff.name}
      </Link>
      {staff.note && (
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <span className="text-[#4488cc] truncate cursor-help">{staff.note}</span>
            </TooltipTrigger>
            <TooltipContent side="top" className="bg-[#0F2942] text-white p-2 rounded shadow-lg max-w-xs">
              <p>{staff.note}</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      )}
    </div>
  )
}