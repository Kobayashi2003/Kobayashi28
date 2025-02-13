import Link from "next/link"
import type { Character } from "@/lib/types"
import { cn } from "@/lib/utils"

interface TraitsProps {
  traits: NonNullable<Character["traits"]>
  showSexualTraits: boolean
  spoilerLevel: number
}

export function Traits({ traits, showSexualTraits, spoilerLevel }: TraitsProps) {
  // Filter and sort traits
  const filteredAndSortedTraits = traits
    .filter((trait) => {
      const isSexualTrait = trait.group_name?.toLowerCase().includes("sexual") ?? false
      const isWithinSpoilerLevel = (trait.spoiler || 0) <= spoilerLevel
      return (showSexualTraits || !isSexualTrait) && isWithinSpoilerLevel
    })
    .sort((a, b) => {
      return (a.group_id || "").localeCompare(b.group_id || "") || (a.id || "").localeCompare(b.id || "")
    })

  // Group traits
  const groupedTraits = filteredAndSortedTraits.reduce(
    (groups, trait) => {
      const groupId = trait.group_id || "other"
      if (!groups[groupId]) {
        groups[groupId] = { name: trait.group_name || "Other", traits: [] }
      }
      groups[groupId].traits.push(trait)
      return groups
    },
    {} as Record<string, { name: string; traits: typeof traits }>,
  )

  return (
    <div className="grid gap-2">
      {Object.entries(groupedTraits).map(([groupId, { name, traits }]) => (
        <div key={groupId} className="grid grid-cols-[100px_1fr] gap-2 items-start text-sm">
          <Link
            href={`/${groupId}`}
            className="text-white/60 font-medium shrink-0 hover:text-white/80 transition-colors"
          >
            {name}
          </Link>
          <div>
            {traits.map((trait, index) => (
              <span key={trait.id}>
                <Link
                  href={`/${trait.id}`}
                  className={cn(
                    trait.spoiler === 1 ? "text-[#ffcc66]" : trait.spoiler === 2 ? "text-[#ff6666]" : "text-[#88ccff]",
                    "hover:text-white transition-colors",
                  )}
                >
                  {trait.name}
                </Link>
                {index < traits.length - 1 && <span className="text-white/20 mx-1">•</span>}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}