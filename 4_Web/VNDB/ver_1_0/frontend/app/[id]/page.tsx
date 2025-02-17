import { Suspense } from "react"
import { notFound } from "next/navigation"
import { api } from "@/lib/api"
import type {
  VN as VNType,
  Release as ReleaseType,
  Character as CharacterType,
  Producer as ProducerType,
  Staff as StaffType,
  Tag as TagType,
  Trait as TraitType,
  VisualNovelDataBaseQueryResponse,
} from "@/lib/types"

import { VNDetails } from "@/components/vn/main/details"
import { VNTags } from "@/components/vn/tags/tags"
import { VNStaff } from "@/components/vn/staff/staff"
import { VNReleases } from "@/components/vn/releases/releases"
import { VNCharacters } from "@/components/vn/characters/characters"
import { VNScreenshots } from "@/components/vn/screenshots/screenshots"
import { CharacterDetails } from "@/components/character/main/details"
import { ProducerDetails } from "@/components/producer/main/detials"
import { ProducerVNs } from "@/components/producer/vns/vns"
import { StaffDetails } from "@/components/staff/main/details"
import { StaffCredits } from "@/components/staff/credits/credits"
import { Loader2 } from "lucide-react"

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
    i: "trait",
  }
  return types[firstChar] || null
}

function LoadingComponent() {
  return (
    <div className="flex justify-center items-center h-screen">
      <Loader2 className="h-16 w-16 animate-spin text-white" />
    </div>
  )
}

function renderVNPage(vn: VNType) {
  const containerClass = "container max-w-5xl mx-auto space-y-6 px-4 py-6"
  const sectionClass = "bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden"
  const headerClass = "p-4 text-white/90 text-lg font-semibold"

  return (
    <div className={containerClass}>
      {vn && (
        <div className={sectionClass}>
          <VNDetails vn={vn} />
        </div>
      )}
      {vn.tags && vn.tags.length > 0 && (
        <div className={sectionClass}>
          <div className={headerClass}>
            <h3>Tags</h3>
          </div>
          <div className="p-4">
            <VNTags vn={vn} />
          </div>
        </div>
      )}
      {vn.releases && vn.releases.length > 0 && (
        <div className={sectionClass}>
          <div className={headerClass}>
            <h3>Releases</h3>
          </div>
          <div className="p-4">
            <Suspense fallback={<div>Loading releases...</div>}>
              <VNReleases vn={vn} />
            </Suspense>
          </div>
        </div>
      )}
      {vn.characters && vn.characters.length > 0 && (
        <div className={sectionClass}>
          <div className={headerClass}>
            <h3>Characters</h3>
          </div>
          <div className="p-4">
            <VNCharacters vn={vn} />
          </div>
        </div>
      )}
      {vn.staff && vn.staff.length > 0 && (
        <div className={sectionClass}>
          <div className={headerClass}>
            <h3>Staff</h3>
          </div>
          <div className="p-4">
            <VNStaff vn={vn} />
          </div>
        </div>
      )}
      {vn.screenshots && vn.screenshots.length > 0 && (
        <div className={sectionClass}>
          <div className={headerClass}>
            <h3>Screenshots</h3>
          </div>
          <div className="p-4">
            <VNScreenshots vn={vn} />
          </div>
        </div>
      )}
    </div>
  )
}

function renderReleasepage(release: ReleaseType) {
  // Implementation pending
  return null
}

function renderCharacterPage(character: CharacterType) {
  const containerClass = "container max-w-5xl mx-auto space-y-6 px-4 py-6"
  const sectionClass = "bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden"

  return (
    <div className={containerClass}>
      {character && (
        <div className={sectionClass}>
          <CharacterDetails character={character} />
        </div>
      )}
    </div>
  )
}

function renderProducerPage(producer: ProducerType) {
  const containerClass = "container max-w-5xl mx-auto space-y-6 px-4 py-6"
  const sectionClass = "bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden"
  const headerClass = "p-4 text-white/90 text-lg font-semibold"

  return (
    <div className={containerClass}>
      {producer && (
        <div className={sectionClass}>
          <ProducerDetails producer={producer} />
        </div>
      )}
      {producer && (
        <div className={sectionClass}>
          <div className={headerClass}>
            <h3>Visual Novels</h3>
          </div>
          <div className="p-4">
            <ProducerVNs producer={producer} />
          </div>
        </div>
      )}
    </div>
  )
}

function renderStaffPage(staff: StaffType) {
  const containerClass = "container max-w-5xl mx-auto space-y-6 px-4 py-6"
  const sectionClass = "bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 overflow-hidden"
  const headerClass = "p-4 text-white/90 text-lg font-semibold"

  return (
    <div className={containerClass}>
      {staff && (
        <div className={sectionClass}>
          <StaffDetails staff={staff} />
        </div>
      )}
      {staff && (
        <div className={sectionClass}>
          <div className={headerClass}>
            <h3>Credits</h3>
          </div>
          <StaffCredits staff={staff} />
        </div>
      )}
    </div>
  )
}

function renderTagPage(tag: TagType) {
  // Implementation pending
  return null
}

function renderTraitPage(trait: TraitType) {
  // Implementation pending
  return null
}

async function fetchData(contentType: ContentType, id: string) {
  let response: VisualNovelDataBaseQueryResponse<VNType | ReleaseType | CharacterType | ProducerType | StaffType>

  try {
    switch (contentType) {
      case "vn":
        response = await api.vn(id, { size: "large" })
        break
      case "release":
        response = await api.release(id, { size: "large" })
        break
      case "character":
        response = await api.character(id, { size: "large" })
        break
      case "producer":
        response = await api.producer(id, { size: "large" })
        break
      case "staff":
        response = await api.staff(id, { size: "large" })
        break
      case "tag":
        response = await api.tag(id, { size: "large" })
        break
      case "trait":
        response = await api.trait(id, { size: "large" })
        break
      default:
        throw new Error("Invalid content type")
    }

    if (!response?.results?.[0]) {
      notFound()
    }

    return response.results[0]
  } catch (error) {
    console.error(`Error fetching ${contentType} data:`, error)
    throw error
  }
}

async function AsyncDetailContent({ contentType, id }: { contentType: ContentType; id: string }) {
  try {
    const data = await fetchData(contentType, id)
    switch (contentType) {
      case "vn":
        return renderVNPage(data as VNType)
      case "release":
        return renderReleasepage(data as ReleaseType)
      case "character":
        return renderCharacterPage(data as CharacterType)
      case "producer":
        return renderProducerPage(data as ProducerType)
      case "staff":
        return renderStaffPage(data as StaffType)
      case "tag":
        return renderTagPage(data as TagType)
      case "trait":
        return renderTraitPage(data as TraitType)
      default:
        notFound()
    }
  } catch (error) {
    console.error(`Error rendering ${contentType} content:`, error)
    notFound()
  }
}

export default async function DetailPage({ params }: { params: { id: string } }) {
  const id = params.id
  const contentType = getContentType(id)

  if (!contentType) {
    notFound()
  }

  const cleanId = id.slice(1)

  return (
    <Suspense fallback={<LoadingComponent />}>
      <AsyncDetailContent contentType={contentType} id={cleanId} />
    </Suspense>
  )
}