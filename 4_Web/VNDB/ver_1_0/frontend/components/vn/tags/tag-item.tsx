import { cn } from "@/lib/utils"
import { SIZES } from "@/lib/constants"

// Props for the TagItem component
interface TagProps {
  name: string
  rating?: number
  spoiler?: number
  category?: string
  href?: string
  separator?: boolean
}

// Component for rendering individual tags
export function TagItem({ name, rating, spoiler, category, href, separator = true }: TagProps) {
  // Determine the text size based on the rating
  const getTagSize = (rating?: number) => {
    if (!rating) return SIZES.xs
    if (rating < 1) return SIZES.xs
    if (rating < 2) return SIZES.sm
    if (rating < 3) return SIZES.base
    return SIZES.lg
  }

  // Tag content
  const content = (
    <>
      <span
        className={cn(
          getTagSize(rating),
          "transition-all duration-200 ease-in-out",
          spoiler === 0 && "text-[#88ccff] hover:text-[#aaddff]",
          spoiler === 1 && "text-[#ffcc66] hover:text-[#ffdd88]",
          spoiler === 2 && "text-[#ff6666] hover:text-[#ff8888]",
          spoiler ? "opacity-100" : "opacity-100",
          "hover:scale-110",
        )}
      >
        {name}
      </span>
      {rating !== undefined && (
        <span className="text-xs text-[#6699cc] ml-1 transition-all duration-200 ease-in-out hover:text-[#88bbee]">
          {rating.toFixed(1)}
        </span>
      )}
      {separator && <span className="text-[#88ccff] mx-2 opacity-50">·</span>}
    </>
  )

  // Render as a link if href is provided, otherwise as a span
  if (href) {
    return (
      <a
        href={href}
        className="hover:underline inline-block transform transition-transform duration-200 ease-in-out hover:scale-105"
      >
        {content}
      </a>
    )
  }

  return <span className="inline-block">{content}</span>
}