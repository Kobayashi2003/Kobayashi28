"use client"

import { useState } from "react"
import type { VN } from "@/lib/types"
import { CharacterItem } from "./character-item"
import { cn } from "@/lib/utils"

interface CharactersProps {
  vn: VN
}

const roleOrder = { main: 0, primary: 1, side: 2, appears: 3 }

function sortCharacters(
  roleA: string | undefined,
  roleB: string | undefined,
  nameA: string | undefined,
  nameB: string | undefined,
): number {
  const roleValueA = roleOrder[(roleA || "appears") as keyof typeof roleOrder]
  const roleValueB = roleOrder[(roleB || "appears") as keyof typeof roleOrder]

  if (roleValueA !== roleValueB) {
    return roleValueA - roleValueB
  }

  return (nameA || "").localeCompare(nameB || "")
}

export function VNCharacters({ vn }: CharactersProps) {
  const [spoilerLevel, setSpoilerLevel] = useState(0)

  if (!vn.characters?.length) return null

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 text-sm justify-end">
        <button
          onClick={() => setSpoilerLevel(0)}
          className={cn("transition-colors", spoilerLevel === 0 ? "text-[#88ccff]" : "text-white/60 hover:text-white")}
        >
          Hide spoilers
        </button>
        <span className="text-white/20">|</span>
        <button
          onClick={() => setSpoilerLevel(1)}
          className={cn("transition-colors", spoilerLevel === 1 ? "text-[#ffcc66]" : "text-white/60 hover:text-white")}
        >
          Show minor spoilers
        </button>
        <span className="text-white/20">|</span>
        <button
          onClick={() => setSpoilerLevel(2)}
          className={cn("transition-colors", spoilerLevel === 2 ? "text-[#ff6666]" : "text-white/60 hover:text-white")}
        >
          Spoil me!
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-4">
        {vn.characters
          ?.filter((character) => {
            const vnInfo = character.vns?.find((v) => v.id === vn.id)
            return (vnInfo?.spoiler || 0) <= spoilerLevel
          })
          .sort((a, b) => {
            const roleA = a.vns?.find((v) => v.id === vn.id)?.role
            const roleB = b.vns?.find((v) => v.id === vn.id)?.role
            return sortCharacters(roleA, roleB, a.name, b.name)
          })
          .map((character) => {
            return (
              <CharacterItem
                key={character.id}
                vn={vn}
                character={character}
              />
            )
          })}
      </div>
    </div>
  )
}