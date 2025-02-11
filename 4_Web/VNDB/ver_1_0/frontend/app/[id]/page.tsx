import { Suspense } from "react"
import { VNDetails } from "@/components/vn/details/details"
import { Tags } from "@/components/vn/tags/tags"
import { api } from "@/lib/api"
import { notFound } from "next/navigation"
import type { VN, Character, Producer, Staff } from "@/lib/types"
import { Details } from "@/components/details"
import { Releases } from "@/components/vn/releases/releases"
import { log } from "console"

type ContentType = "vn" | "release" | "character" | "producer" | "staff"

function getContentType(id: string): ContentType | null {
  const firstChar = id.charAt(0).toLowerCase()
  const types: Record<string, ContentType> = {
    v: "vn",
    r: "release",
    c: "character",
    p: "producer",
    s: "staff",
  }
  return types[firstChar] || null
}

async function renderVNPage(vn: VN) {
  if (!vn) return null

  const hasImage = vn.image?.url
  const mainTitle = vn.titles?.find((t) => t.official && t.main)?.title

  const detailsData = {
    "Original Language": { value: vn.olang },
    "Release Date": { value: vn.released },
    Length: { value: vn.length && `${vn.length} hours (${vn.length_votes} votes)` },
    Rating: { value: vn.rating && `${vn.rating.toFixed(2)} (${vn.votecount} votes)` },
    Developers: { value: vn.developers?.map((dev) => dev.name).join(", ") },
    Links: { value: "Links" },
    Platforms: { value: "Platforms" },
  }

  const tags =
    vn.tags?.map((tag) => ({
      id: tag.id,
      name: tag.name,
      rating: tag.rating,
      spoiler: tag.spoiler,
      category: tag.category,
    })) || []

  const releaseIds = (vn.releases || [])
    .map((release) => release.id)
    .filter((id): id is string => typeof id === "string")
    .map((id) => id.slice(1))

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="max-w-5xl mx-auto space-y-6">
        <VNDetails
          image={hasImage ? vn.image!.url : undefined}
          title={vn.title}
          subtitle={mainTitle}
          titles={vn.titles}
          data={detailsData}
          description={vn.description}
          developers={vn.developers}
          relations={vn.relations}
          platforms={vn.platforms}
          links={vn.extlinks?.map((link) => ({ url: link.url || "", name: link.name || "" }))}
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
      </div>
    </div>
  )
}

async function renderCharacterPage(character: Character) {
  if (!character) return null

  const detailsData = {
    Name: {
      value: character.name && (
        <div className="space-y-0.5">
          <div>{character.name}</div>
          {character.original && <div className="text-white/60">{character.original}</div>}
        </div>
      ),
    },
    Aliases: { value: character.aliases?.join(", ") },
    Physical: {
      value: (character.height ||
        character.weight ||
        character.bust ||
        character.waist ||
        character.hips ||
        character.cup) && (
        <div className="grid grid-cols-2 gap-x-4 text-sm">
          {character.height && <div>Height: {character.height} cm</div>}
          {character.weight && <div>Weight: {character.weight} kg</div>}
          {character.bust && <div>Bust: {character.bust} cm</div>}
          {character.waist && <div>Waist: {character.waist} cm</div>}
          {character.hips && <div>Hips: {character.hips} cm</div>}
          {character.cup && <div>Cup: {character.cup}</div>}
        </div>
      ),
    },
  }

  return (
    <Details
      type="character"
      image={character.image?.url}
      title={character.name}
      data={detailsData}
      description={character.description}
    />
  )
}

async function renderProducerPage(producer: Producer) {
  if (!producer) return null

  const detailsData = {
    Name: {
      value: producer.name && (
        <div className="space-y-0.5">
          <div>{producer.name}</div>
          {producer.original && <div className="text-white/60">{producer.original}</div>}
        </div>
      ),
    },
    Aliases: { value: producer.aliases?.join(", ") },
    Language: { value: producer.lang },
    Type: { value: producer.type },
  }

  return <Details type="producer" title={producer.name} data={detailsData} description={producer.description} />
}

async function renderStaffPage(staff: Staff) {
  if (!staff) return null

  const detailsData = {
    Name: {
      value: staff.name && (
        <div className="space-y-0.5">
          <div>{staff.name}</div>
          {staff.original && <div className="text-white/60">{staff.original}</div>}
        </div>
      ),
    },
    Aliases: { value: staff.aliases?.map((alias) => alias.name).join(", ") },
    Gender: { value: staff.gender },
    Language: { value: staff.lang },
    Links: { value: "Links" },
  }

  return <Details type="staff" title={staff.name} data={detailsData} description={staff.description} />
}

export default async function DetailPage({ params }: { params: { id: string } }) {
  const contentType = getContentType(params.id)
  if (!contentType) {
    notFound()
  }

  const id = params.id.slice(1)

  try {
    let response
    switch (contentType) {
      case "vn":
        response = await api.vn(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderVNPage(response.results[0] as VN)

      case "character":
        response = await api.character(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderCharacterPage(response.results[0] as Character)

      case "producer":
        response = await api.producer(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderProducerPage(response.results[0] as Producer)

      case "staff":
        response = await api.staff(id, { size: "large" })
        if (!response?.results?.[0]) notFound()
        return await renderStaffPage(response.results[0] as Staff)

      default:
        notFound()
    }
  } catch (error) {
    console.error(`Error fetching ${contentType} data:`, error)
    notFound()
  }
}