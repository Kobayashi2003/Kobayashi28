import { ImageCard } from "@/components/common/ImageCard"
import { TextCard } from "@/components/common/TextCard"

import { VN_Small, Release_Small, Character_Small, Producer_Small, Staff_Small, Tag_Small, Trait_Small } from "@/lib/types"

export function GenVNCard(vn: VN_Small, sexualLevel: "safe" | "suggestive" | "explicit", violenceLevel: "tame" | "violent" | "brutal", cardType: "image" | "text") {
  if (cardType === "text") {
    return <TextCard title={vn.title} />
  }
  const sexual = vn.image?.sexual || 0
  const violence = vn.image?.violence || 0
  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      const yellow = sexual > 1 && violence > 1 ? `text-yellow-800` : `text-yellow-400`
      return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={yellow} />
    }
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  return <ImageCard imageTitle={vn.title} imageUrl={vn.image?.thumbnail || vn.image?.url} imageDims={vn.image?.thumbnail_dims || vn.image?.dims} />
}

export function GenReleaseCard(release: Release_Small) {
  return <TextCard title={release.title} />
}

export function GenCharacterCard(character: Character_Small, sexualLevel: "safe" | "suggestive" | "explicit", violenceLevel: "tame" | "violent" | "brutal", cardType: "image" | "text") {
  if (cardType === "text") {
    return <TextCard title={character.name} />
  }
  const sexual = character.image?.sexual || 0
  const violence = character.image?.violence || 0
  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      const yellow = sexual > 1 && violence > 1 ? `text-yellow-800` : `text-yellow-400`
      return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor={yellow} />
    }
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  return <ImageCard imageTitle={character.name} imageUrl={character.image?.url} imageDims={character.image?.dims} />
}

export function GenProducerCard(producer: Producer_Small) {
  return <TextCard title={producer.name} />
}

export function GenStaffCard(staff: Staff_Small) {
  return <TextCard title={staff.name} />
}

export function GenTagCard(tag: Tag_Small) {
  return <TextCard title={tag.name} />
}

export function GenTraitCard(trait: Trait_Small) {
  return <TextCard title={trait.name} />
}
