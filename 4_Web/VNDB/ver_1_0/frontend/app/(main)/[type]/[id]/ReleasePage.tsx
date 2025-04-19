import { Release } from "@/lib/types"

import { ReleaseDetailsPanel } from "@/components/panel/ReleaseDetailsPanel"

interface ReleasePageProps {
  release: Release
}

export default function ReleasePage({ release }: ReleasePageProps) {
  return (
    <div>
      <h1>ReleasePage</h1>
    </div>
  )
}
