import Link from "next/link"
import { Row } from "@/components/row/Row"

interface Publisher {
  id: string
  name: string
  original?: string
}

interface PublishersRowProps {
  publishers: Publisher[]
}

export function PublishersRow({ publishers }: PublishersRowProps) {

  if (publishers.length === 0) return null

  return (
    <Row label="Publishers" value={
      <div className="flex flex-wrap gap-1 items-center">
        {publishers.map((pub, index) => (
          <div key={pub.id}>
            <Link href={`/${pub.id}`} className="text-blue-400 hover:text-blue-500 transition-colors">
              {pub.name}
            </Link>
            {index < publishers.length - 1 && <span className="px-1">&</span>}
          </div>
        ))}
      </div>
    } />
  )
}