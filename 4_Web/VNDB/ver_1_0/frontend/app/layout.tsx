import "@/styles/globals.css"
import { Search } from "@/components/search"
import type React from "react" // Import React

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#0A1929]">
        <header className="py-4 px-4 border-b border-white/10">
          <div className="container mx-auto space-y-4">
            <h1 className="text-2xl font-bold text-white">Visual Novel Database</h1>
            <Search />
          </div>
        </header>
        {children}
      </body>
    </html>
  )
}