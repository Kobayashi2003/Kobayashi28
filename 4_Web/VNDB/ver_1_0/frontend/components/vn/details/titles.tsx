interface TitlesProps {
  titles?: Array<{
    lang?: string
    title?: string
    latin?: string
    official?: boolean
    main?: boolean
  }>
  mainTitle?: string
}

const LANG_FLAGS: Record<string, string> = {
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
}

export function Titles({ titles }: TitlesProps) {
  if (!titles?.length) return null

  const sortedTitles = [...titles].sort((a, b) => {
    if (a.main && a.official) return -1
    if (b.main && b.official) return 1
    return 0
  })

  return (
    <div className="space-y-1">
      {sortedTitles.map((title, index) => {
        const isMainAndOfficial = title.main && title.official
        return (
          <div key={index} className="flex items-start gap-2 text-sm">
            <span className="w-6 text-center">
              {title.lang && <span className={LANG_FLAGS[title.lang] || "icon-lang-en"} />}
            </span>
            <div className="space-y-0.5 min-w-0">
              <div className={`break-words text-white/90 ${isMainAndOfficial ? "font-bold" : ""}`}>{title.title}</div>
              {title.latin && title.latin !== title.title && (
                <div className="text-white/60 break-words">{title.latin}</div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}