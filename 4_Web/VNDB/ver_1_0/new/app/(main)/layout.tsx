import { HeaderBar } from "@/components/header/HeaderBar"
import { UserProvider } from "@/context/UserContext"
export default function MainLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#0A1929] text-white">
      <UserProvider>
        <HeaderBar />
        {children}
      </UserProvider>
    </div>
  )
}