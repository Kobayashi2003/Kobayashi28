"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { Dialog, DialogContent, DialogTrigger, DialogTitle, DialogClose } from "@/components/ui/dialog"
import { VisuallyHidden } from "@/components/ui/visually-hidden"
import { Button } from "@/components/ui/button"
import { RefreshCw, X } from 'lucide-react'

interface CharacterImageProps {
  image: {
    url: string
  }
  name: string
}

export function CharacterImage({ image, name }: CharacterImageProps) {
  const [isThumbnailLoaded, setIsThumbnailLoaded] = useState(false)
  const [isThumbnailError, setIsThumbnailError] = useState(false)
  const [isFullImageLoaded, setIsFullImageLoaded] = useState(false)
  const [isFullImageError, setIsFullImageError] = useState(false)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [retryCount, setRetryCount] = useState(0)

  const handleThumbnailLoad = () => setIsThumbnailLoaded(true)
  const handleThumbnailError = () => {
    setTimeout(() => setIsThumbnailError(true), 10000) // 10 seconds timeout
  }
  const handleFullImageLoad = () => setIsFullImageLoaded(true)
  const handleFullImageError = () => {
    setTimeout(() => setIsFullImageError(true), 15000) // 15 seconds timeout
  }

  const retryFullImage = () => {
    setIsFullImageError(false)
    setIsFullImageLoaded(false)
    setRetryCount(retryCount + 1)
  }

  useEffect(() => {
    if (isDialogOpen) {
      setIsFullImageError(false)
      setIsFullImageLoaded(false)
    }
  }, [isDialogOpen])

  return (
    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
      <DialogTrigger asChild>
        <button className="overflow-hidden rounded transition-transform hover:scale-[1.02] bg-[#0F2942]/80">
          <div className="relative w-[250px] aspect-[3/4]">
            {!isThumbnailLoaded && !isThumbnailError && (
              <div className="absolute inset-0 flex items-center justify-center bg-[#0F2942]">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-white/20 border-t-white/80"></div>
              </div>
            )}
            {isThumbnailError ? (
              <div className="absolute inset-0 flex items-center justify-center bg-[#0F2942] text-white/60">
                Failed to load image
              </div>
            ) : (
              <Image
                src={image.url || "/placeholder.svg"}
                alt={name || "Character"}
                fill
                className={`object-contain transition-opacity duration-300 ${
                  isThumbnailLoaded ? "opacity-100" : "opacity-0"
                }`}
                sizes="250px"
                onLoad={handleThumbnailLoad}
                onError={handleThumbnailError}
              />
            )}
          </div>
        </button>
      </DialogTrigger>
      <DialogContent className="max-w-screen-lg bg-[#0F2942]/95 border-none p-0">
        <VisuallyHidden>
          <DialogTitle>Full-size Character Image</DialogTitle>
        </VisuallyHidden>
        <div className="relative w-full aspect-[3/4]">
          {!isFullImageLoaded && !isFullImageError && (
            <div className="absolute inset-0 flex items-center justify-center bg-[#0F2942]">
              <div className="h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white/80"></div>
            </div>
          )}
          {isFullImageError ? (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-[#0F2942] text-white/60">
              <p className="mb-4">Failed to load full-size image</p>
              <Button onClick={retryFullImage} variant="outline" className="mr-2">
                <RefreshCw className="mr-2 h-4 w-4" /> Retry
              </Button>
            </div>
          ) : (
            <Image
              key={retryCount}
              src={image.url || "/placeholder.svg"}
              alt={name || "Full-size character image"}
              fill
              className={`object-contain transition-opacity duration-300 ${
                isFullImageLoaded ? "opacity-100" : "opacity-0"
              }`}
              sizes="100vw"
              priority
              onLoad={handleFullImageLoad}
              onError={handleFullImageError}
            />
          )}
        </div>
        <div className="absolute top-2 right-2 flex space-x-2">
          <Button onClick={retryFullImage} size="icon" variant="outline" className="bg-[#0F2942]/80 hover:bg-[#0F2942]">
            <RefreshCw className="h-4 w-4" />
          </Button>
          <DialogClose asChild>
            <Button size="icon" variant="outline" className="bg-[#0F2942]/80 hover:bg-[#0F2942]">
              <X className="h-4 w-4" />
            </Button>
          </DialogClose>
        </div>
      </DialogContent>
    </Dialog>
  )
}