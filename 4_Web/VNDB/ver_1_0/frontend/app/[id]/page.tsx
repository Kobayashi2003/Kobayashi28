import { Suspense } from "react"

import { notFound } from "next/navigation"

import { api } from "@/lib/api"
import type { 
  VN as VNType, Release as ReleaseType, Character as CharacterType, 
  Producer as ProducerType, Staff as StaffType, Tag as TagType,
  Trait as TraitType, VisualNovelDataBaseQueryResponse,
} from "@/lib/types"


import { Details as VNDetails } from "@/components/vn/main/details"
import { Tags } from "@/components/vn/tags/tags"
import { Staff } from "@/components/vn/staff/staff"
import { Releases } from "@/components/vn/releases/releases"
import { Characters } from "@/components/vn/characters/characters"
import { Screenshots } from "@/components/vn/screenshots/screenshots"

import { CharacterDetails } from "@/components/character/main/details"

type ContentType = "vn" | "release" | "character" | "producer" | "staff" | "tag" | "trait"

function getContentType(id: string): ContentType | null {
  const firstChar = id.charAt(0).toLowerCase()
  const types: Record<string, ContentType> = {
    v: "vn",
    r: "release",
    c: "character",
    p: "producer",
    s: "staff",
    g: "tag",
    i: "trait"
  }
  return types[firstChar] || null
}

async function renderVNPage(vn: VNType) {
  if (!vn) return null

  // Safely handle release IDs
  return (
    <div className="container mx-auto px-4 py-6">
      <div className="max-w-5xl mx-auto space-y-6">

        <VNDetails vn={vn} />

        {vn.tags && vn.tags.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h3 className="text-lg font-semibold text-white/90">Tags</h3>
            </div>
            <div className="p-4">
              <Tags vn={vn} />
            </div>
          </div>
        )}

        {vn.releases && vn.releases.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h3 className="text-lg font-semibold text-white/90">Releases</h3>
            </div>
            <div className="p-4">
              <Suspense fallback={<div>Loading releases...</div>}>
                <Releases vn={vn} />
              </Suspense>
            </div>
          </div>
        )}

        {vn.characters && vn.characters.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h2 className="text-lg text-white/90 pl-2">Characters</h2>
            </div>
            <div className="p-6">
              <Characters vn={vn} />
            </div>
          </div>
        )}

        {vn.staff && vn.staff.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h3 className="text-lg font-semibold text-white/90">Staff</h3>
            </div>
            <div className="p-4">
              <Staff vn={vn} />
            </div>
          </div>
        )}

        {vn.screenshots && vn.screenshots.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h3 className="text-lg font-semibold text-white/90">Screenshots</h3>
            </div>
            <div className="p-4">
              <Screenshots vn={vn} />
            </div>
          </div>
        )}

      </div>
    </div>
  )
}

async function renderReleasepage(releaseResult: ReleaseType) {
}

async function renderCharacterPage(character: CharacterType) {
  if (!character) return null

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="max-w-5xl mx-auto">
        <CharacterDetails character={character} />
      </div>
    </div>
  )
}

async function renderProducerPage(producer: ProducerType) {
}

async function renderStaffPage(staff: StaffType) {
}

async function renderTagPage(tag: TagType) {
}

async function renderTraitPage(trait: TraitType) {
}

export default async function DetailPage({ params }: { params: { id: string } }) {
  const contentType = getContentType(params.id)
  if (!contentType) {
    notFound()
  }

  const id = params.id.slice(1)

  try {
    let response: VisualNovelDataBaseQueryResponse<VNType | ReleaseType | CharacterType | ProducerType | StaffType>
    switch (contentType) {
      case "vn":
        response = await api.vn(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderVNPage(response.results[0] as VNType)

      case "character":
        response = await api.character(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderCharacterPage(response.results[0] as CharacterType)

      case "producer":
        response = await api.producer(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderProducerPage(response.results[0] as ProducerType)

      case "staff":
        response = await api.staff(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderStaffPage(response.results[0] as StaffType)

      case "tag":
        response = await api.tag(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderTagPage(response.results[0] as TagType)

      case "trait":
        response = await api.trait(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderTraitPage(response.results[0] as TraitType)

      default:
        notFound()
    }
  } catch (error) {
    console.error(`Error fetching ${contentType} data:`, error)
    notFound()
  }
}