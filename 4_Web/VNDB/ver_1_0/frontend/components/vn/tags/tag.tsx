import { cn } from "@/lib/utils"

interface TagProps {
  name: string
  rating?: number
  spoiler?: number
  category?: string
  href?: string
  separator?: boolean
}

const RATING_SIZES = {
  xs: "text-xs",
  sm: "text-sm",
  base: "text-base",
  lg: "text-lg",
}

export function Tag({ name, rating, spoiler, category, href, separator = true }: TagProps) {
  const getRatingSize = (rating?: number) => {
    if (!rating) return RATING_SIZES.xs
    if (rating < 1) return RATING_SIZES.xs
    if (rating < 2) return RATING_SIZES.sm
    if (rating < 3) return RATING_SIZES.base
    return RATING_SIZES.lg
  }

  const content = (
    <>
      <span
        className={cn(
          getRatingSize(rating),
          "transition-colors duration-200",
          spoiler === 0 && "text-[#88ccff]",
          spoiler === 1 && "text-[#ffcc66]",
          spoiler === 2 && "text-[#ff6666]",
          spoiler ? "opacity-100" : "opacity-100",
        )}
      >
        {name}
      </span>
      {rating !== undefined && <span className="text-xs text-[#6699cc] ml-1">{rating.toFixed(1)}</span>}
      {separator && <span className="text-[#88ccff] mx-2">·</span>}
    </>
  )

  if (href) {
    return (
      <a href={href} className="hover:underline">
        {content}
      </a>
    )
  }

  return <span>{content}</span>
}