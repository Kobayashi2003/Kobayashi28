import { cn } from "@/lib/utils";
import { LevelSelectorButton, LevelSelectorSelect } from "@/components/selector/LevelSelector";

const sexualLevelButtonOptions = [
  {
    key: "sexual-level-button-safe",
    value: "safe",
    label: "Safe",
    selectedClassName: "text-[#88ccff]",
    unselectedClassName: "text-white/80 hover:text-[#88ccff]/70",
    className: "font-bold",
  },
  {
    key: "sexual-level-button-suggestive",
    value: "suggestive",
    label: "Suggestive",
    selectedClassName: "text-[#ffcc66]",
    unselectedClassName: "text-white/80 hover:text-[#ffcc66]/70",
    className: "font-bold",
  },
  {
    key: "sexual-level-button-explicit",
    value: "explicit",
    label: "Explicit",
    selectedClassName: "text-[#ff6666]",
    unselectedClassName: "text-white/80 hover:text-[#ff6666]/70",
    className: "font-bold",
  }
]

const sexualLevelSelectOptions = [
  {
    key: "sexual-level-select-safe",
    value: "safe",
    label: "🟢SA",
  },
  {
    key: "sexual-level-select-suggestive",
    value: "suggestive",
    label: "🟡SU",
  },
  {
    key: "sexual-level-select-explicit",
    value: "explicit",
    label: "🔴EX",
  }
]

interface SexualLevelSelectorProps {
  sexualLevel: string
  setSexualLevel: (value: string) => void
}

export function SexualLevelSelector({ sexualLevel, setSexualLevel }: SexualLevelSelectorProps) {
  return (
    <>
      <LevelSelectorButton
        levelOptions={sexualLevelButtonOptions}
        selectedLevel={sexualLevel}
        setSelectedLevel={setSexualLevel}
        className={cn(
          "hidden sm:flex",
          "font-serif italic",
          "border-b border-white/50"
        )}
      />
      <LevelSelectorSelect
        levelOptions={sexualLevelSelectOptions}
        selectedLevel={sexualLevel}
        setSelectedLevel={setSexualLevel}
        className={cn(
          "sm:hidden",
        )}
      />
    </>
  )
}