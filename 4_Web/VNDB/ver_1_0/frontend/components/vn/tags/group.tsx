import { TagItem } from "./tag"

// Props for the Group component
interface GroupProps {
  tags: Array<{
    id?: string
    name?: string
    rating?: number
    spoiler?: number
    category?: string
  }>
  showLowRated?: boolean
  selectedCategories?: string[]
  maxSpoilerLevel?: number
}

// Component for grouping and filtering tags
export function Group({ tags, showLowRated = true, selectedCategories = [], maxSpoilerLevel = 0 }: GroupProps) {
  if (!tags?.length) return null

  // Filter and sort tags based on criteria
  const filteredTags = tags
    .filter((tag) => {
      if (!showLowRated && (tag.rating || 0) < 1) return false
      if ((tag.spoiler || 0) > maxSpoilerLevel) return false
      if (selectedCategories.length > 0 && tag.category && !selectedCategories.includes(tag.category)) return false
      return true
    })
    .sort((a, b) => (b.rating || 0) - (a.rating || 0))

  if (!filteredTags.length) return null

  return (
    <div className="flex flex-wrap items-center">
      {filteredTags.map((tag, index) => (
        <TagItem
          key={tag.id || tag.name}
          name={tag.name || ""}
          rating={tag.rating}
          spoiler={tag.spoiler}
          category={tag.category}
          href={tag.id ? `/tags/${tag.id}` : undefined}
          separator={index < filteredTags.length - 1}
        />
      ))}
    </div>
  )
}