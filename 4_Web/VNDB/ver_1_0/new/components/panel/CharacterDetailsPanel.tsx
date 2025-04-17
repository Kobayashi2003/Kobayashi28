import { Character } from "@/lib/types"
import { kMaxLength } from "buffer"

export function CharacterDetailsPanel({ character }: { character: Character }) {

  const mainTitle = character.name
  const subTitle = character.original || ""
  const image_url = character.image?.url
  const image_dims = character.image?.dims
  const image_sexual = character.image?.sexual
  const image_violence = character.image?.violence

  const birthdayMatch = typeof character.birthday === 'string' ? character.birthday.match(/(\d+)\D+(\d+)/) : null
  const birthdayMonth  = birthdayMatch && birthdayMatch[1]
  const birthdayDay = birthdayMatch && birthdayMatch[2]
  const birthday = (birthdayMonth && birthdayDay) &&
    new Date(`2000-${birthdayMonth.padStart(2, "0")}-${birthdayDay.padStart(2, "0")}`)
    .toLocaleDateString("en-US", {
      day: "numeric",
      month: "long",
    })


  return <div>CharacterDetailsPanel</div>
}

