import Link from "next/link"
import type { Character } from "@/lib/types"

interface SeiyuuProps {
  seiyuu: NonNullable<Character["seiyuu"]>
}

export function Seiyuu({ seiyuu }: SeiyuuProps) {
  if (!seiyuu?.length) return null

  return (
    <div className="grid grid-cols-[100px_1fr] gap-2 items-start text-sm">
      <span className="text-white/60 font-medium shrink-0">Voiced by</span>
      <div className="space-y-0.5">
        {seiyuu
          .sort((a, b) => (a.name || "").localeCompare(b.name || ""))
          .map((va, index) => (
            <div key={`${va.id}-${va.name}-${index}`} className="flex items-baseline gap-1">
              <Link href={`/${va.id}`} className="text-[#88ccff] hover:text-white transition-colors">
                {va.name}
              </Link>
              {va.note && <span className="text-[#4488cc]">({va.note})</span>}
            </div>
          ))}
      </div>
    </div>
  )
}