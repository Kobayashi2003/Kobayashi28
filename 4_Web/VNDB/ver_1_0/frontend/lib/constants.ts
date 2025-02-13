export const VNDB_BASE_URL = process.env.NEXT_PUBLIC_VNDB_BASE_URL || 'http://localhost:5000';
export const IMGSERVE_BASE_URL = process.env.NEXT_PUBLIC_IMGSERVE_BASE_URL || 'http://localhost:5001';
export const USERSERVE_BASE_URL = process.env.NEXT_PUBLIC_IMGSERVE_BASE_URL || 'http://localhost:5002';

export const LANGUAGES: Record<string, string> = {
  ar: "Arabic",
  be: "Belarusian",
  bg: "Bulgarian",
  ca: "Catalan",
  ck: "Cherokee",
  cs: "Czech",
  da: "Danish",
  de: "German",
  el: "Greek",
  en: "English",
  eo: "Esperanto",
  es: "Spanish",
  et: "Estonian",
  eu: "Basque",
  fa: "Persian",
  fi: "Finnish",
  fr: "French",
  ga: "Irish",
  gd: "Scottish Gaelic",
  he: "Hebrew",
  hi: "Hindi",
  hr: "Croatian",
  hu: "Hungarian",
  id: "Indonesian",
  it: "Italian",
  iu: "Inuktitut",
  ja: "Japanese",
  ka: "Georgian",
  ko: "Korean",
  la: "Latin",
  lt: "Lithuanian",
  lv: "Latvian",
  mk: "Macedonian",
  ms: "Malay",
  nl: "Dutch",
  no: "Norwegian",
  pl: "Polish",
  "pt-br": "Portuguese (Brazilian)",
  "pt-pt": "Portuguese",
  pt: "Portuguese",
  ro: "Romanian",
  ru: "Russian",
  sk: "Slovak",
  sl: "Slovenian",
  sr: "Serbian",
  sv: "Swedish",
  th: "Thai",
  tr: "Turkish",
  uk: "Ukrainian",
  ur: "Urdu",
  vi: "Vietnamese",
  "zh-Hans": "Chinese (Simplified)",
  "zh-Hant": "Chinese (Traditional)",
  zh: "Chinese",
} as const

// Language code to icon class mapping
export const LANGUAGE_ICONS: Record<string, string> = {
  ar: "icon-lang-ar",
  be: "icon-lang-be",
  bg: "icon-lang-bg",
  ca: "icon-lang-ca",
  ck: "icon-lang-ck",
  cs: "icon-lang-cs",
  da: "icon-lang-da",
  de: "icon-lang-de",
  el: "icon-lang-el",
  en: "icon-lang-en",
  eo: "icon-lang-eo",
  es: "icon-lang-es",
  eu: "icon-lang-eu",
  fa: "icon-lang-fa",
  fi: "icon-lang-fi",
  fr: "icon-lang-fr",
  ga: "icon-lang-ga",
  gd: "icon-lang-gd",
  he: "icon-lang-he",
  hi: "icon-lang-hi",
  hr: "icon-lang-hr",
  hu: "icon-lang-hu",
  id: "icon-lang-id",
  it: "icon-lang-it",
  iu: "icon-lang-iu",
  ja: "icon-lang-ja",
  kk: "icon-lang-kk",
  ko: "icon-lang-ko",
  la: "icon-lang-la",
  lt: "icon-lang-lt",
  lv: "icon-lang-lv",
  mk: "icon-lang-mk",
  ms: "icon-lang-ms",
  nl: "icon-lang-nl",
  no: "icon-lang-no",
  pl: "icon-lang-pl",
  "pt-br": "icon-lang-pt-br",
  "pt-pt": "icon-lang-pt-pt",
  pt: "icon-lang-pt-pt",
  ro: "icon-lang-ro",
  ru: "icon-lang-ru",
  sk: "icon-lang-sk",
  sl: "icon-lang-sl",
  sr: "icon-lang-sr",
  sv: "icon-lang-sv",
  ta: "icon-lang-ta",
  th: "icon-lang-th",
  tr: "icon-lang-tr",
  uk: "icon-lang-uk",
  ur: "icon-lang-ur",
  vi: "icon-lang-vi",
  "zh-Hans": "icon-lang-zh-Hans",
  "zh-Hant": "icon-lang-zh-Hant",
  zh: "icon-lang-zh",
} as const

