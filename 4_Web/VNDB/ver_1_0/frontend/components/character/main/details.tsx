"use client"

import { useState, Fragment } from "react"
import { cn } from "@/lib/utils"

import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

import type { Character } from "@/lib/types"
import { CHARACTER_ICONS } from "@/lib/constants"
import { CHARACTER_SEX_COLORS } from "@/lib/constants"

import { Row } from "./row"
import { Traits } from "./traits"
import { VNs } from "./vns"
import { Seiyuu } from "./seiyuu"
import { CharacterImage } from "./image"


interface CharacterDetailsProps {
  character: Character
}

const SEX_DISPLAY = {
  m: "Male",
  f: "Female",
  b: "Both",
  n: "Sexless",
}

export function CharacterDetails({ character }: CharacterDetailsProps) {
  const [showSexual, setShowSexualTraits] = useState(false)
  const [spoilerLevel, setSpoilerLevel] = useState(0)

  const measurements = [
    character.height && `Height: ${character.height}cm`,
    character.weight && `Weight: ${character.weight}kg`,
    character.bust && character.waist && character.hips &&
    `Bust-Waist-Hips: ${character.bust}-${character.waist}-${character.hips}cm`,
    character.cup && `${character.cup} cup`,
    character.blood_type && `Blood Type: ${character.blood_type.toUpperCase()}`
  ].filter(Boolean).join(", ")

  const birthdayMatch = typeof character.birthday === 'string' ? character.birthday.match(/(\d+)\D+(\d+)/) : null
  const month  = birthdayMatch && birthdayMatch[1]
  const day = birthdayMatch && birthdayMatch[2]

  const birthday = (month && day) &&
    new Date(`2000-${month.padStart(2, "0")}-${day.padStart(2, "0")}`)
    .toLocaleDateString("en-US", {
      day: "numeric",
      month: "long",
    })

  const getSexIcon = (sex: string) => (
    <span
      className={cn(
        CHARACTER_ICONS[sex as keyof typeof CHARACTER_ICONS],
        CHARACTER_SEX_COLORS[sex as keyof typeof CHARACTER_SEX_COLORS],
      )}
    />
  )

  const renderSexIcon = () => (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger className="flex items-center gap-1">
          {character.sex && character.sex[0] && getSexIcon(character.sex[0])}
          {spoilerLevel > 1 && character.sex && character.sex[1] && character.sex[0] !== character.sex[1] && (
            <>
              <span className="text-white/20 mx-1">→</span>
              {getSexIcon(character.sex[1])}
            </>
          )}
        </TooltipTrigger>
        <TooltipContent side="top" className="bg-[#0F2942]">
          <p className="text-white">
            {character.sex && character.sex[0] && (
              <>
                {getSexIcon(character.sex[0])}
                <span className="ml-1">{SEX_DISPLAY[character.sex[0] as keyof typeof SEX_DISPLAY]}</span>
              </>
            )}
            {spoilerLevel > 0 && character.sex && character.sex[1] && character.sex[0] !== character.sex[1] && (
              <>
                <span className="text-white/60 mx-1">→</span>
                {getSexIcon(character.sex[1])}
                <span className="ml-1">{SEX_DISPLAY[character.sex[1] as keyof typeof SEX_DISPLAY]}</span>
              </>
            )}
          </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )

  return (
    <>
      <div className="p-4 border-b border-white/10 flex justify-between items-center">
        {/* Character name section */}
        <div className="max-w-3xl pl-2">
          <div className="text-lg text-white/90">{character.name}</div>
        </div>
        {/* Controls section */}
        <div className="flex items-center gap-4">
          {/* Spoiler level controls */}
          <div className="flex items-center gap-2 text-sm">
            {/* Map through spoiler levels and create buttons */}
            {[
              { level: 0, text: "Hide spoilers", color: "text-[#88ccff]" },
              { level: 1, text: "Show minor spoilers", color: "text-[#ffcc66]" },
              { level: 2, text: "Spoil me!", color: "text-[#ff6666]" },
            ].map((button, index) => (
              <Fragment key={button.level}>
                {/* Add separator between buttons, except for the first one */}
                {index > 0 && <span className="text-white/20 ml-2">|</span>}
                {/* Spoiler level button */}
                <button
                  onClick={() => setSpoilerLevel(button.level)}
                  className={cn(
                    "hover:text-white transition-colors",
                    // Apply color based on whether this level is currently selected
                    spoilerLevel === button.level ? button.color : "text-white/60",
                  )}
                >
                  {button.text}
                </button>
              </Fragment>
            ))}
          </div>
          {/* Toggle button for showing/hiding sexual traits */}
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSexualTraits(!showSexual)}
            className="text-xs bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20 text-white"
          >
            {showSexual ? "Hide" : "Show"} sexual traits
          </Button>
        </div>
      </div>

      <div className={cn("grid gap-6 p-6", character.image ? "md:grid-cols-[250px_1fr]" : "grid-cols-1")}>

        {/* Only render if character image URL exists */}
        {character.image?.url && (
          <div className="flex flex-col items-center">
            <CharacterImage image={character.image} name={character.name || ""} />
          </div>
        )}

        <div className="space-y-4 min-w-0">
          {/* Rows */}
          <Row label={character.name ?? ""} value={<div className="flex items-center gap-2"> {character.original} {renderSexIcon()} </div>} />
          <Row label="Measurements" value={measurements} />
          <Row label="Birthday" value={birthday} />

          {/* Traits */}
          {character.traits && character.traits.length > 0 && (
            <Traits traits={character.traits} showSexual={showSexual} spoilerLevel={spoilerLevel} />
          )}

          {/* Seiyuu */}
          {character.seiyuu && character.seiyuu.length > 0 && (
            <Row label="Voiced by" value={<Seiyuu seiyuuList={character.seiyuu} />} />
          )}

          {/* Visual Novels */}
          {character.vns && character.vns.length > 0 && (
            <div className={cn("border-t border-white/10 pt-4", character.description && "pb-4")}>
              <h3 className="text-sm font-semibold text-white/90 mb-2">Appears In</h3>
              <VNs vns={character.vns} />
            </div>
          )}

          {/* Description */}
          {character.description && (
            <div className={cn("border-t border-white/10 pt-4", !character.vns?.length && "mt-4")}>
              <h3 className="text-sm font-semibold text-white/90 mb-2">Description</h3>
              <p className="text-sm text-white/80 leading-relaxed break-words">{character.description}</p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}