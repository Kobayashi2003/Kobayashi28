import Image from "next/image"
import type { Character } from "@/lib/types"

interface CharacterImageProps {
  image?: Character["image"]
  alt?: string
}

export function CharacterImage({ image, alt }: CharacterImageProps) {
  if (!image?.url) return null

  return (
    <div className="flex flex-col items-center">
      <div className="bg-transparent p-1 rounded-sm">
        <div className="relative w-[250px] aspect-[3/4]">
          <Image
            src={image.url || "/placeholder.svg"}
            alt={alt || "Character"}
            fill
            className="object-contain"
            sizes="250px"
          />
        </div>
      </div>
    </div>
  )
}