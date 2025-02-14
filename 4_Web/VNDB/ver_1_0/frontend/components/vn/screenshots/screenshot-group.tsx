import Link from "next/link"
import { ScreenshotItem } from "./screenshot-item"

interface Screenshot {
  url?: string;
  dims?: [number, number]
  sexual?: number;
  violence?: number;
  thumbnail?: string;
  thumbnail_dims?: [number, number];
  release?: {
    id?: string;
    title?: string;
  }
}

interface ScreenshotGroupProps {
  releaseId: string
  title: string
  screenshots: Screenshot[]
}

export function ScreenshotGroup({ title, screenshots, releaseId }: ScreenshotGroupProps) {
  return (
    <div className="space-y-3">
      <Link href={`/${releaseId}`} className="block text-center">
        <h3 className="text-white font-bold hover:text-[#88ccff] transition-colors">{title}</h3>
      </Link>
      <div className="flex flex-wrap justify-center gap-1">
        {screenshots.map((screenshot, index) => (
          <ScreenshotItem key={index} screenshot={screenshot} />
        ))}
      </div>
    </div>
  )
}