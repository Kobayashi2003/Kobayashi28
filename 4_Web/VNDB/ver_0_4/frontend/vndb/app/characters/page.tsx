import Link from 'next/link'
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

// This is a mock data, replace it with actual API call in a real application
const characters = [
  { id: 'c1', name: 'Okabe Rintarou' },
  { id: 'c2', name: 'Makise Kurisu' },
  { id: 'c3', name: 'Shirou Emiya' },
]

export default function CharactersIndex() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold mb-8">Characters</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {characters.map((character) => (
          <Card key={character.id}>
            <CardHeader>
              <CardTitle>{character.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <Link href={`/characters/${character.id}`} className="text-blue-500 hover:underline">
                View Details
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

