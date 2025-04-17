import Link from "next/link"
import { Row } from "@/components/row/Row"
import { ExternalLink } from "lucide-react"
import { divide } from "lodash"

interface ExtLink {
  url: string
  label: string
  name: string
  id: string
}

interface ExtlinksRowProps {
  extlinks: ExtLink[]
}

export function ExtlinksRow({ extlinks }: ExtlinksRowProps) {

  if (extlinks.length === 0) return null

  return (
    <Row label="External Links" value={
      <div className="flex flex-wrap gap-1 items-center">
        {extlinks.map((extlink) => (
          <Link href={extlink.url} key={extlink.id} 
            className="flex gap-1 items-center text-blue-400 hover:text-blue-500 transition-colors">
            {extlink.label}
            <ExternalLink className="h-3 w-3 text-white" />
          </Link>
        ))}
      </div>
    } />
  )
}
