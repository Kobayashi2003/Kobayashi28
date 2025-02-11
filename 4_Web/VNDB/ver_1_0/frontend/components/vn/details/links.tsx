import { ExternalLink } from "lucide-react"

interface Link {
  url: string
  name: string
}

interface LinksProps {
  links?: Link[]
}

export function Links({ links }: LinksProps) {
  if (!links || links.length === 0) return null

  return (
    <div className="flex flex-wrap gap-2">
      {links.map((link) => (
        <a
          key={link.url}
          href={link.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-blue-400 hover:text-blue-300 transition-colors text-sm"
        >
          {link.name}
          <ExternalLink className="h-3 w-3" />
        </a>
      ))}
    </div>
  )
}