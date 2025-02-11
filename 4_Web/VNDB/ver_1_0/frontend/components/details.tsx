"use client"

import Image from "next/image"
import Link from "next/link"
import { ExternalLink } from "lucide-react"
import { cn } from "@/lib/utils"
import type React from "react"
import { Titles } from "./vn/details/titles"
import { Developers } from "./vn/details/developers"

interface DetailsProps {
  type: "vn" | "release" | "character" | "producer" | "staff"
  image?: string
  title?: string
  subtitle?: string
  titles?: Array<{
    lang?: string
    title?: string
    latin?: string
    official?: boolean
    main?: boolean
  }>
  data: Record<
    string,
    {
      value: React.ReactNode
      icon?: React.ReactNode
      className?: string
    }
  >
  description?: string
  developers?: Array<{
    id?: string
    name?: string
    original?: string
  }>
}

export function ExternalLinkButton({ href, children }: { href?: string; children: React.ReactNode }) {
  if (!href) return null

  return (
    <Link
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1 text-blue-400 hover:text-blue-300 transition-colors text-sm"
    >
      {children}
      <ExternalLink className="h-3 w-3" />
    </Link>
  )
}

export function Details({ type, image, title, subtitle, titles, data, description, developers }: DetailsProps) {
  return (
    <div className="container mx-auto px-4 py-6">
      <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 max-w-5xl mx-auto overflow-hidden">
        {/* Header with title and subtitle */}
        {(title || subtitle) && (
          <div className="p-4 border-b border-white/10">
            <div className="max-w-3xl pl-2">
              <div className="text-lg text-white/90">{title}</div>
              {subtitle && <div className="text-sm text-white/60">{subtitle}</div>}
            </div>
          </div>
        )}

        {/* Main content */}
        <div className={cn("grid gap-6 p-6", image ? "md:grid-cols-[250px_1fr]" : "grid-cols-1")}>
          {/* Image Section */}
          {image && (
            <div className="flex flex-col items-center">
              <div className="bg-black p-1 rounded-sm">
                <div className="relative w-[250px] aspect-[3/4]">
                  <Image src={image || "/placeholder.svg"} alt="Cover" fill className="object-contain" sizes="250px" />
                </div>
              </div>
            </div>
          )}

          {/* Details Section */}
          <div className="space-y-4 min-w-0">
            {titles && titles.length > 0 && (
              <div className="pb-4 border-b border-white/10">
                <Titles titles={titles} mainTitle={title} />
              </div>
            )}

            <div className="grid gap-2">
              {Object.entries(data).map(([key, { value, icon, className }]) => {
                if (!value && key !== "Developers") return null

                return (
                  <div key={key} className="grid grid-cols-[120px_1fr] gap-4 items-start text-sm">
                    <span className="text-white/60 font-medium shrink-0">{key}</span>
                    <div className={cn("text-white/90 min-w-0 break-words", className)}>
                      {icon && <span className="mr-2">{icon}</span>}
                      {key === "Developers" ? <Developers developers={developers} /> : value}
                    </div>
                  </div>
                )
              })}
            </div>

            {description && (
              <div className="border-t border-white/10 pt-4">
                <h3 className="text-sm font-semibold text-white/90 mb-2">Description</h3>
                <p className="text-sm text-white/80 leading-relaxed break-words">{description}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

