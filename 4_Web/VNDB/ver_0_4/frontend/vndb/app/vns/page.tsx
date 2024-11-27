import Link from 'next/link'
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

// This is a mock data, replace it with actual API call in a real application
const vns = [
  { id: 'v1', title: 'Steins;Gate' },
  { id: 'v2', title: 'Clannad' },
  { id: 'v3', title: 'Fate/stay night' },
]

export default function VNsIndex() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold mb-8">Visual Novels</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {vns.map((vn) => (
          <Card key={vn.id}>
            <CardHeader>
              <CardTitle>{vn.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <Link href={`/vns/${vn.id}`} className="text-blue-500 hover:underline">
                View Details
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

