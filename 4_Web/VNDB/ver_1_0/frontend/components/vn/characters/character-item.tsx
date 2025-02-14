import Link from "next/link"
import { cn } from "@/lib/utils"
import type { VN } from "@/lib/types"
import { CHARACTER_ICONS, CHARACTER_SEX_COLORS } from "@/lib/constants"

interface Character {
  id?: string;
  name?: string;
  sex?: [string, string];
  vns?: Array<{
    id?: string;
    role?: string;
    spoiler?: number;
  }>;
}

interface CharacterItemProps {
  vn: VN
  character: Character
}

const ROLE_DISPLAY: Record<string, string> = {
  primary: "Main character",
  side: "Side character",
  main: "Protagonist"
}

export function CharacterItem({ vn, character }: CharacterItemProps) {

  const apparentSex = character.sex?.[0] ?? ""
  const realSex = character.sex?.[1] ?? ""
  const role = character.vns?.find((v) => v.id === vn.id)?.role ?? ""
  const voiceActors = vn.va?.filter((va) => va.character?.id === character.id) ?? []

  return (
    <div className="space-y-1 border border-white/10 rounded p-2">
      {/* Character name and sex icon */}
      <div className="flex items-center gap-2">
        {apparentSex && (
          <span
            className={cn(
              CHARACTER_ICONS[apparentSex],
              CHARACTER_SEX_COLORS[apparentSex],
            )}
          />
        )}
        <Link href={`/${character.id}`} className="text-[#88ccff] hover:text-white transition-colors">
          {character.name}
        </Link>
        {role && <span className="text-[#4488cc] italic text-xs">{ROLE_DISPLAY[role] || role}</span>}
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