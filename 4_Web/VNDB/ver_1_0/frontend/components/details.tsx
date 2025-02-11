"use client"

import Image from "next/image"
import Link from "next/link"
import { ExternalLink } from "lucide-react"
import { cn } from "@/lib/utils"
import type React from "react"

interface DetailsProps {
  type: "vn" | "release" | "character" | "producer" | "staff"
  image?: string
  data: Record<
    string,
    {
      value: React.ReactNode
      icon?: React.ReactNode
      className?: string
    }
  >
  description?: string
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

export function Details({ type, image, data, description }: DetailsProps) {
  return (
    <div className="container mx-auto px-4 py-6">
      <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 max-w-5xl mx-auto overflow-hidden">
        <div className={cn("grid gap-6 p-6", image ? "md:grid-cols-[250px_1fr]" : "grid-cols-1")}>
          {/* Image Section - Only render if image is provided */}
          {image && (
            <div className="flex justify-center">
              <div className="relative w-full max-w-[250px] aspect-[3/4] rounded-lg overflow-hidden border border-white/10">
                <Image src={image || "/placeholder.svg"} alt="Cover" fill className="object-cover" sizes="250px" />
              </div>
            </div>
          )}

          {/* Details Section */}
          <div className="space-y-4">
            <div className="grid gap-2">
              {Object.entries(data).map(([key, { value, icon, className }]) => {
                // Skip rendering if value is empty
                if (!value || (typeof value === "string" && !value.trim())) return null

                return (
                  <div key={key} className="grid grid-cols-[120px_1fr] gap-4 items-start text-sm break-words">
                    <span className="text-white/60 font-medium">{key}</span>
                    <div className={cn("text-white/90 min-w-0", className)}>
                      {icon && <span className="mr-2">{icon}</span>}
                      {value}
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

