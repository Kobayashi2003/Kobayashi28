import Link from "next/link"
import type { Character } from "@/lib/types"
import { cn } from "@/lib/utils"

interface TraitsProps {
  traits: NonNullable<Character["traits"]>
  showSexual: boolean
  spoilerLevel: number
}

export function Traits({ traits, showSexual, spoilerLevel }: TraitsProps) {
  // Filter and group traits
  const groupedTraits = traits.reduce((groups, trait) => {
    // Filter out traits based on sexual content and spoiler level
    const isSexualTrait = trait.group_name?.toLowerCase().includes("sexual") ?? false
    const isWithinSpoilerLevel = (trait.spoiler || 0) <= spoilerLevel
    if ((showSexual || !isSexualTrait) && isWithinSpoilerLevel) {
      const groupId = trait.group_id || "other"
      if (!groups[groupId]) {
        groups[groupId] = { name: trait.group_name || "Other", traits: [] }
      }
      groups[groupId].traits.push(trait)
    }
    return groups
  }, {} as Record<string, { name: string; traits: typeof traits }>)

  // Sort groups and traits within groups
  const sortedGroups = Object.entries(groupedTraits).sort(([a], [b]) => a.localeCompare(b))

  return (
    <div className="grid gap-2">
      {sortedGroups.map(([groupId, { name, traits }]) => (
        <div key={groupId} className="grid grid-cols-[100px_1fr] gap-2 items-start text-sm">
          {/* Trait group name */}
          <Link
            href={`/${groupId}`}
            className="text-white/60 font-medium shrink-0 hover:text-white/80 transition-colors"
          >
            {name}
          </Link>
          {/* Traits list */}
          <div className="flex flex-wrap items-center">
            {traits
              .sort((a, b) => (a.id || "").localeCompare(b.id || ""))
              .map((trait, index, array) => (
                <span key={trait.id} className="flex items-center">
                  {/* Individual trait */}
                  <Link
                    href={`/${trait.id}`}
                    className={cn(
                      trait.spoiler === 1 ? "text-[#ffcc66]" : 
                      trait.spoiler === 2 ? "text-[#ff6666]" : "text-[#88ccff]",
                      "hover:text-white transition-colors",
                    )}
                  >
                    {trait.name}
                  </Link>
                  {/* Separator dot */}
                  {index < array.length - 1 && <span className="text-white/20 mx-1">•</span>}
                </span>
              ))}
          </div>
        </div>
      ))}
    </div>
  )
}