"use client"
import type { Producer } from "@/lib/types"
import { LANGUAGES } from "@/lib/constants"
import { Row } from "./row"
import { Links } from "./links"

interface ProducerDetailsProps {
  producer: Producer
}

const TypeDisplay: Record<string, string> = {
  co: "Company",
  in: "Individual",
  ng: "Amateur Group",
}

export function ProducerDetails({ producer }: ProducerDetailsProps) {
  const mainTitle = producer.name
  const originalName = producer.original

  return (
    <>
      {/* Header section with title */}
      {mainTitle && (
        <div className="p-4 border-b border-white/10">
          <div className="max-w-3xl pl-2">
            <div className="text-lg text-white/90">{mainTitle}</div>
            {originalName && <div className="text-sm text-white/60">{originalName}</div>}
          </div>
        </div>
      )}

      {/* Main content */}
      <div className="p-6">
        <div className="space-y-4 min-w-0">
          <div className="grid gap-2">
            <Row label="Type" value={producer.type ? TypeDisplay[producer.type] : undefined} />
            <Row label="Primary Language" value={producer.lang && LANGUAGES[producer.lang]} />
            <Row
              label="Aliases"
              value={
                producer.aliases?.length ? (
                  <div className="flex flex-wrap gap-2">
                    {producer.aliases.map((alias, index) => (
                      <span key={index} className="text-white/80">
                        {alias}
                      </span>
                    ))}
                  </div>
                ) : null
              }
            />
            <Row label="Links" value={<Links extlinks={producer.extlinks} />} />
          </div>

          {producer.description && (
            <div className="border-t border-white/10 pt-4">
              <h3 className="text-sm font-semibold text-white/90 mb-2">Description</h3>
              <p className="text-sm text-white/80 leading-relaxed break-words">{producer.description}</p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}