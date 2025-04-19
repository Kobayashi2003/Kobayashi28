import Link from "next/link"

// Interface for a single relation
interface Relation {
  id?: string
  relation?: string
  title?: string
  relation_official?: boolean
}

// Props for the Relations component
interface RelationsProps {
  relations?: Relation[]
}

const RELATIONS_DISPLAY: Record<string, string> = {
  ser: "Same series",
  char: "Shares characters",
  alt: "Alternative version",
  preq: "Prequel",
  seq: "Sequel",
  side: "Side story",
  set: "Same setting",
  fan: "Fandisc",
  orig: "Original game",
  par: "Parent story",
  child: "Child story",
  other: "Other",
}

// Component to display related visual novels
export function Relations({ relations }: RelationsProps) {
  if (!relations?.length) return null

  // Group relations by their relation type
  const groupedRelations = relations.reduce(
    (groups, relation) => {
      const group = relation.relation || "other"
      if (!groups[group]) {
        groups[group] = []
      }
      groups[group].push(relation)
      return groups
    },
    {} as Record<string, Relation[]>,
  )

  return (
    <div className="space-y-3">
      {Object.entries(groupedRelations).map(([group, items]) => (
        <div key={group} className="grid grid-cols-[120px_1fr] gap-4 items-start">
          {/* Relation type label */}
          <div className="text-white/60 text-sm">{RELATIONS_DISPLAY[group] || group}</div>
          {/* List of related visual novels */}
          <div className="space-y-1">
            {items.map((relation) => (
              <div key={relation.id} className="flex items-center gap-1 text-sm">
                <Link href={`/${relation.id}`} className="text-white/90 hover:text-white">
                  {relation.title}
                </Link>
                {/* Display 'unofficial' label if not an official relation */}
                {!relation.relation_official && <span className="text-white/60 text-xs">(unofficial)</span>}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}