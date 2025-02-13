import Link from "next/link"
import type { VN } from "@/lib/types"

interface StaffItemProps {
  staff: NonNullable<VN["staff"]>[number]
}

export function StaffItem({ staff }: StaffItemProps) {
  return (
    <div className="flex items-baseline gap-2 text-sm truncate">
      <Link href={`/s${staff.id}`} className="text-[#88ccff] hover:text-white transition-colors shrink-0">
        {staff.name}
      </Link>
      {staff.note && <span className="text-[#4488cc] truncate">{staff.note}</span>}
    </div>
  )
}