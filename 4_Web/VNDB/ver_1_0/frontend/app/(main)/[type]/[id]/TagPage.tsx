import { Tag } from "@/lib/types"

import { TagDetailsPanel } from "@/components/panel/TagDetailsPanel"

interface TagPageProps {
  tag: Tag
}

export default function TagPage({ tag }: TagPageProps) {
  return (
    <div>
      <TagDetailsPanel tag={tag} />
    </div>
  )
}
