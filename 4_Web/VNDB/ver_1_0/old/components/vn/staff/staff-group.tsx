"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import { ChevronRight } from "lucide-react"
import { StaffItem } from "./staff-item"

interface Staff {
  id?: string;
  name?: string;
  eid?: number;
  role?: string;
  note?: string;
}

interface StaffGroupProps {
  editionName: string
  staffList: Staff[]
}

function getRoleDisplay(role: string) {
  if (role === "art") return "Artist" 
  if (role === "music") return "Composer" 
  if (role === "songs") return "Vocals" 
  if (role === "chardesign") return "Character Design" 
  return role
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ")
}

export function StaffGroup({ editionName, staffList }: StaffGroupProps) {
  const [isExpanded, setIsExpanded] = useState(editionName === "Original edition")

  const staffByRole = staffList.reduce(
    (groups, member) => {
      const role = member.role || "Other"
      if (!groups[role]) {
        groups[role] = []
      }
      groups[role].push(member)
      return groups
    },
    {} as Record<string, typeof staffList>,
  )

  return (
    <div>
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full text-left p-2 bg-[#0F2942] hover:bg-[#1A3A5A] transition-colors flex items-center gap-2 group"
      >
        <ChevronRight className={cn("h-4 w-4 text-[#88ccff] transition-transform", isExpanded && "rotate-90")} />
        <span className="text-white font-semibold">{editionName}</span>
      </button>

      {isExpanded && (
        <div className="pl-6 py-2">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-4">
            {Object.entries(staffByRole).map(([role, members]) => (
              <div key={role} className="min-w-[200px] break-inside-avoid">
                <div className="text-white font-semibold text-base mb-2">{getRoleDisplay(role)}</div>
                <div className="space-y-1 text-sm">
                  {members.map((member) => (
                    <StaffItem key={`${member.id}-${member.role}-${member.note}`} staff={member} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}