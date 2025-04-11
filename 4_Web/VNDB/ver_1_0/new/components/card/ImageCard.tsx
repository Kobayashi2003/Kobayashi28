"use client"


import { useEffect, useState } from "react"
import Image from "next/image"
import { cn } from "@/lib/utils"
import { ImageOff, RotateCw, RefreshCw } from "lucide-react"

interface ImageCardProps {
  title: string
  url: string
  dims?: [number, number]
  msgs?: string[]
  link?: string
  className?: string
}

export function ImageCard({ title, url, dims, msgs, link, className }: ImageCardProps) {

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [imgUrl, setImgUrl] = useState(url)

  useEffect(() => {
    setLoading(true)
    setError(false)
    setImgUrl(url)
  }, [url])

  const handleRetry = (e: React.MouseEvent) => {
    e.stopPropagation()
    setLoading(true)
    setError(false)
    setImgUrl(`${url}?${Date.now()}`)
  }

  const handleCardClick = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (link) {
      window.location.href = link
    }
  }

  // Card container styles
  const containerStyle = cn(
    "bg-[#0F2942]/80 hover:bg-[#0F2942]",
    "rounded-lg",
    "p-2",
    "border border-white/10",
    "hover:scale-105 transition-transform duration-300",
    link ? "cursor-pointer" : "cursor-default",
    className
  )

  // Image area styles
  const imageWrapperStyle = "relative w-full aspect-square"
  const imageContentStyle = cn(
    "object-contain transition-opacity duration-300",
    loading || error ? "opacity-0" : "opacity-100"
  )
  const iconWrapperStyle = "absolute inset-0 flex items-center justify-center"
  const iconStyle = "h-12 w-12"

  // Text area styles
  const textWrapperStyle = "w-full p-2 border-t border-white/10"
  const titleTextStyle = "truncate font-semibold text-xs sm:text-sm md:text-base"
  const msgTextStyle = "truncate text-xs md:text-sm text-gray-400"

  return (
    <div 
      className={cn(containerStyle)}
      onClick={handleCardClick}
    >
      <div className={cn(imageWrapperStyle)}>
        {imgUrl ? (<>
          <Image
            src={imgUrl}
            alt={imgUrl}
            fill
            loading="lazy"
            onLoad={() => {setLoading(false); setError(false)}}
            onError={() => {setLoading(false); setError(true)}}
            className={cn(imageContentStyle)}
          />
          {error && (
            <div onClick={handleRetry} className={cn(iconWrapperStyle)}>
              <RefreshCw className={cn(iconStyle, "text-red-400")} />
            </div>
          )}
          {loading && (
            <div className={cn(iconWrapperStyle)}>
              <RotateCw className={cn(iconStyle, "text-gray-500 animate-spin")} />
            </div>
          )}
        </>) : (
          <div className={cn(iconWrapperStyle)}>
            <ImageOff className={cn(iconStyle)} />
          </div>
        )}
      </div>
      <div className={cn(textWrapperStyle)}>
        <h2 className={cn(titleTextStyle)}>{title}</h2>
        {msgs?.filter(Boolean).map((msg, index) => (
          <p key={index} className={cn(msgTextStyle)}>{msg}</p>
        ))}
      </div>
    </div>    
  )
}