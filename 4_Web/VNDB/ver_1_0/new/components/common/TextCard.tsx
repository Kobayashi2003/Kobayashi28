interface TextCardProps {
  title: string
  subTitle?:string
  textColor?: string
  className?: string
}

export function TextCard({ title, subTitle, textColor, className }: TextCardProps) {
  return (
    <div className={`bg-[#0F2942]/80 hover:bg-[#0F2942] p-2 rounded-lg border border-white/10 overflow-hidden hover:scale-105 transition-transform duration-300 ease-in-out ${className}`}>
      <h2 className={`h-full text-center font-semibold truncate text-sm md:text-base ${textColor || "text-white"}`}>{title}</h2>
      {subTitle && (
        <p className="text-center text-xs md:text-sm text-gray-400">{subTitle}</p>
      )}
    </div>
  )
}