// Platform code to full name mapping
export const PLATFORMS: Record<string, string> = {
  win: "Windows",
  lin: "Linux",
  mac: "macOS",
  ios: "iOS",
  and: "Android",
  dvd: "DVD",
  bdp: "Blu-ray",
  ps1: "PlayStation",
  ps2: "PlayStation 2",
  ps3: "PlayStation 3",
  ps4: "PlayStation 4",
  ps5: "PlayStation 5",
  psp: "PlayStation Portable",
  psv: "PlayStation Vita",
  xb1: "Xbox One",
  xb3: "Xbox Series X/S",
  xbo: "Xbox",
  swi: "Nintendo Switch",
  wii: "Wii",
  wiu: "Wii U",
  nds: "Nintendo DS",
  n3d: "Nintendo 3DS",
  web: "Web",
} as const

// Platform code to icon class mapping
export const PLATFORM_ICONS: Record<string, string> = {
  win: "icon-plat-win",
  lin: "icon-plat-lin",
  mac: "icon-plat-mac",
  ios: "icon-plat-ios",
  and: "icon-plat-and",
  dvd: "icon-plat-dvd",
  bdp: "icon-plat-bdp",
  ps1: "icon-plat-ps1",
  ps2: "icon-plat-ps2",
  ps3: "icon-plat-ps3",
  ps4: "icon-plat-ps4",
  ps5: "icon-plat-ps5",
  psp: "icon-plat-psp",
  psv: "icon-plat-psv",
  xb1: "icon-plat-xb1",
  xb3: "icon-plat-xb3",
  xbo: "icon-plat-xbo",
  swi: "icon-plat-swi",
  wii: "icon-plat-wii",
  wiu: "icon-plat-wiu",
  nds: "icon-plat-nds",
  n3d: "icon-plat-n3d",
  web: "icon-plat-web",
} as const

// Relation type to full name mapping
export const RELATIONS: Record<string, string> = {
  ser: "Same series",
  char: "Shares characters",
  alt: "Alternative version",
  preq: "Prequel",
  seq: "Sequel",
  side: "Side story",
  set: "Same setting",
  fan: "Fandisc",
  orig: "Original game",
  par: "Parent story",
  child: "Child story",
  other: "Other",
} as const

export const MEDIUM: Record<string, string> = {
  in: "Internet download",
  cd: "CD",
  dvd: "DVD",
  blr: "Blu-ray",
  gd: "GD",
  gdr: "GD-ROM",
  umd: "UMD",
  flp: "Floppy Disk",
  mrt: "Cartridge",
} as const

export const RELEASE_ICONS = {
  media: {
    download: "icon-rel-download",
    disk: "icon-rel-disk",
    cartridge: "icon-rel-cartridge",
  },
  voiced: {
    v1: "icon-rel-voiced icon-rel-v1", // Not voiced
    v2: "icon-rel-voiced icon-rel-v2", // Only ero scenes voiced
    v3: "icon-rel-voiced icon-rel-v3", // Partially voiced
    v4: "icon-rel-voiced icon-rel-v4", // Fully voiced
  },
  rtype: {
    complete: "icon-rtcomplete",
    partial: "icon-rtpartial",
    trial: "icon-rttrial",
  },
  other: {
    notes: "icon-rel-notes",
    free: "icon-rel-free",
    nonfree: "icon-rel-nonfree",
    external: "icon-external",
  },
} as const

export const SEX = {
  m: "Male",
  f: "Female",
  b: "Both",
  n: "Sexless",
} as const

export const SEX_ICONS = {
  m: "icon-char-m",
  f: "icon-char-f",
  b: "icon-char-b",
  n: "icon-char-n",
} as const

export const SEX_COLORS = {
  m: "charsex-m",
  f: "charsex-f",
  b: "charsex-b",
  n: "charsex-n",
} as const

export const VOICED = {
  1: "Not voiced",
  2: "Only ero scenes voiced",
  3: "Partially voiced",
  4: "Fully voiced",
} as const

export const CATEGORIES = [
  { id: "cont", label: "content" },
  { id: "tech", label: "technical" },
  { id: "ero", label: "sexual content" },
] as const

export const SPOILER = [
  { id: "hide", label: "hide spoilers", value: 0 },
  { id: "minor", label: "show minor spoilers", value: 1 },
  { id: "all", label: "spoil me!", value: 2 },
] as const

export const SIZES = {
  xs: "text-xs",
  sm: "text-sm",
  base: "text-base",
  lg: "text-lg",
} as const

export const ROLE = {
  primary: "Main character",
  side: "Side character",
  main: "Protagonist",
} as const