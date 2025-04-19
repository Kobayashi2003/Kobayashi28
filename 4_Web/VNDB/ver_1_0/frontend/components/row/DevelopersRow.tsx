import Link from "next/link"
import { Row } from "@/components/row/Row"

interface Developer {
  id: string
  name: string
  original?: string
}

interface DevelopersRowProps {
  developers: Developer[]
}

export function DevelopersRow({ developers }: DevelopersRowProps) {

  if (developers.length === 0) return null

  return (
    <Row label="Developers" value={
      <div className="flex flex-wrap gap-1 items-center">
        {developers.map((dev, index) => (
          <div key={dev.id}>
            <Link href={`/${dev.id}`} className="text-blue-400 hover:text-blue-500 transition-colors">
              {dev.name}
            </Link>
            {index < developers.length - 1 && <span className="px-1">&</span>}
          </div>
        ))}
      </div>
    } />
  )
}