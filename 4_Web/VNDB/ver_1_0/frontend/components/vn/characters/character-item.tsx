import Link from "next/link"
import { cn } from "@/lib/utils"
import type { VN } from "@/lib/types"
import { SEX_ICONS, SEX_COLORS, ROLE } from "@/lib/constants"

interface CharacterItemProps {
  id?: string
  name?: string
  sex?: string[]
  role?: string
  vn: VN
}

export function CharacterItem({ id, name, sex, role, vn }: CharacterItemProps) {
  // Use first (apparent) sex for the icon
  const sexValue = sex?.[0]

  // Find voice actors for this character
  const voiceActors = vn.va?.filter((va) => va.character?.id === id) || []

  return (
    <div className="space-y-1 border border-white/10 rounded p-2">
      {/* Character name and sex icon */}
      <div className="flex items-center gap-2">
        {sexValue && (
          <span
            className={cn(
              SEX_ICONS[sexValue as keyof typeof SEX_ICONS],
              SEX_COLORS[sexValue as keyof typeof SEX_COLORS],
            )}
          />
        )}
        <Link href={`/${id}`} className="text-[#88ccff] hover:text-white transition-colors">
          {name}
        </Link>
        {role && <span className="text-[#4488cc] italic text-xs">{ROLE[role as keyof typeof ROLE] || role}</span>}
      </div>
      {/* Voice actors section */}
      {voiceActors.length > 0 && (
        <div className="pl-6 text-xs">
          <div className="space-y-0.5">
            {voiceActors.map((va, index) => (
              <div key={`${va.staff?.id}-${index}`} className="flex items-baseline gap-1">
                <span className="text-white/60">Voiced by</span>
                <Link href={`/${va.staff?.id}`} className="text-[#88ccff] hover:text-white transition-colors">
                  {va.staff?.name}
                </Link>
                {va.note && <span className="text-[#4488cc]">({va.note})</span>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}