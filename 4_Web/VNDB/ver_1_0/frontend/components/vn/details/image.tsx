import Image from "next/image"

// Props for the VNImage component
interface VNImageProps {
  src?: string // Source URL for the image
  alt?: string // Alternative text for the image
}

// Component to display the visual novel cover image
export function VNImage({ src, alt }: VNImageProps) {
  // If no source is provided, don't render anything
  if (!src) return null

  return (
    <div className="flex flex-col items-center">
      <div className="bg-transparent p-1 rounded-sm">
        {/* Container for the image with fixed dimensions */}
        <div className="relative w-[250px] aspect-[3/4]">
          {/* Next.js Image component for optimized image loading */}
          <Image src={src || "/placeholder.svg"} alt={alt || "Cover"} fill className="object-contain" sizes="250px" />
        </div>
      </div>
    </div>
  )
}