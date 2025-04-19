import { VN } from "@/lib/types"

import { VNDetailsPanel } from "@/components/panel/VNDetailsPanel"
import { VNTagsPanel } from "@/components/panel/VNTagsPanel"
import { VNReleasesPanel } from "@/components/panel/VNReleasesPanel"
import { VNCharactersPanel } from "@/components/panel/VNCharactersPanel"
import { VNScreenshotsPanel } from "@/components/panel/VNScreenshotsPanel"

interface VNPageProps {
  vn: VN
}

export default function VNPage({ vn }: VNPageProps) {
  return (
    <div>
      <VNDetailsPanel vn={vn} />
      <VNTagsPanel vn={vn} />
      <VNReleasesPanel vn={vn} />
      <VNCharactersPanel vn={vn} />
      <VNScreenshotsPanel vn={vn} />
    </div>
  )
}
