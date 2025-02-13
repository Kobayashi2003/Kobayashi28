import { api } from "@/lib/api"
import Image from "next/image"
import Link from "next/link"
import { notFound } from "next/navigation"

export default async function SearchResults({
  params,
  searchParams,
}: {
  params: { type: string }
  searchParams: { [key: string]: string | string[] | undefined }
}) {
  const { type } = params
  const validTypes = ["vn", "release", "character", "producer", "staff"]

  if (!validTypes.includes(type)) {
    notFound()
  }

  try {
    const apiFunction = api[type as keyof typeof api]
    if (typeof apiFunction !== "function") {
      throw new Error(`Invalid search type: ${type}`)
    }

    // Convert searchParams to a plain object with string values
    const queryParams = Object.fromEntries(
      Object.entries(searchParams).map(([key, value]) => [key, Array.isArray(value) ? value[0] : value]),
    )

    const response = await apiFunction("", queryParams)
    const results = response.results

    return (
      <div className="container mx-auto p-4">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-white">{results.length} Results Found</h1>
          </div>
          {results.length === 0 ? (
            <p className="text-white/60">No results found. Try adjusting your search criteria.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {results.map((item: any) => (
                <div key={item.id} className="bg-[#0F2942]/80 rounded-lg shadow-lg overflow-hidden">
                  {(type === "vn" || type === "character") && item.image?.url && (
                    <div className="relative h-48 w-full">
                      <Image
                        src={item.image.url || "/placeholder.svg"}
                        alt={item.title || item.name}
                        fill
                        className="object-cover"
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                      />
                    </div>
                  )}
                  <div className="p-4">
                    <Link href={`/${type[0]}${item.id}`} className="text-[#88ccff] hover:text-white transition-colors">
                      <h2 className="text-lg font-semibold truncate">{item.title || item.name}</h2>
                    </Link>
                    {type === "vn" && (
                      <div className="text-white/60 text-sm mt-1 space-y-1">
                        {item.released && <p>Released: {item.released}</p>}
                        {item.length && (
                          <p>Length: {typeof item.length === "number" ? `${item.length} hours` : item.length}</p>
                        )}
                        {item.rating && (
                          <p>
                            Rating: {item.rating.toFixed(2)} ({item.votecount} votes)
                          </p>
                        )}
                      </div>
                    )}
                    {type === "release" && (
                      <div className="text-white/60 text-sm mt-1 space-y-1">
                        {item.released && <p>Released: {item.released}</p>}
                        {item.languages?.length > 0 && <p>Languages: {item.languages.join(", ")}</p>}
                        {item.platforms?.length > 0 && <p>Platforms: {item.platforms.join(", ")}</p>}
                      </div>
                    )}
                    {type === "character" && (
                      <div className="text-white/60 text-sm mt-1 space-y-1">
                        {item.gender && <p>Gender: {item.gender}</p>}
                        {item.age && <p>Age: {item.age}</p>}
                        {item.height && <p>Height: {item.height}cm</p>}
                      </div>
                    )}
                    {type === "producer" && (
                      <div className="text-white/60 text-sm mt-1 space-y-1">
                        {item.type && <p>Type: {item.type}</p>}
                        {item.language && <p>Language: {item.language}</p>}
                      </div>
                    )}
                    {type === "staff" && (
                      <div className="text-white/60 text-sm mt-1 space-y-1">
                        {item.aliases?.length > 0 && <p>Also known as: {item.aliases.join(", ")}</p>}
                        {item.description && <p className="line-clamp-2">{item.description}</p>}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    )
  } catch (error) {
    console.error("Error fetching search results:", error)
    return (
      <div className="container mx-auto p-4">
        <div className="text-center space-y-4">
          <h1 className="text-2xl font-bold text-white">Error</h1>
          <p className="text-white/60">An error occurred while fetching the search results. Please try again.</p>
        </div>
      </div>
    )
  }
}

