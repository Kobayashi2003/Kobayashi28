"use client"
import type { Staff } from "@/lib/types"
import { LANGUAGES } from "@/lib/constants"
import { Row } from "./row"
import { Links } from "./links"

interface StaffDetailsProps {
  staff: Staff
}

const GenderDisplay: Record<string, string> = {
  m: "Male",
  f: "Female",
}

export function StaffDetails({ staff }: StaffDetailsProps) {
  const mainTitle = staff.name
  const originalName = staff.original

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
            <Row label="Gender" value={staff.gender ? GenderDisplay[staff.gender] : undefined} />
            <Row label="Language" value={staff.lang && LANGUAGES[staff.lang]} />
            <Row
              label="Aliases"
              value={
                staff.aliases?.length ? (
                  <div className="flex flex-wrap gap-2">
                    {staff.aliases.map((alias, index) => (
                      <span key={index} className="text-white/80">
                        {alias.name}
                        {alias.latin && ` (${alias.latin})`}
                        {alias.is_main && " (Main)"}
                      </span>
                    ))}
                  </div>
                ) : null
              }
            />
            <Row label="Links" value={<Links extlinks={staff.extlinks} />} />
          </div>

          {staff.description && (
            <div className="border-t border-white/10 pt-4">
              <h3 className="text-sm font-semibold text-white/90 mb-2">Description</h3>
              <p className="text-sm text-white/80 leading-relaxed break-words">{staff.description}</p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}