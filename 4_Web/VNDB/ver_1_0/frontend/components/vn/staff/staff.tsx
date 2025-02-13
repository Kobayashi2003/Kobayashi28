import type { VN } from "@/lib/types"
import { StaffGroup } from "./staff-group"

interface StaffProps {
  vn: VN
}

export function Staff({ vn }: StaffProps) {
  // Create a Map to store staff by edition
  const staffByEdition = new Map<number, { name: string; staff: typeof vn.staff }>()

  // Add Original edition (eid: 0)
  staffByEdition.set(0, {
    name: "Original edition",
    staff: vn.staff?.filter((s) => s.eid === 0) || [],
  })

  // Add other editions
  vn.editions?.forEach((edition) => {
    if (edition.eid) {
      const editionId = Number.parseInt(edition.eid)
      staffByEdition.set(editionId, {
        name: edition.name || `Edition ${edition.eid}`,
        staff: vn.staff?.filter((s) => s.eid === editionId) || [],
      })
    }
  })

  return (
    <div className="space-y-2">
      {Array.from(staffByEdition.entries())
        .filter(([_, { staff }]) => staff && staff.length > 0)
        .map(([eid, { name, staff }]) => (
          <StaffGroup key={eid} name={name} staff={staff || []} isOriginal={eid === 0} />
        ))}
    </div>
  )
}