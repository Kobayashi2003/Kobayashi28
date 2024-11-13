'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Trash2 } from 'lucide-react'

interface Bookmark {
  id: number
  name: string
  host: string
  route: string
  method: string
  params: string
  body: string
  created_at: string
}

interface BookmarksProps {
  host: string
  onLoadBookmark: (bookmark: Bookmark) => void
}

export default function Bookmarks({ host, onLoadBookmark }: BookmarksProps) {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchBookmarks()
  }, [host])

  const fetchBookmarks = async () => {
    try {
      const res = await fetch(`${host}/api/bookmarks`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      setBookmarks(data);
      setError(null);
    } catch (error) {
      console.error('Error fetching bookmarks:', error);
      setError(`Error fetching bookmarks: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  const deleteBookmark = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent triggering the card click
    try {
      const res = await fetch(`${host}/api/bookmarks/${id}`, {
        method: 'DELETE',
      });
      if (res.ok) {
        fetchBookmarks();
      } else {
        throw new Error('Failed to delete bookmark');
      }
    } catch (error) {
      console.error('Error deleting bookmark:', error);
      setError(`Error deleting bookmark: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Bookmarks</h2>
      {bookmarks.map((bookmark) => (
        <Card 
          key={bookmark.id} 
          className="p-4 hover:bg-accent transition-colors cursor-pointer"
          onClick={() => onLoadBookmark(bookmark)}
        >
          <CardContent className="p-0">
            <div className="flex justify-between items-center">
              <div className="flex-grow">
                <div className="font-bold">{bookmark.name || `${bookmark.method} ${bookmark.route}`}</div>
                <div className="text-sm text-muted-foreground">
                  {bookmark.name && `${bookmark.method} ${bookmark.route}`}
                </div>
                <div className="text-sm text-muted-foreground">
                  {bookmark.host}
                </div>
                <div className="text-sm text-muted-foreground">
                  {new Date(bookmark.created_at).toLocaleString()}
                </div>
              </div>
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={(e) => deleteBookmark(bookmark.id, e)}
                className="ml-2"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
      {bookmarks.length === 0 && !error && (
        <div className="text-muted-foreground text-sm">No bookmarks found.</div>
      )}
      {error && (
        <div className="text-destructive text-sm mt-2">
          {error}
        </div>
      )}
    </div>
  )
}