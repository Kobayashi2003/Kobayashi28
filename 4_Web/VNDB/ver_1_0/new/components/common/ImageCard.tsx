import Image from "next/image"
import { ImageOff } from "lucide-react"

interface ImageCardProps {
  imageTitle?: string
  imageUrl?: string  
  imageDims?: [number, number]
  className?: string
}

export function ImageCard({ imageTitle, imageUrl, imageDims, className }: ImageCardProps) {
  return (
    <div className={`bg-[#0F2942]/80 hover:bg-[#0F2942] rounded-lg border border-white/10 overflow-hidden hover:scale-105 transition-transform duration-300 ease-in-out ${className}`}>
      {/* <div className="relative w-full bg-gray-200" style={{ aspectRatio: imageDims ? `${imageDims[0]}/${imageDims[1]}` : "0.85" }}> */}
      <div className="relative w-full bg-gray-200 aspect-[0.85]">
        {imageUrl ? (
          <Image src={imageUrl} alt={imageUrl} fill className="object-contain bg-[#0F2942]" />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <ImageOff className="h-12 w-12" />
          </div>
        )}
      </div>
      <div className="p-4 border-t border-white/10">
        <h2 className="font-semibold truncate text-white text-sm md:text-base">{imageTitle}</h2>
      </div>
    </div>
  )
}