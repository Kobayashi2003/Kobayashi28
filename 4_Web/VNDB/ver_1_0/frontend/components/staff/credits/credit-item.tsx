import Image from "next/image"
import Link from "next/link"
import type { VN } from "@/lib/types"

interface CreditItemProps {
  vn: VN
}

export function CreditItem({ vn }: CreditItemProps) {
  return (
    <Link href={`/${vn.id}`} className="block group">
      <div className="bg-[#0F2942] rounded-lg overflow-hidden shadow-lg transition-all duration-300 ease-in-out group-hover:shadow-xl group-hover:scale-105">
        <div className="relative w-full" style={{ paddingBottom: "133.33%" }}>
          {vn.image?.url ? (
            <Image
              src={vn.image.url || "/placeholder.svg"}
              alt={vn.title || "Visual Novel Cover"}
              layout="fill"
              objectFit="cover"
              loading="lazy"
              className="transition-transform duration-300 ease-in-out group-hover:scale-110"
            />
          ) : (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-200 text-gray-500">No image</div>
          )}
        </div>
        <div className="p-4 transition-colors duration-300 ease-in-out group-hover:bg-[#1A3A5A]">
          <h3 className="text-lg font-semibold text-white mb-2 truncate">{vn.title}</h3>
          {vn.released && (
            <p className="text-sm text-white/60 transition-colors duration-300 ease-in-out group-hover:text-white/80">
              Released: {vn.released}
            </p>
          )}
        </div>
      </div>
    </Link>
  )
}