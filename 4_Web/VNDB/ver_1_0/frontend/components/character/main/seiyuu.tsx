import Link from "next/link"
import type { Character } from "@/lib/types"

// Define props interface for the Seiyuu component
interface SeiyuuProps {
  seiyuu: NonNullable<Character["seiyuu"]>
}

// Seiyuu component to display voice actors
export function Seiyuu({ seiyuu }: SeiyuuProps) {
  // If there are no voice actors, don't render anything
  if (!seiyuu?.length) return null

  return (
    // Container for the list of voice actors with small vertical spacing
    <div className="space-y-0.5">
      {seiyuu
        // Sort voice actors alphabetically by name
        .sort((a, b) => (a.name || "").localeCompare(b.name || ""))
        // Map through sorted voice actors and create a div for each
        .map((va, index) => (
          <div 
            // Unique key for each voice actor element
            key={`${va.id}-${va.name}-${index}`} 
            // Flex container for voice actor name and note
            className="flex items-baseline gap-1"
          >
            {/* Link to voice actor's page */}
            <Link 
              href={`/${va.id}`} 
              className="text-[#88ccff] hover:text-white transition-colors"
            >
              {va.name}
            </Link>
            {/* Display voice actor's note if it exists */}
            {va.note && <span className="text-[#4488cc]">({va.note})</span>}
          </div>
        ))}
    </div>
  )
}