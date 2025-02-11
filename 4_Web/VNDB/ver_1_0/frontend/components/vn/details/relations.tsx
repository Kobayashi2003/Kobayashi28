import Link from "next/link"

interface Relation {
  id?: string
  relation?: string
  title?: string
  official?: boolean
}

interface RelationsProps {
  relations?: Relation[]
}

const RELATION_TYPES: Record<string, string> = {
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

export function Relations({ relations }: RelationsProps) {
  if (!relations?.length) return null

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
          <div className="text-white/60 text-sm">{RELATION_TYPES[group] || group}</div>
          <div className="space-y-1">
            {items.map((relation) => (
              <div key={relation.id} className="flex items-center gap-1 text-sm">
                <Link href={`/${relation.id}`} className="text-white/90 hover:text-white">
                  {relation.title}
                </Link>
                {!relation.official && <span className="text-white/60 text-xs">(unofficial)</span>}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}