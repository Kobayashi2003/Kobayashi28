import Image from "next/image"
import { ImageOff } from "lucide-react"

interface ImageCardProps {
  imageTitle?: string
  imageUrl?: string  
  imageDims?: [number, number]
}

export function ImageCard({ imageTitle, imageUrl, imageDims }: ImageCardProps) {
  return (
    <div className="rounded-lg border border-white/10 overflow-hidden transition-transform duration-300 ease-in-out hover:scale-105 text-white text-lg bg-[#0F2942]">
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
      <div className="p-4">
        <h2 className="font-semibold truncate">{imageTitle}</h2>
      </div>
    </div>
  )
}