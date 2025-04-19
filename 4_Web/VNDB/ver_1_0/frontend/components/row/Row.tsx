interface RowProps {
  label: string
  value: React.ReactNode
}

export function Row({ label, value }: RowProps) {
  if (!value) return null

  return (
    <div className="grid grid-cols-[120px_1fr] gap-1">
      <h3 className="font-bold text-left md:text-center text-white/80">{label}</h3>
      <div className="flex items-center text-xs md:text-sm">
        {value}
      </div>
    </div>
  )
}
