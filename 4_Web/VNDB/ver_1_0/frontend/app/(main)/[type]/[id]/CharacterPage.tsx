import { Character } from "@/lib/types"

import { CharacterDetailsPanel } from "@/components/panel/CharacterDetailsPanel"

interface CharacterPageProps {
  character: Character
}

export default function CharacterPage({ character }: CharacterPageProps) {
  return (
    <div>
      <CharacterDetailsPanel character={character} />
    </div>
  )
}
