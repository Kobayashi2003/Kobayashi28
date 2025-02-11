export const VNDB_BASE_URL = process.env.NEXT_PUBLIC_VNDB_BASE_URL || 'http://localhost:5000';
export const IMGSERVE_BASE_URL = process.env.NEXT_PUBLIC_IMGSERVE_BASE_URL || 'http://localhost:5001';
export const USERSERVE_BASE_URL = process.env.NEXT_PUBLIC_IMGSERVE_BASE_URL || 'http://localhost:5002';

export const LANG_FLAGS: Record<string, { flag: string; name: string }> = {
  ar: { flag: "🇸🇦", name: "Arabic" },
  be: { flag: "🇧🇾", name: "Belarusian" },
  bg: { flag: "🇧🇬", name: "Bulgarian" },
  ca: { flag: "🇪🇸", name: "Catalan" },
  cs: { flag: "🇨🇿", name: "Czech" },
  da: { flag: "🇩🇰", name: "Danish" },
  de: { flag: "🇩🇪", name: "German" },
  el: { flag: "🇬🇷", name: "Greek" },
  en: { flag: "🇺🇸", name: "English" },
  es: { flag: "🇪🇸", name: "Spanish" },
  et: { flag: "🇪🇪", name: "Estonian" },
  fi: { flag: "🇫🇮", name: "Finnish" },
  fr: { flag: "🇫🇷", name: "French" },
  he: { flag: "🇮🇱", name: "Hebrew" },
  hi: { flag: "🇮🇳", name: "Hindi" },
  hr: { flag: "🇭🇷", name: "Croatian" },
  hu: { flag: "🇭🇺", name: "Hungarian" },
  id: { flag: "🇮🇩", name: "Indonesian" },
  it: { flag: "🇮🇹", name: "Italian" },
  ja: { flag: "🇯🇵", name: "Japanese" },
  ko: { flag: "🇰🇷", name: "Korean" },
  lt: { flag: "🇱🇹", name: "Lithuanian" },
  lv: { flag: "🇱🇻", name: "Latvian" },
  nl: { flag: "🇳🇱", name: "Dutch" },
  no: { flag: "🇳🇴", name: "Norwegian" },
  pl: { flag: "🇵🇱", name: "Polish" },
  pt: { flag: "🇵🇹", name: "Portuguese" },
  "pt-br": { flag: "🇧🇷", name: "Brazilian Portuguese" },
  ro: { flag: "🇷🇴", name: "Romanian" },
  ru: { flag: "🇷🇺", name: "Russian" },
  sk: { flag: "🇸🇰", name: "Slovak" },
  sl: { flag: "🇸🇮", name: "Slovenian" },
  sr: { flag: "🇷🇸", name: "Serbian" },
  sv: { flag: "🇸🇪", name: "Swedish" },
  th: { flag: "🇹🇭", name: "Thai" },
  tr: { flag: "🇹🇷", name: "Turkish" },
  uk: { flag: "🇺🇦", name: "Ukrainian" },
  vi: { flag: "🇻🇳", name: "Vietnamese" },
  zh: { flag: "🇨🇳", name: "Chinese" },
  "zh-hans": { flag: "🇨🇳", name: "Simplified Chinese" },
  "zh-hant": { flag: "🇹🇼", name: "Traditional Chinese" },
}

// Platform icons mapping
export const PLATFORM_ICONS = {
  win: "Windows",
  lin: "Linux",
  mac: "macOS",
  ios: "iOS",
  and: "Android",
  web: "Web",
  swi: "Nintendo Switch",
  ps4: "PlayStation 4",
  ps5: "PlayStation 5",
  xb1: "Xbox One",
  xbx: "Xbox Series X/S",
} as const

// Release type icons
export const RELEASE_ICONS = {
  complete: "Complete",
  partial: "Partial",
  trial: "Trial",
} as const

// Character gender icons
export const CHARACTER_GENDER = {
  m: "Male",
  f: "Female",
  b: "Both",
  n: "None",
} as const