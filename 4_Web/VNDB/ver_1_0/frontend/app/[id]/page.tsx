import { Suspense } from "react"

import { notFound } from "next/navigation"

import { api } from "@/lib/api"
import type { 
  VN as VNType, Release as ReleaseType, Character as CharacterType, 
  Producer as ProducerType, Staff as StaffType, Tag as TagType,
  Trait as TraitType, VisualNovelDataBaseQueryResponse,
} from "@/lib/types"


import { Details as VNDetails } from "@/components/vn/details/details"
import { Tags } from "@/components/vn/tags/tags"
import { Staff } from "@/components/vn/staff/staff"
import { Releases } from "@/components/vn/releases/releases"
import { Characters } from "@/components/vn/characters/characters"
import { Screenshots } from "@/components/vn/screenshots/screenshots"

import { Details as CharacterDetails } from "@/components/character/details/details"

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

async function renderVNPage(vnResult: VNType) {
  if (!vnResult) return null

  const hasImage = vnResult.image?.url
  const mainTitle = vnResult.titles?.find((t) => t.official && t.main)?.title

  const detailsData = {
    "Original Language": { value: vnResult.olang },
    "Release Date": { value: vnResult.released },
    Length: { value: vnResult.length && `${vnResult.length} hours (${vnResult.length_votes} votes)` },
    Rating: { value: vnResult.rating && `${vnResult.rating.toFixed(2)} (${vnResult.votecount} votes)` },
    Developers: { value: vnResult.developers?.map((dev) => dev.name).join(", ") },
    Links: { value: "Links" },
    Platforms: { value: "Platforms" },
  }

  const tags =
    vnResult.tags?.map((tag) => ({
      id: tag.id,
      name: tag.name,
      rating: tag.rating,
      spoiler: tag.spoiler,
      category: tag.category,
    })) || []

  // Safely handle release IDs
  const releaseIds =
    vnResult.releases
      ?.map((release) => release.id)
      .filter((id): id is string => id !== undefined)
      .map((id) => id.slice(1)) || []

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="max-w-5xl mx-auto space-y-6">
        <VNDetails
          image={hasImage ? vnResult.image!.url : undefined}
          title={vnResult.title}
          subtitle={mainTitle}
          titles={vnResult.titles}
          data={detailsData}
          description={vnResult.description}
          developers={vnResult.developers}
          relations={vnResult.relations}
          platforms={vnResult.platforms}
          links={vnResult.extlinks?.map((link) => ({ url: link.url || "", name: link.name || "" }))}
        />
        {tags.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h3 className="text-lg font-semibold text-white/90">Tags</h3>
            </div>
            <div className="p-4">
              <Tags tags={tags} />
            </div>
          </div>
        )}
        {releaseIds.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h3 className="text-lg font-semibold text-white/90">Releases</h3>
            </div>
            <div className="p-4">
              <Suspense fallback={<div>Loading releases...</div>}>
                <Releases releaseIds={releaseIds} />
              </Suspense>
            </div>
          </div>
        )}
        {vnResult.characters && vnResult.characters.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h2 className="text-lg text-white/90 pl-2">Characters</h2>
            </div>
            <div className="p-6">
              <Characters vn={vnResult} />
            </div>
          </div>
        )}
        {vnResult.staff && vnResult.staff.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h3 className="text-lg font-semibold text-white/90">Staff</h3>
            </div>
            <div className="p-4">
              <Staff vn={vnResult} />
            </div>
          </div>
        )}
        {vnResult.screenshots && vnResult.screenshots.length > 0 && (
          <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h3 className="text-lg font-semibold text-white/90">Screenshots</h3>
            </div>
            <div className="p-4">
              <Screenshots vn={vnResult} />
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