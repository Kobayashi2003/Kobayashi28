"use client"

import { useState, useEffect } from "react"

import { cn } from "@/lib/utils"
import { Row } from "../common/Row"
import { Image2 } from "../common/Image2"
import { TitlesRow } from "./TitlesRow"
import { PlatformsRow } from "./PlatformsRow"
import { DevelopersRow } from "./DevelopersRow"
import { RelationsRow } from "./RelationsRow"
import { ExtlinksRow } from "../common/ExtlinksRow"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"

import type { VN } from "@/lib/types"

interface VNDetailsPanelProps {
  vn: VN
}

export function VNDetailsPanel({ vn }: VNDetailsPanelProps) {

  // TITLE
  const mainTitle = vn.title
  const subTitle = vn.titles.find((t) => t.official && t.main)?.title || ""

  // IMAGE
  const image_url = vn.image?.url
  const image_dims = vn.image?.dims
  const image_thumbnail = vn.image?.thumbnail
  const image_thumbnail_dims = vn.image?.thumbnail_dims
  const image_sexual = vn.image?.sexual
  const image_violence = vn.image?.violence

  // TITLES ROW
  const titles = vn.titles

  // PLATFORMS ROW
  const platforms = vn.platforms

  // DEVELOPERS ROW
  const developers = vn.developers

  // LENGTH ROW
  const length = vn.length 
  const lengthHours = vn.length_minutes && Math.floor(vn.length_minutes / 60)
  const lengthMinutes = vn.length_minutes && vn.length_minutes % 60
  const lengthVotes = vn.length_votes

  // RELATIONS ROW
  const relations = vn.relations

  // EXTLINKS ROW
  const extlinks = vn.extlinks

  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  useEffect(() => {

  }, [sexualLevel, violenceLevel])

  return (
    <div className="container mx-auto">
      {mainTitle}
    </div>
  )
}