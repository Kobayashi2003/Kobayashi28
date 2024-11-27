import Link from 'next/link'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold mb-8">VN Database</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Visual Novels</CardTitle>
            <CardDescription>Browse all visual novels</CardDescription>
          </CardHeader>
          <CardContent>
            <Link href="/vns" className="text-blue-500 hover:underline">
              View VNs
            </Link>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Characters</CardTitle>
            <CardDescription>Explore characters from various VNs</CardDescription>
          </CardHeader>
          <CardContent>
            <Link href="/characters" className="text-blue-500 hover:underline">
              View Characters
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}