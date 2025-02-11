'use client'

import { useState } from 'react'
import { api } from '@/lib/api'
import { VN } from '@/lib/types'

export default function SearchPage() {
  const [search, setSearch] = useState('')
  const [results, setResults] = useState<VN[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      const response = await api.vn('', { search, size: 'small' })
      setResults(response.results)
    } catch (err) {
      setError('An error occurred while fetching data')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Search Visual Novels</h1>
      <form onSubmit={handleSearch} className="mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Enter search term"
          className="border p-2 mr-2"
        />
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">
          Search
        </button>
      </form>

      {isLoading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {results.length > 0 && (
        <ul>
          {results.map((vn) => (
            <li key={vn.id} className="mb-2">
              <h2 className="font-semibold">{vn.title}</h2>
              <p>Released: {vn.released}</p>
              {vn.image && (
                <img
                  src={vn.image.url || "/placeholder.svg"}
                  alt={vn.title}
                  className="w-32 h-auto"
                />
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}