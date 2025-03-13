import { HeaderBar } from "@/components/header/HeaderBar"
import { UserProvider } from "@/context/UserContext"
import { SearchProvider } from "@/context/SearchContext"
import { IMGSERVE_BASE_URL } from "@/lib/constants"

export default function MainLayout({ children }: { children: React.ReactNode }) {

  const bgUrl = `url(${(typeof window === 'undefined') ? `${process.env.NEXT_PUBLIC_IMGSERVE_BASE_URL || IMGSERVE_BASE_URL}/bg` : `${IMGSERVE_BASE_URL}/bg`})`

  return (
    <div style={{ 
        backgroundImage: bgUrl, 
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      }}>
      <div className="min-h-screen bg-[#0A1929]/80 text-white">
        <SearchProvider>
        <UserProvider>
          <HeaderBar className="fixed top-0 left-0 right-0 z-50 bg-[#0A1929]/80" />
          <div className="pt-[110px] md:pt-[55px]"></div>
          {children}
        </UserProvider>
        </SearchProvider>
      </div>
    </div>
  )
}