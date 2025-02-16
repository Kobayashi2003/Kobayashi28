import "@/styles/globals.css"
import "@/styles/icons.css"
import Link from "next/link"
import { SearchHeader } from "@/components/search/search-header"
import { UserProvider } from "@/components/user/user-context"
import { UserHeader } from "@/components/user/user-header"
import type React from "react"

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#0A1929]">
        <UserProvider>
          <header className="py-4 px-4 border-b border-white/10">
            <div className="container mx-auto space-y-4">
              <div className="flex justify-between items-center">
                <Link href="/" className="hover:opacity-80 transition-opacity">
                  <h1 className="text-2xl font-bold text-white">Visual Novel Database</h1>
                </Link>
                <UserHeader />
              </div>
              <SearchHeader />
            </div>
          </header>
          {children}
        </UserProvider>
      </body>
    </html>
  )
}