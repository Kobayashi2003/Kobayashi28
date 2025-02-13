"use client"

import Image from "next/image"
import type { VN } from "@/lib/types"
import { VisuallyHidden } from "@/components/ui/visually-hidden"
import { Dialog, DialogContent, DialogTrigger, DialogTitle } from "@/components/ui/dialog"

interface ScreenshotItemProps {
  screenshot: NonNullable<VN["screenshots"]>[number]
}

export function ScreenshotItem({ screenshot }: ScreenshotItemProps) {
  if (!screenshot.thumbnail || !screenshot.url) return null

  // Calculate aspect ratio and container width
  const aspectRatio = screenshot.thumbnail_dims ? screenshot.thumbnail_dims[0] / screenshot.thumbnail_dims[1] : 16 / 9
  const containerWidth = screenshot.thumbnail_dims ? Math.min(screenshot.thumbnail_dims[0], 320) : 320

  return (
    <Dialog>
      <DialogTrigger asChild>
        <button
          className="overflow-hidden rounded bg-black/50 transition-transform hover:scale-[1.02]"
          style={{ width: containerWidth, aspectRatio }}
        >
          <div className="relative h-full w-full">
            <Image
              src={screenshot.thumbnail || "/placeholder.svg"}
              alt="Screenshot thumbnail"
              fill
              className="object-contain"
              sizes={`${containerWidth}px`}
            />
          </div>
        </button>
      </DialogTrigger>
      <DialogContent className="max-w-screen-lg bg-black/90 border-none p-0">
        <VisuallyHidden>
          <DialogTitle>Full-size Screenshot</DialogTitle>
        </VisuallyHidden>
        <div className="relative w-full" style={{ aspectRatio }}>
          <Image
            src={screenshot.url || "/placeholder.svg"}
            alt="Full-size screenshot"
            fill
            className="object-contain"
            sizes="100vw"
            priority
          />
        </div>
      </DialogContent>
    </Dialog>
  )
}