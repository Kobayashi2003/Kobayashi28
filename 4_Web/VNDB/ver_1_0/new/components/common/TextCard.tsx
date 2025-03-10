interface TextCardProps {
  title: string
}

export function TextCard({ title }: TextCardProps) {
  return (
    <div className="rounded-lg border border-white/10 overflow-hidden transition-transform duration-300 ease-in-out group-hover:scale-105 text-white text-lg p-4 bg-[#0F2942]">
      <h2 className="font-semibold truncate">{title}</h2>
    </div>
  )
}