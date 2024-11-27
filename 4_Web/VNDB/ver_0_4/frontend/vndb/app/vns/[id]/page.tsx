'use client'

import { useParams } from 'next/navigation'
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export default function VNInfo() {
  const params = useParams()
  const vnId = params.id

  // In a real application, you would fetch the VN data based on the ID
  // For now, we'll just display the ID
  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Visual Novel Details</CardTitle>
        </CardHeader>
        <CardContent>
          <p>VN ID: {vnId}</p>
          {/* Add more VN details here */}
        </CardContent>
      </Card>
    </div>
  )
}

