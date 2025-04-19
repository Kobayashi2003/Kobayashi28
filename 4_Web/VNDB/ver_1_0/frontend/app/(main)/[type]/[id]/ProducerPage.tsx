import { Producer } from "@/lib/types"

import { ProducerDetailsPanel } from "@/components/panel/ProducerDetailsPanel"

interface ProducerPageProps {
  producer: Producer
} 

export default function ProducerPage({ producer }: ProducerPageProps) {
  return (
    <div>
      <h1>ProducerPage</h1>
    </div>
  )
}