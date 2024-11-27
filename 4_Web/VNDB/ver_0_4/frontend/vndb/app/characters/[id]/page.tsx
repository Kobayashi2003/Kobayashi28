'use client'

import { useParams } from 'next/navigation'
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export default function CharacterInfo() {
  const params = useParams()
  const characterId = params.id

  // In a real application, you would fetch the character data based on the ID
  // For now, we'll just display the ID
  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Character Details</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Character ID: {characterId}</p>
          {/* Add more character details here */}
        </CardContent>
      </Card>
    </div>
  )
}

