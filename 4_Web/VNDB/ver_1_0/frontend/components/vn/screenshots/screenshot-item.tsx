"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import type { VN } from "@/lib/types"
import { Dialog, DialogContent, DialogTrigger, DialogTitle, DialogClose } from "@/components/ui/dialog"
import { VisuallyHidden } from "@/components/ui/visually-hidden"
import { Button } from "@/components/ui/button"
import { RefreshCw, X } from 'lucide-react'

interface ScreenshotItemProps {
  screenshot: NonNullable<VN["screenshots"]>[number]
}

export function ScreenshotItem({ screenshot }: ScreenshotItemProps) {
  const [isThumbnailLoaded, setIsThumbnailLoaded] = useState(false)
  const [isThumbnailError, setIsThumbnailError] = useState(false)
  const [isFullImageLoaded, setIsFullImageLoaded] = useState(false)
  const [isFullImageError, setIsFullImageError] = useState(false)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [retryCount, setRetryCount] = useState(0)

  if (!screenshot.thumbnail || !screenshot.url) return null

  const aspectRatio = screenshot.thumbnail_dims ? screenshot.thumbnail_dims[0] / screenshot.thumbnail_dims[1] : 16 / 9
  const containerWidth = screenshot.thumbnail_dims ? Math.min(screenshot.thumbnail_dims[0], 320) : 320

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
      setIsFullImageError(false);
      setIsFullImageLoaded(false);
    }
  }, [isDialogOpen]);

  useEffect(() => {
    //This effect will always run, regardless of isDialogOpen
  }, []);


  return (
    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
      <DialogTrigger asChild>
        <button
          className="overflow-hidden rounded bg-black/50 transition-transform hover:scale-[1.02]"
          style={{ width: containerWidth, aspectRatio }}
        >
          <div className="relative h-full w-full">
            {!isThumbnailLoaded && !isThumbnailError && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-200">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-500"></div>
              </div>
            )}
            {isThumbnailError ? (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-200 text-gray-500">
                Failed to load thumbnail
              </div>
            ) : (
              <Image
                src={screenshot.thumbnail || "/placeholder.svg"}
                alt="Screenshot thumbnail"
                fill
                className={`object-contain transition-opacity duration-300 ${
                  isThumbnailLoaded ? "opacity-100" : "opacity-0"
                }`}
                sizes={`${containerWidth}px`}
                onLoad={handleThumbnailLoad}
                onError={handleThumbnailError}
              />
            )}
          </div>
        </button>
      </DialogTrigger>
      <DialogContent className="max-w-screen-lg bg-black/90 border-none p-0">
        <VisuallyHidden>
          <DialogTitle>Full-size Screenshot</DialogTitle>
        </VisuallyHidden>
        <div className="relative w-full" style={{ aspectRatio }}>
          {!isFullImageLoaded && !isFullImageError && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-200">
              <div className="h-12 w-12 animate-spin rounded-full border-4 border-gray-300 border-t-blue-500"></div>
            </div>
          )}
          {isFullImageError ? (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-200 text-gray-500">
              <p className="mb-4">Failed to load full-size image</p>
              <Button onClick={retryFullImage} variant="outline" className="mr-2">
                <RefreshCw className="mr-2 h-4 w-4" /> Retry
              </Button>
            </div>
          ) : (
            <Image
              key={retryCount} // Force re-render on retry
              src={screenshot.url || "/placeholder.svg"}
              alt="Full-size screenshot"
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
          <Button onClick={retryFullImage} size="icon" variant="outline">
            <RefreshCw className="h-4 w-4" />
          </Button>
          <DialogClose asChild>
            <Button size="icon" variant="outline">
              <X className="h-4 w-4" />
            </Button>
          </DialogClose>
        </div>
      </DialogContent>
    </Dialog>
  )
}