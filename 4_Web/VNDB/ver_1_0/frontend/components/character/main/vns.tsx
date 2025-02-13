import Link from "next/link"
import type { Character } from "@/lib/types"
import { ROLE } from "@/lib/constants"

interface VNsProps {
  vns: NonNullable<Character["vns"]>
}

export function VNs({ vns }: VNsProps) {
  // Group VNs by their title
  const groupedVNs = vns.reduce((groups, vn) => {
    const title = vn.title || "Unknown"
    if (!groups[title]) {
      groups[title] = []
    }
    groups[title].push(vn)
    return groups
  }, {} as Record<string, typeof vns>)

  return (
    <div className="space-y-4">
      {Object.entries(groupedVNs).map(([title, entries]) => (
        <div key={title} className="space-y-1">
          {/* Show VN title as a link if there are multiple releases */}
          {entries.length > 1 && (
            <Link href={`/${entries[0].id}`} className="text-[#88ccff] hover:text-white transition-colors block">
              {title}
            </Link>
          )}
          {/* Container for VN entries */}
          <div className={entries.length > 1 ? "ml-4 space-y-0.5" : ""}>
            {entries.map((vn) => (
              <div key={`${vn.id}-${vn.release?.id}`} className="flex items-baseline gap-1 text-sm">
                {/* Show bullet point for multiple entries */}
                {entries.length > 1 && <span className="text-[#4488cc]">›</span>}
                {/* Display character's role in the VN */}
                <span className="text-[#4488cc]">{ROLE[vn.role as keyof typeof ROLE] || vn.role}</span>
                {/* Display VN or release information */}
                {renderVNLink(vn, entries.length === 1 ? title : undefined)}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

// Helper function to render VN or release link
function renderVNLink(vn: Character["vns"][number], singleTitle?: string) {
  if (singleTitle) {
    return (
      <>
        <span className="text-[#4488cc]">-</span>
        <Link href={`/${vn.id}`} className="text-[#88ccff] hover:text-white transition-colors">
          {singleTitle}
        </Link>
      </>
    )
  }
  if (vn.release) {
    return (
      <>
        <span className="text-[#4488cc]">-</span>
        <Link href={`/${vn.release.id}`} className="text-[#88ccff] hover:text-white transition-colors">
          {vn.release.title}
        </Link>
      </>
    )
  }
  return <span className="text-[#88ccff]">- All other releases</span>
}