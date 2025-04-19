"use client"

import { useState, useEffect } from "react"
import NextImage from "next/image"
import { cn } from "@/lib/utils"
import { Dialog, DialogContent, DialogTrigger, DialogTitle } from "@/components/ui/dialog"
import { DownloadButton } from "@/components/button/DownloadButton"
import { ReloadButton } from "@/components/button/ReloadButton"
import { CancelButton } from "@/components/button/CancelButton"
import { ImageOff, RotateCw, RefreshCw } from "lucide-react"

interface ImageProps {
  url: string
  thumbnail?: string
  image_dims?: [number, number]
  thumbnail_dims?: [number, number]
}

export function Image({ url, thumbnail, image_dims, thumbnail_dims }: ImageProps) {

  const [thumbnailUrl, setThumbnailUrl] = useState(thumbnail || url)
  const [fullImageUrl, setFullImageUrl] = useState(url)
  const [thumbnailAspectRatio, setThumbnailAspectRatio] = useState(
    thumbnail_dims ? thumbnail_dims[0] / thumbnail_dims[1] : 
    image_dims ? image_dims[0] / image_dims[1] : 3 / 4
  )
  const [fullImageAspectRatio, setFullImageAspectRatio] = useState(
    image_dims ? image_dims[0] / image_dims[1] : 3 / 4
  )

  const [isThumbnailLoaded, setIsThumbnailLoaded] = useState(false)
  const [isThumbnailError, setIsThumbnailError] = useState<string | null>(null)
  const [isFullImageLoaded, setIsFullImageLoaded] = useState(false)
  const [isFullImageError, setIsFullImageError] = useState<string | null>(null)
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  const handleThumbnailRetry = () => {
    setIsThumbnailError(null)
    setIsThumbnailLoaded(false)
    setThumbnailUrl(`${thumbnail || url}?${Date.now()}`)
  }

  const handleFullImageRetry = () => {
    setIsFullImageError(null)
    setIsFullImageLoaded(false)
    setFullImageUrl(`${url}?${Date.now()}`)
  }

  const handleDownload = () => {
    const a = document.createElement("a")
    a.href = fullImageUrl
    a.download = fullImageUrl.split("/").pop() || "image.png"
    a.click()
  }

  useEffect(() => {
    setIsThumbnailLoaded(false)
    setIsThumbnailError(null)
    setIsFullImageLoaded(false)
    setIsFullImageError(null)
    setThumbnailUrl(`${thumbnail || url}?${Date.now()}`)
    setFullImageUrl(`${url}?${Date.now()}`)
    setThumbnailAspectRatio(
      thumbnail_dims ? thumbnail_dims[0] / thumbnail_dims[1] : 
      image_dims ? image_dims[0] / image_dims[1] : 1
    )
    setFullImageAspectRatio(
      image_dims ? image_dims[0] / image_dims[1] : 1
    )
  }, [url, thumbnail, image_dims, thumbnail_dims])

  return (
    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
      <DialogTrigger asChild disabled={!thumbnail}>
        <div className={cn("relative w-full bg-[#0F2942]/80 select-none")} style={{
          aspectRatio: thumbnailAspectRatio
        }}>
          {thumbnail ? (<>
            <NextImage
              src={thumbnailUrl}
              alt={thumbnailUrl}
              fill
              loading="lazy"
              onLoad={() => setIsThumbnailLoaded(true)}
              onError={() => setIsThumbnailError(null)}
              className={cn(
                "object-contain transition-opacity duration-300",
                !isThumbnailLoaded || isThumbnailError ? "opacity-0" : "opacity-100"
              )}
            />
            {isThumbnailError && (
              <div 
                onClick={(e) => {
                  e.stopPropagation();
                  handleThumbnailRetry();
                }} 
                className={cn(
                  "absolute inset-0 flex flex-col items-center justify-center gap-4",
                )}
              >
                <RefreshCw className={cn(
                  "h-12 w-12 text-red-400"
                )} />
                <p className="text-red-400/90 text-sm">
                  Error: {isThumbnailError}
                </p>
              </div>
            )}
            {!isThumbnailLoaded && (
              <div className={cn(
                "absolute inset-0 flex items-center justify-center"
              )}>
                <RotateCw className={cn(
                  "h-12 w-12 text-gray-500 animate-spin"
                )} />
              </div>
            )}
          </>) : (
            <div className={cn(
              "absolute inset-0 flex items-center justify-center"
            )}>
              <ImageOff className={cn(
                "h-12 w-12 text-gray-500"
              )} />
            </div>
          )}
        </div>
      </DialogTrigger>
      <DialogContent className={cn(
        "max-w-screen-lg bg-[#0F2942]/80 p-0 select-none"
      )}>
        <DialogTitle className="hidden">
          Full-size Image
        </DialogTitle>
        <div className={cn("relative w-full")} style={{
          aspectRatio: fullImageAspectRatio
        }}>
          <NextImage
            src={fullImageUrl}
            alt={fullImageUrl}
            fill
            loading="lazy"
            onLoad={() => setIsFullImageLoaded(true)}
            onError={() => setIsFullImageError(null)}
            className={cn(
              "object-contain transition-opacity duration-300",
              !isFullImageLoaded || isFullImageError ? "opacity-0" : "opacity-100"
            )}
          />
          {isFullImageError && (
            <div onClick={handleFullImageRetry} className={cn(
              "absolute inset-0 flex flex-col items-center justify-center gap-4"
            )}>
              <RefreshCw className={cn(
                "h-12 w-12 text-red-400"
              )} />
              <p className="text-red-400/90 text-sm">
                Error: {isFullImageError}
              </p>
            </div>
          )}
          {!isFullImageLoaded && (
            <div className={cn(
              "absolute inset-0 flex items-center justify-center"
            )}>
              <RotateCw className={cn(
                "h-12 w-12 text-gray-500 animate-spin"
              )} />
            </div>
          )}
          <div className={cn(
            "absolute top-2 right-2 flex flex-row gap-2"
          )}>
            <DownloadButton handleDownload={handleDownload} className="
              bg-[#0F2942]/80 hover:bg-[#0F2942]
            "/>
            <ReloadButton handleReload={handleFullImageRetry} className="
              bg-[#0F2942]/80 hover:bg-[#0F2942]
            "/>
            <CancelButton handleCancel={() => setIsDialogOpen(false)} className="
              bg-[#0F2942]/80 hover:bg-[#0F2942]
            "/>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}