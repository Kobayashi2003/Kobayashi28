import { VN } from "@/lib/types"

import { VNDetailsPanel } from "@/components/panel/VNDetailsPanel"

interface VNPageProps {
  vn: VN
}

export default function VNPage({ vn }: VNPageProps) {
  return (
    <div>
      <VNDetailsPanel vn={vn} />
    </div>
  )
}
