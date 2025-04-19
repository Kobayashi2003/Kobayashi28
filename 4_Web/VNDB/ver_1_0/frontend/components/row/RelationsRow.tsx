"use client"

import { useState } from "react"
import Link from "next/link"
import { ENUMS } from "@/lib/enums"

interface Relation {
  id: string
  title: string
  relation: string
  relation_official: boolean
}

interface RelationsRowProps {
  relations: Relation[]
}

export function RelationsRow({ relations }: RelationsRowProps) {
  if (!relations?.length) return null

  const [showUnofficial, setShowUnofficial] = useState(false)

  const groupedRelations = relations.reduce(
    (groups, relation) => {
      if (!showUnofficial && !relation.relation_official) return groups
      const group = relation.relation || "other"
      if (!groups[group]) {
        groups[group] = []
      }
      groups[group].push(relation)
      return groups
    },
    {} as Record<string, Relation[]>
  )

  return (
    <div className="grid grid-cols-[120px_1fr] gap-1">
      <div className="flex flex-col gap-1">
        <h3 className="font-bold text-left md:text-center text-white/80">Relations</h3>
        <button 
          onClick={() => setShowUnofficial(!showUnofficial)}
          className="text-left md:text-center text-white/60 text-xs cursor-pointer"
        >
          {showUnofficial ? "(Hide Unofficial)" : "(Show Unofficial)"}
        </button>
      </div>
      <div className="flex items-center text-xs md:text-sm">
        <div className="flex flex-col gap-1">
          {Object.entries(groupedRelations).map(([group, items]) => (
            <div key={group} className="flex flex-col gap-1">
              <h4 className="text-white">
                {ENUMS.RELATION[group as keyof typeof ENUMS.RELATION]}
              </h4>
              <div className="flex flex-col gap-1">
                {items.map((item) => (
                  <div key={item.id} className="flex gap-1 items-center">
                    <Link href={`/${item.id}`} className="text-blue-400 hover:text-blue-500 transition-colors">
                      {item.title}
                    </Link>
                    {!item.relation_official && (
                      <p className="text-white/60 text-xs">
                        (unofficial)
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
