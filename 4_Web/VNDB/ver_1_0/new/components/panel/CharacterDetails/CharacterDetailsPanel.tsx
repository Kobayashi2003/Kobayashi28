"use client"

import { useState, useEffect } from "react"

import { cn } from "@/lib/utils"
import { Row } from "../common/Row"
import { Image2 } from "../common/Image2"
import { AliasesRow } from "./AliasesRow"
import { SeiyuuRow } from "./SeiyuuRow"
import { TraitsRow } from "./TraitsRow"
import { VNsRow } from "./VNsRow"

import type { Character } from "@/lib/types"

interface CharacterDetailsPanelProps {
  character: Character
  loading?: boolean
  error?: string | null
}

export function CharacterDetailsPanel({ character, loading, error }: CharacterDetailsPanelProps) {

  // TITLE
  const title = character.name
  const subTitle = character.original

  // IMAGE
  const image_url = character.image?.url
  const image_dims = character.image?.dims
  const image_sexual = character.image?.sexual
  const image_violence = character.image?.violence

  // ALIASES ROW
  const aliases = character.aliases

  // SEIYUU ROW
  const seiyuu = character.seiyuu

  // TRAITS ROW
  const traits = character.traits

  // VNS ROW
  const vns = character.vns

  return (
    <div>
      {loading && (
        <></>
      )}
      {error && (
        <></>
      )}
      {!loading && !error && (
        <></>
      )}
    </div>
  )
}
