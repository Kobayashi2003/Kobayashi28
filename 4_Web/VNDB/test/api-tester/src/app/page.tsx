import DualAPITester from '@/components/dual-api-tester'
import { ThemeProvider } from "@/components/theme-provider"

export default function Home() {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <main className="container mx-auto py-8">
        <DualAPITester />
      </main>
    </ThemeProvider>
  )
}