import { Details, ExternalLinkButton } from "@/components/details"
import { api } from "@/lib/api"
import { notFound } from "next/navigation"
import type React from "react"
import type { VN, Release, Character, Producer, Staff, VisualNovelDataBaseQueryResponse } from "@/lib/types"

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

function groupTraitsByCategory(traits: Array<{ id?: string; name?: string; group_name?: string }> | undefined) {
  if (!traits) return new Map()

  return traits.reduce((groups, trait) => {
    if (trait.name && trait.group_name) {
      const group = groups.get(trait.group_name) || []
      group.push(trait.name)
      groups.set(trait.group_name, group)
    }
    return groups
  }, new Map<string, string[]>())
}

export default async function DetailPage({ params }: { params: { id: string } }) {
  const contentType = getContentType(params.id)
  if (!contentType) {
    notFound()
  }

  const id = params.id.slice(1)
  let data: VisualNovelDataBaseQueryResponse<VN | Release | Character | Producer | Staff>
  let detailsData: Record<string, { value: React.ReactNode }>

  switch (contentType) {
    case "vn":
      data = await api.vn(id, { size: "large" })
      const vn = data.results[0] as VN
      detailsData = {
        Titles: {
          value: vn.title && (
            <div className="space-y-0.5">
              <div>{vn.title}</div>
              {vn.alttitle && <div className="text-white/60">{vn.alttitle}</div>}
            </div>
          ),
        },
        Aliases: { value: vn.aliases?.join(", ") },
        "Original Language": { value: vn.olang },
        "Release Date": { value: vn.released },
        Length: { value: vn.length && `${vn.length} hours (${vn.length_votes} votes)` },
        Rating: { value: vn.rating && `${vn.rating.toFixed(2)} (${vn.votecount} votes)` },
        Developers: { value: vn.developers?.map((dev) => dev.name).join(", ") },
        Links: {
          value: vn.extlinks && (
            <div className="flex flex-wrap gap-2">
              {vn.extlinks.map((link) => (
                <ExternalLinkButton key={link.url} href={link.url}>
                  {link.name}
                </ExternalLinkButton>
              ))}
            </div>
          ),
        },
      }
      break

    case "character":
      data = await api.character(id, { size: "large" })
      const character = data.results[0] as Character
      const traitGroups = groupTraitsByCategory(character.traits)

      detailsData = {
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
        Traits: {
          value: traitGroups.size > 0 && (
            <div className="space-y-2">
              {Array.from(traitGroups.entries()).map(([groupName, traits]) => (
                <div key={groupName}>
                  <div className="text-white/80">{groupName}</div>
                  <div className="text-white/60 text-sm">{traits.join(", ")}</div>
                </div>
              ))}
            </div>
          ),
        },
        Appearances: {
          value: character.vns?.length && (
            <div className="space-y-1">
              {character.vns.map((vn) => (
                <div key={vn.id} className="flex items-center gap-2 text-sm">
                  <span className="text-white/80">{vn.title}</span>
                  {vn.role && <span className="text-white/60">({vn.role})</span>}
                </div>
              ))}
            </div>
          ),
        },
      }
      break

    case "producer":
      data = await api.producer(id, { size: "large" })
      const producer = data.results[0] as Producer
      detailsData = {
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
      break

    case "staff":
      data = await api.staff(id, { size: "large" })
      const staff = data.results[0] as Staff
      detailsData = {
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
        Links: {
          value: staff.extlinks?.length && (
            <div className="flex flex-wrap gap-2">
              {staff.extlinks.map((link) => (
                <ExternalLinkButton key={link.url} href={link.url}>
                  {link.name}
                </ExternalLinkButton>
              ))}
            </div>
          ),
        },
      }
      break

    default:
      notFound()
  }

  if (!data?.results?.[0]) {
    notFound()
  }

  const result = data.results[0]
  const hasImage = (contentType === "vn" || contentType === "character") && "image" in result && result.image?.url

  return (
    <Details
      type={contentType}
      image={hasImage ? result.image!.url : undefined}
      data={detailsData}
      description={"description" in result ? result.description : "notes" in result ? result.notes : undefined}
    />
  )
}

