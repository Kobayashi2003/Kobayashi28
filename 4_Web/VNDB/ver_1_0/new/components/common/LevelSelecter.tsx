interface LevelSelecterProps {
  levelOptions: {
    key: string,
    label: string,
    value: string,
    activeColor: string,
  }[],
  selectedValue: string,
  onChange: (value: string) => void,
}

export function LevelSelecter({ levelOptions, selectedValue, onChange }: LevelSelecterProps) {
  return (
    <div className="flex gap-4 items-center select-none">
      {levelOptions.map((option) => (
        <button
          key={option.key}
          onClick={() => onChange(option.value)}
          className={`transition-colors ${
            selectedValue === option.value 
              ? option.activeColor 
              : "text-white"
          } hover:text-white/80`}
        >
          {option.label}
        </button>
      ))}
    </div>
  )
}
