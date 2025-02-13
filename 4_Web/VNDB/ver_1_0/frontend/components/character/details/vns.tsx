import Link from "next/link"
import type { Character } from "@/lib/types"
import { ROLE } from "@/lib/constants"

interface VNsProps {
  vns: NonNullable<Character["vns"]>
}

// Map role values to display text

export function VNs({ vns }: VNsProps) {
  // Group VNs by their title
  const groupedVNs = vns.reduce(
    (groups, vn) => {
      const title = vn.title || "Unknown"
      if (!groups[title]) {
        groups[title] = []
      }
      groups[title].push(vn)
      return groups
    },
    {} as Record<string, typeof vns>,
  )

  return (
    <div className="space-y-4">
      {Object.entries(groupedVNs).map(([title, entries]) => (
        <div key={title} className="space-y-1">
          {/* Show VN title if there are multiple releases */}
          {entries.length > 1 && (
            <Link href={`/v${entries[0].id}`} className="text-[#88ccff] hover:text-white transition-colors block">
              {title}
            </Link>
          )}
          <div className={entries.length > 1 ? "ml-4 space-y-0.5" : ""}>
            {entries.map((vn) => (
              <div key={`${vn.id}-${vn.release?.id}`} className="flex items-baseline gap-1 text-sm">
                {entries.length > 1 && <span className="text-[#4488cc]">›</span>}
                <span className="text-[#4488cc]">{ROLE[vn.role as keyof typeof ROLE] || vn.role}</span>
                {entries.length === 1 ? (
                  <>
                    <span className="text-[#4488cc]">-</span>
                    <Link href={`/v${vn.id}`} className="text-[#88ccff] hover:text-white transition-colors">
                      {title}
                    </Link>
                  </>
                ) : vn.release ? (
                  <>
                    <span className="text-[#4488cc]">-</span>
                    <Link href={`/r${vn.release.id}`} className="text-[#88ccff] hover:text-white transition-colors">
                      {vn.release.title}
                    </Link>
                  </>
                ) : (
                  <span className="text-[#88ccff]">- All other releases</span>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}