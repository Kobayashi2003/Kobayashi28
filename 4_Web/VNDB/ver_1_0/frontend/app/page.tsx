import { api } from "@/lib/api"
import type { VN, Release, Character, Producer, Staff } from "@/lib/types"
import * as ScrollArea from "@radix-ui/react-scroll-area"
import Link from "next/link"

async function fetchData() {
  const vns = await api.vn("", { size: "small", limit: 100, from: "local" })
  const releases = await api.release("", { size: "small", limit: 100, from: "local" })
  const characters = await api.character("", { size: "small", limit: 100, from: "local" })
  const producers = await api.producer("", { size: "small", limit: 100, from: "local" })
  const staff = await api.staff("", { size: "small", limit: 100, from: "local" })

  return { vns, releases, characters, producers, staff }
}

export default async function Home() {
  const { vns, releases, characters, producers, staff } = await fetchData()

  return (
    <main className="container mx-auto p-4 pb-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 h-[calc(100vh-12rem)]">
        <Column title="Visual Novels" items={vns.results} type="vn" />
        <Column title="Releases" items={releases.results} type="release" />
        <Column title="Characters" items={characters.results} type="character" />
        <Column title="Producers" items={producers.results} type="producer" />
        <Column title="Staff" items={staff.results} type="staff" />
      </div>
    </main>
  )
}

type ColumnProps = {
  title: string
  items: VN[] | Release[] | Character[] | Producer[] | Staff[]
  type: "vn" | "release" | "character" | "producer" | "staff"
}

function Column({ title, items, type }: ColumnProps) {
  const getDisplayName = (item: VN | Release | Character | Producer | Staff) => {
    switch (type) {
      case "vn":
      case "release":
        return (item as VN | Release).title
      case "character":
      case "producer":
      case "staff":
        return (item as Character | Producer | Staff).name
      default:
        return "Unknown"
    }
  }

  return (
    <div className="bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg flex flex-col h-full border border-white/10 transition-all duration-300 hover:bg-[#0F2942]/90 hover:border-white/20 overflow-hidden">
      <h2 className="text-xl font-semibold p-4 border-b border-white/10 text-white/90 shrink-0">{title}</h2>
      <div className="flex-1 min-h-0">
        <ScrollArea.Root className="h-full">
          <ScrollArea.Viewport className="h-full w-full">
            <ul className="p-2">
              {items.map((item) => (
                <li key={item.id}>
                  <Link
                    href={`/${item.id}`}
                    className="block w-full text-left p-2 rounded text-white/80 hover:text-white hover:bg-white/5 transition-colors duration-200"
                  >
                    {getDisplayName(item)}
                  </Link>
                </li>
              ))}
            </ul>
          </ScrollArea.Viewport>
          <ScrollArea.Scrollbar
            className="flex select-none touch-none p-0.5 bg-white/5 transition-colors duration-[160ms] ease-out hover:bg-white/10 data-[orientation=vertical]:w-2.5 data-[orientation=horizontal]:flex-col data-[orientation=horizontal]:h-2.5"
            orientation="vertical"
          >
            <ScrollArea.Thumb className="flex-1 bg-white/20 rounded-[10px] relative before:content-[''] before:absolute before:top-1/2 before:left-1/2 before:-translate-x-1/2 before:-translate-y-1/2 before:w-full before:h-full before:min-w-[44px] before:min-h-[44px]" />
          </ScrollArea.Scrollbar>
        </ScrollArea.Root>
      </div>
    </div>
  )
}