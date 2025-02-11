"use client"

import type React from "react"
import { cn } from "@/lib/utils"
import { Row } from "./row"
import { VNImage } from "./image"
import { Titles } from "./titles"
import { Links } from "./links"
import { Platforms } from "./platforms"
import { Relations } from "./relations"
import { Developers } from "./developers"

interface VNDetailsProps {
  image?: string
  title?: string
  subtitle?: string
  description?: string
  platforms?: string[]
  titles?: Array<{
    lang?: string
    title?: string
    latin?: string
    official?: boolean
    main?: boolean
  }>
  developers?: Array<{
    id?: string
    name?: string
    original?: string
  }>
  relations?: Array<{
    id?: string
    relation?: string
    title?: string
    official?: boolean
  }>
  links?: Array<{
    url: string
    name: string
  }>
  data: Record<
  string,
  {
    value: React.ReactNode
    icon?: React.ReactNode
    className?: string
  }>
}

export function VNDetails({
  image,
  title,
  subtitle,
  titles,
  data,
  description,
  developers,
  relations,
  platforms,
  links,
}: VNDetailsProps) {
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
          <VNImage src={image} alt={title} />

          {/* Details Section */}
          <div className="space-y-4 min-w-0">
            {titles && titles.length > 0 && (
              <div className="pb-4 border-b border-white/10">
                <Titles titles={titles} mainTitle={title} />
              </div>
            )}

            <div className="grid gap-2">
              {Object.entries(data).map(([key, { value, icon, className }]) => {
                if (key === "Developers") {
                  return <Row key={key} label={key} value={<Developers developers={developers} />} />
                }
                if (key === "Platforms") {
                  return <Row key={key} label={key} value={<Platforms platforms={platforms} />} />
                }
                if (key === "Links") {
                  return <Row key={key} label={key} value={<Links links={links} />} />
                }
                return <Row key={key} label={key} value={value} icon={icon} className={className} />
              })}
            </div>

            {relations && relations.length > 0 && (
              <div className="border-t border-white/10 pt-4">
                <h3 className="text-sm font-semibold text-white/90 mb-2">Relations</h3>
                <Relations relations={relations} />
              </div>
            )}

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