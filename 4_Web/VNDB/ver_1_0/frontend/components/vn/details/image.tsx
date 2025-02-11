import Image from "next/image"

interface VNImageProps {
  src?: string
  alt?: string
}

export function VNImage({ src, alt }: VNImageProps) {
  if (!src) return null

  return (
    <div className="flex flex-col items-center">
      <div className="bg-transparent p-1 rounded-sm">
        <div className="relative w-[250px] aspect-[3/4]">
          <Image src={src || "/placeholder.svg"} alt={alt || "Cover"} fill className="object-contain" sizes="250px" />
        </div>
      </div>
    </div>
  )
}

