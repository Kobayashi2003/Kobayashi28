import Link from "next/link"

interface Developer {
  id?: string
  name?: string
  original?: string
}

interface DevelopersProps {
  developers?: Developer[]
}

export function Developers({ developers }: DevelopersProps) {
  if (!developers?.length) return null

  return (
    <span className="text-white/90">
      {developers.map((dev, index) => (
        <span key={dev.id}>
          <Link href={`/${dev.id}`} className="hover:text-white transition-colors">
            {dev.name}
          </Link>
          {index < developers.length - 1 && <span className="px-1">&</span>}
        </span>
      ))}
    </span>
  )
}