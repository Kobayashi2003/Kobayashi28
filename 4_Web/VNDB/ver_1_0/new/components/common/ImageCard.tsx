"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { ImageOff, RotateCw, RefreshCw } from "lucide-react"

interface ImageCardProps {
  imageTitle?: string
  imageSubtitle?: string
  imageUrl?: string  
  imageDims?: [number, number]
  textColor?: string
  className?: string
}

export function ImageCard({ imageTitle, imageSubtitle, imageUrl, imageDims, textColor, className }: ImageCardProps) {
  const [isLoading, setIsLoading] = useState(true)
  const [isError, setIsError] = useState(false)

  useEffect(() => {
    setIsLoading(true);
    setIsError(false);
  }, [imageUrl]);

  const handleRetry = () => {
    // TODO: Implement retry
  }

  return (
    <div className={`bg-[#0F2942]/80 hover:bg-[#0F2942] rounded-lg border border-white/10 overflow-hidden hover:scale-105 transition-transform duration-300 ease-in-out ${className}`}>
      {/* <div className="relative w-full bg-gray-200" style={{ aspectRatio: imageDims ? `${imageDims[0]}/${imageDims[1]}` : "0.85" }}> */}
      <div className="relative w-full aspect-[0.85]">
        {imageUrl ? (<>
          {isLoading && (
            <div className="absolute inset-0 flex items-center justify-center z-10">
              <RotateCw className="h-12 w-12 animate-spin" />
            </div>
          )}
          {isError && (
            <div onClick={handleRetry} className={`absolute inset-0 flex items-center justify-center ${textColor || "text-red-400"}`}>
              <RefreshCw className="h-12 w-12" />
            </div>
          )}
          <Image 
            src={imageUrl} 
            alt={imageUrl} 
            fill 
            loading="lazy"
            className={`object-contain transition-opacity duration-300 ease-in-out ${isLoading || isError ? "opacity-0" : "opacity-100"}`}
            onLoad={() => { setIsLoading(false); setIsError(false) }}
            onError={() => { setIsLoading(false); setIsError(true) }}
          />
        </>) : (
          <div className={`absolute inset-0 flex items-center justify-center ${textColor || "text-gray-500"}`}>
            <ImageOff className="h-12 w-12" />
          </div>
        )} 
      </div>
      <div className="p-4 border-t border-white/10">
        <h2 className={`font-semibold truncate text-sm md:text-base ${textColor || "text-white"}`}>{imageTitle}</h2>
        {imageSubtitle && (
          <p className="text-xs md:text-sm text-gray-400">{imageSubtitle}</p>
        )}
      </div>
    </div>
  )
}