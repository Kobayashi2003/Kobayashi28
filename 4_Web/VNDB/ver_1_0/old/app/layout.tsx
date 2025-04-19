"use client"

import "@/styles/globals.css"
import "@/styles/icons.css"
import Link from "next/link"
import { useRouter, usePathname } from "next/navigation"
import { ArrowLeft } from "lucide-react"
import { SearchHeader } from "@/components/search/search-header"
import { UserProvider } from "@/components/user/user-context"
import { UserHeader } from "@/components/user/user-header"
import { Button } from "@/components/ui/button"
import type React from "react"


function Header() {
  const router = useRouter()
  const pathname = usePathname()
  const isHomePage = pathname === "/"

  return (
    <header className="py-4 px-4 border-b border-white/10">
      <div className="container mx-auto space-y-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-4">
            {!isHomePage && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => router.back()}
                className="text-white hover:bg-white/10"
                aria-label="Go back"
              >
                <ArrowLeft className="h-5 w-5" />
              </Button>
            )}
            <Link href="/" className="hover:opacity-80 transition-opacity">
              <h1 className="text-2xl font-bold text-white">Visual Novel Database</h1>
            </Link>
          </div>
          <UserHeader />
        </div>
        <SearchHeader />
      </div>
    </header>
  )
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#0A1929]">
        <UserProvider>
          <Header />
          {children}
        </UserProvider>
      </body>
    </html>
  )
}