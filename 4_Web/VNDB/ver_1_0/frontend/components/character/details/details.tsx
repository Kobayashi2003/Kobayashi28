"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import type { Character } from "@/lib/types"
import { CharacterImage } from "./image"
import { Row } from "./row"
import { Traits } from "./traits"
import { VNs } from "./vns"
import { Seiyuu } from "./seiyuu"
import { Button } from "@/components/ui/button"
import { SpoilerControls } from "./spoiler-controls"

interface CharacterDetailsProps {
  character: Character
}

export function Details({ character }: CharacterDetailsProps) {
  const [showSexualTraits, setShowSexualTraits] = useState(false)
  const [spoilerLevel, setSpoilerLevel] = useState(0)

  // Format physical measurements
  const measurements = [
    character.height && `Height: ${character.height}cm`,
    character.weight && `Weight: ${character.weight}kg`,
    character.bust &&
      character.waist &&
      character.hips &&
      `Bust-Waist-Hips: ${character.bust}-${character.waist}-${character.hips}cm`,
    character.cup && `${character.cup} cup`,
  ]
    .filter(Boolean)
    .join(", ")

  const detailsData = {
    Measurements: { value: measurements },
    Birthday: {
      value:
        character.birthday &&
        new Date(`2000-${character.birthday}`).toLocaleDateString("en-US", {
          day: "numeric",
          month: "long",
        }),
    },
  }

  return (
    <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
      <div className="p-4 border-b border-white/10 flex justify-between items-center">
        <div className="max-w-3xl pl-2">
          <div className="text-lg text-white/90">{character.name}</div>
          {character.original && <div className="text-sm text-white/60">{character.original}</div>}
        </div>
        <div className="flex items-center gap-4">
          <SpoilerControls value={spoilerLevel} onChange={setSpoilerLevel} />
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSexualTraits(!showSexualTraits)}
            className="text-xs bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20 text-white"
          >
            {showSexualTraits ? "Hide" : "Show"} sexual traits
          </Button>
        </div>
      </div>

      <div className={cn("grid gap-6 p-6", character.image ? "md:grid-cols-[250px_1fr]" : "grid-cols-1")}>
        <CharacterImage image={character.image} alt={character.name} />

        <div className="space-y-4 min-w-0">
          {/* Basic Details */}
          <div className="grid gap-2">
            {Object.entries(detailsData).map(([key, { value }]) => {
              if (!value) return null
              return <Row key={key} label={key} value={value} />
            })}
            {character.seiyuu && character.seiyuu.length > 0 && <Seiyuu seiyuu={character.seiyuu} />}
          </div>

          {/* Traits */}
          {character.traits && character.traits.length > 0 && (
            <div className="space-y-4">
              <Traits traits={character.traits} showSexualTraits={showSexualTraits} spoilerLevel={spoilerLevel} />
            </div>
          )}

          {/* Visual Novels */}
          {character.vns && character.vns.length > 0 && (
            <div className="border-t border-white/10 pt-4">
              <h3 className="text-sm font-semibold text-white/90 mb-2">Appears In</h3>
              <VNs vns={character.vns} />
            </div>
          )}

          {/* Description */}
          {character.description && (
            <div className="border-t border-white/10 pt-4">
              <h3 className="text-sm font-semibold text-white/90 mb-2">Description</h3>
              <p className="text-sm text-white/80 leading-relaxed break-words">{character.description}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}