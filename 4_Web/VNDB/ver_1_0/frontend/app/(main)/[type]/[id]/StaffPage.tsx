import { Staff } from "@/lib/types"

import { StaffDetailsPanel } from "@/components/panel/StaffDetailsPanel"

interface StaffPageProps {
  staff: Staff
}

export default function StaffPage({ staff }: StaffPageProps) {
  return (
    <div>
      <h1>StaffPage</h1>
    </div>
  )
}
