interface TextCardProps {
  title: string
  className?: string
}

export function TextCard({ title, className }: TextCardProps) {
  return (
    <div className={`bg-[#0F2942]/80 hover:bg-[#0F2942] p-2 rounded-lg border border-white/10 overflow-hidden hover:scale-105 transition-transform duration-300 ease-in-out ${className}`}>
      <h2 className="h-full text-center font-semibold truncate text-white text-sm md:text-base">{title}</h2>
    </div>
  )
}