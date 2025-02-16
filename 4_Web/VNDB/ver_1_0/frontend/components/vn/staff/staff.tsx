import type { VN } from "@/lib/types"
import { StaffGroup } from "./staff-group"

interface StaffProps {
  vn: VN
}

interface Staff {
  id?: string;
  name?: string;
  eid?: number;
  role?: string;
  note?: string;
}

export function VNStaff({ vn }: StaffProps) {
  const staffList = vn.staff ?? []

  // Group staff by edition name
  const groupedStaff = staffList.reduce(
    (groups, staff) => {
      const editionName: string =
        staff.eid === null ? "Original edition" : (vn.editions?.find((e) => e.eid === staff.eid)?.name ?? "Unknown")
      if (!groups[editionName]) {
        groups[editionName] = []
      }
      groups[editionName].push(staff)
      return groups
    },
    {} as Record<string, Staff[]>,
  )

  // Sort editions: "Original edition" first, then others alphabetically
  const sortedEditions = Object.entries(groupedStaff).sort(([a], [b]) => {
    if (a === "Original edition") return -1
    if (b === "Original edition") return 1
    return a.localeCompare(b)
  })

  return (
    <div className="space-y-2">
      {sortedEditions.map(([editionName, staffList]) => (
        <StaffGroup
          key={editionName}
          editionName={editionName}
          staffList={staffList}
        />
      ))}
    </div>
  )
}