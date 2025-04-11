import Link from "next/link"
import { cn } from "@/lib/utils"

interface TextCardProps {
  title: string
  msgs: string[]
  link?: string
  className?: string
}

export function TextCard({ title, msgs, link, className }: TextCardProps) {

  const containerStyle = cn(
    "bg-[#0F2942]/80 hover:bg-[#0F2942]",
    "rounded-lg",
    "p-2",
    "border border-white/10",
    "hover:scale-105 transition-transform duration-300",
    link ? "cursor-pointer" : "cursor-default",
    className
  )

  const textWrapperStyle = "w-full p-2"
  const titleTextStyle = cn(
    "truncate font-semibold text-xs sm:text-sm md:text-base",
    "border-b border-white/10 mb-1"
  )
  const msgTextStyle = "truncate text-xs md:text-sm text-gray-400"


  return (
    <Link href={link || ""}>
      <div className={cn(containerStyle)}>
        <div className={cn(textWrapperStyle)}>
          <h2 className={cn(titleTextStyle)}>{title}</h2>
          {msgs?.filter(Boolean).map((msg, index) => (
            <p key={index} className={cn(msgTextStyle)}>{msg}</p>
          ))}
        </div>
      </div>
    </Link>
  )
}