import { cn } from "@/lib/utils"
import type { Tag } from "@/lib/types"

interface TagProps {
  rating: number
  spoiler: number
  tag: Tag
}

export function TagItem({ tag, rating, spoiler }: TagProps) {

  const getTagSize = (rating: number) => {
    if (rating < 1) return "text-xs"
    if (rating < 2) return "text-sm"
    if (rating < 3) return "text-base"
    return "text-lg"
  }

  const getTagColor = (spoiler: number) => {
    if (spoiler === 0) return "text-[#88ccff] hover:text-[#aaddff]"
    if (spoiler === 1) return "text-[#ffcc66] hover:text-[#ffdd88]"
    if (spoiler === 2) return "text-[#ff6666] hover:text-[#ff8888]"
    return null
  }

  return (
    <a
      href={`${tag.id}`}
      className="hover:underline inline-block transform transition-transform duration-200 ease-in-out hover:scale-105"
    >
      <span
        className={cn(
          getTagSize(rating),
          getTagColor(spoiler),
          "transition-all duration-200 ease-in-out",
          "opacity-100",
          "hover:scale-110",
        )}
      >
        {tag.name}
      </span>
      {rating !== undefined && (
        <span className="text-xs text-[#6699cc] ml-1 transition-all duration-200 ease-in-out hover:text-[#88bbee]">
          {rating.toFixed(1)}
        </span>
      )}
    </a>
  )
}