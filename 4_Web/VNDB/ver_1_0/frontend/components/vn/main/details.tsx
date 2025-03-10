"use client"

import type React from "react"
import { cn } from "@/lib/utils"

import type { VN } from "@/lib/types"

import { Row } from "./row"
import { Titles } from "./titles"
import { Links } from "./links"
import { Platforms } from "./platforms"
import { Relations } from "./relations"
import { Developers } from "./developers"
import { VNImage } from "./image"

// Props for the VNDetails component
interface VNDetailsProps {
  vn: VN
}

const LENGTH_DISPLAY : Record<number, string> = {
  1 : "Very Short",
  2 : "short",
  3 : "Medium",
  4 : "Long",
  5 : "Very Long"
}

// Main component for displaying visual novel details
export function VNDetails({ vn }: VNDetailsProps) {

  const mainTitle = vn.title
  const subTitle = vn.titles?.find((t) => t.official && t.main)?.title

  const length = vn.length && LENGTH_DISPLAY[vn.length]
  const lengthHours = vn.length_minutes && Math.floor(vn.length_minutes / 60)
  const lengthMinutes = vn.length_minutes && vn.length_minutes % 60
  const lengthVotes = vn.length_votes

  return (
    <>
      {/* Header section with title and subtitle */}
      {(mainTitle || subTitle) && (
        <div className="p-4 border-b border-white/10">
          <div className="max-w-3xl pl-2">
            <div className="text-lg text-white/90">{mainTitle}</div>
            {subTitle && <div className="text-sm text-white/60">{subTitle}</div>}
          </div>
        </div>
      )}

      {/* Main content grid */}
      <div className={cn("grid gap-6 p-6", vn.image?.url ? "md:grid-cols-[250px_1fr]" : "grid-cols-1")}>

        {/* Image Section */}
        {vn.image?.url && (
          <div className="flex flex-col items-center">
            <VNImage image={vn.image} title={mainTitle || ""} />
          </div>
        )}

        {/* Details Section */}
        <div className="space-y-4 min-w-0">

          {vn.titles && vn.titles.length > 0 && (
            <div className="pb-4 border-b border-white/10">
              <Titles titles={vn.titles} />
            </div>
          )}

          <div className="grid gap-2">
            {vn.olang && <Row label={ "Original Language" } value={vn.olang} />}
            {vn.released && <Row label={ "Release Date" } value={vn.released} />}
            {(vn.length || vn.length_minutes) && <Row label={ "Length" } value={ 
              (length) + (vn.length_minutes ? ` (` + (lengthHours ? `${lengthHours}h` : ``) + (lengthMinutes ? `${lengthMinutes}m` : ``) + ` from ${lengthVotes} votes)` : ``)} 
            />}
            {/* {vn.rating && <Row label={ "Rating" } value={
              vn.rating && `${vn.rating.toFixed(0)} (${vn.votecount} votes)`} 
            />} */}
            {vn.developers && vn.developers.length > 0 &&<Row label={ "Developers" } value={
              <Developers developers={vn.developers} />} 
            />}
            {vn.platforms && vn.platforms.length > 0 && <Row label={ "Platforms" } value={
              <Platforms platforms={vn.platforms} />} 
            />}
            {vn.extlinks && vn.extlinks.length > 0 && <Row label={ "Links" } value={
              <Links extlinks= {vn.extlinks} />} 
            />}
          </div>

          {vn.relations && vn.relations.length > 0 && (
            <div className="border-t border-white/10 pt-4">
              <h3 className="text-sm font-semibold text-white/90 mb-2">Relations</h3>
              <Relations relations={vn.relations} />
            </div>
          )}

          {vn.description && (
            <div className="border-t border-white/10 pt-4">
              <h3 className="text-sm font-semibold text-white/90 mb-2">Description</h3>
              <p className="text-sm text-white/80 leading-relaxed break-words">{vn.description}</p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}