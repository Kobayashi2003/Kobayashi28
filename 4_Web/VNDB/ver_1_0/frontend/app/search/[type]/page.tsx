import { Suspense } from "react"
import { Loader2 } from "lucide-react"
import { api } from "@/lib/api"
import type {
  SearchType,
  ResourceType,
  VisualNovelDataBaseQueryParams,
  VisualNovelDataBaseQueryResponse,
} from "@/lib/types"
import { SearchResults } from "@/components/search/search-results"

interface SearchPageProps {
  params: { type: SearchType }
  searchParams: Record<string, string | string[] | undefined>
}

async function AsyncSearchResults({
  type,
  searchParams,
}: {
  type: SearchType
  searchParams: Record<string, string | string[] | undefined>
}) {
  const currentPage = Number.parseInt(searchParams.page as string, 10) || 1
  const itemsPerPage = 20 // You can adjust this value as needed

  const apiParams: VisualNovelDataBaseQueryParams = {
    count: true,
    size: "small",
    page: currentPage,
    limit: itemsPerPage,
  }

  Object.entries(searchParams).forEach(([key, value]) => {
    if (typeof value === "string") {
      switch (key) {
        case "sort":
          apiParams.sort = value
          break
        case "order":
          apiParams.reverse = value === "desc"
          break
        default:
          // For other parameters, add them directly to apiParams
          apiParams[key] = value
      }
    } else if (Array.isArray(value)) {
      // Handle array values (e.g., for multiple selections)
      apiParams[key] = value.join(",")
    }
  })

  try {
    let response: VisualNovelDataBaseQueryResponse<ResourceType>
    switch (type) {
      case "vn":
        response = await api.vn("", apiParams)
        break
      case "release":
        response = await api.release("", apiParams)
        break
      case "character":
        response = await api.character("", apiParams)
        break
      case "producer":
        response = await api.producer("", apiParams)
        break
      case "staff":
        response = await api.staff("", apiParams)
        break
      case "tag":
        response = await api.tag("", apiParams)
        break
      case "trait":
        response = await api.trait("", apiParams)
        break
      default:
        throw new Error(`Invalid search type: ${type}`)
    }
    return <SearchResults type={type} response={response} currentPage={currentPage} itemsPerPage={itemsPerPage} />
  } catch (error) {
    console.error("Error fetching search results:", error)
    return (
      <SearchResults
        type={type}
        response={{ results: [], more: false, count: 0, status: "ERROR" }}
        currentPage={currentPage}
        itemsPerPage={itemsPerPage}
      />
    )
  }
}

function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center h-64">
      <Loader2 className="h-12 w-12 animate-spin text-white" />
    </div>
  )
}

export default async function SearchPage({ params, searchParams }: SearchPageProps) {
  const { type } = params

  return (
    <div className="container mx-auto px-4 py-8">
      <Suspense fallback={<LoadingSpinner />}>
        <AsyncSearchResults type={type} searchParams={searchParams} />
      </Suspense>
    </div>
  )
}