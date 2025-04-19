import { cn } from "@/lib/utils";
import { LevelSelectorButton, LevelSelectorSelect } from "@/components/selector/LevelSelector";

const violenceLevelButtonOptions = [
  {
    key: "violence-level-button-tame",
    value: "tame",
    label: "Tame",
    selectedClassName: "text-[#88ccff]",
    unselectedClassName: "text-white/80 hover:text-[#88ccff]/70",
    className: "font-bold",
  },
  {
    key: "violence-level-button-violent",
    value: "violent",
    label: "Violent",
    selectedClassName: "text-[#ffcc66]",
    unselectedClassName: "text-white/80 hover:text-[#ffcc66]/70",
    className: "font-bold",
  },
  {
    key: "violence-level-button-brutal",
    value: "brutal",
    label: "Brutal",
    selectedClassName: "text-[#ff6666]",
    unselectedClassName: "text-white/80 hover:text-[#ff6666]/70",
    className: "font-bold",
  }
]

const violenceLevelSelectOptions = [
  {
    key: "violence-level-select-tame",
    value: "tame",
    label: "🟢Tame",
  },
  {
    key: "violence-level-select-violent",
    value: "violent",
    label: "🟡Violent",
  },
  {
    key: "violence-level-select-brutal",
    value: "brutal",
    label: "🔴Brutal",
  }
]

interface ViolenceLevelSelectorProps {
  violenceLevel: string
  setViolenceLevel: (value: string) => void
  disabled?: boolean
  className?: string
}

export function ViolenceLevelSelector({ violenceLevel, setViolenceLevel, disabled, className }: ViolenceLevelSelectorProps) {
  return (
    <>
      <LevelSelectorButton
        levelOptions={violenceLevelButtonOptions}
        selectedLevel={violenceLevel}
        setSelectedLevel={setViolenceLevel}
        disabled={disabled}
        className={cn(
          "hidden sm:flex",
          "font-serif italic",
          "border-b border-white/50",
          className
        )}
      />
      <LevelSelectorSelect
        levelOptions={violenceLevelSelectOptions}
        selectedLevel={violenceLevel}
        setSelectedLevel={setViolenceLevel}
        disabled={disabled}
        className={cn(
          "sm:hidden",
          className
        )}
      />
    </>
  )
}