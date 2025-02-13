"use client"

import { useState, useMemo, Fragment } from "react"
import { cn } from "@/lib/utils"
import type { VN } from "@/lib/types"
import { CharacterItem } from "./character-item"

interface CharactersProps {
  vn: VN
}

// Define role order for sorting
const roleOrder = { main: 0, primary: 1, side: 2, appears: 3 }

// Sort characters by role and name
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

export function Characters({ vn }: CharactersProps) {
  const [spoilerLevel, setSpoilerLevel] = useState(0)

  // Memoize filtered and sorted characters
  const filteredCharacters = useMemo(() => {
    if (!vn.characters?.length) return []

    return vn.characters
      .filter((character) => {
        const vnInfo = character.vns?.find((v) => v.id === vn.id)
        return (vnInfo?.spoiler || 0) <= spoilerLevel
      })
      .sort((a, b) => {
        const roleA = a.vns?.find((v) => v.id === vn.id)?.role
        const roleB = b.vns?.find((v) => v.id === vn.id)?.role
        return sortCharacters(roleA, roleB, a.name, b.name)
      })
  }, [vn.characters, vn.id, spoilerLevel])

  if (!filteredCharacters.length) return null

  return (
    <div className="space-y-4">
      {/* Spoiler control buttons */}
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg text-white/90">Characters</h3>
        <div className="flex items-center gap-2 text-sm">
          {[
            { level: 0, text: "Hide spoilers", color: "text-[#88ccff]" },
            { level: 1, text: "Show minor spoilers", color: "text-[#ffcc66]" },
            { level: 2, text: "Spoil me!", color: "text-[#ff6666]" },
          ].map((button, index) => (
            <Fragment key={button.level}>
              {index > 0 && <span className="text-white/20">|</span>}
              <button
                onClick={() => setSpoilerLevel(button.level)}
                className={cn(
                  "hover:text-white transition-colors",
                  spoilerLevel === button.level ? button.color : "text-white/60",
                )}
              >
                {button.text}
              </button>
            </Fragment>
          ))}
        </div>
      </div>

      {/* Character grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-4">
        {filteredCharacters.map((character) => {
          const vnRole = character.vns?.find((v) => v.id === vn.id)?.role

          return (
            <CharacterItem
              key={character.id}
              id={character.id}
              name={character.name}
              sex={character.sex}
              role={vnRole}
              vn={vn}
            />
          )
        })}
      </div>
    </div>
  )
}