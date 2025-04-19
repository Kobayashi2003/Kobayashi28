import { Trait } from "@/lib/types"

import { TraitDetailsPanel } from "@/components/panel/TraitDetailsPanel"

interface TraitPageProps {
  trait: Trait
}

export default function TraitPage({ trait }: TraitPageProps) {
  return (
    <div>
      <h1>TraitPage</h1>
    </div>
  )
}
