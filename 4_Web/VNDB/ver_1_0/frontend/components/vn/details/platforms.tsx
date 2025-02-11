interface PlatformsProps {
  platforms?: string[]
}

const platformToIcon: { [key: string]: string } = {
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
}

export function Platforms({ platforms }: PlatformsProps) {
  if (!platforms || platforms.length === 0) return null

  return (
    <div className="flex flex-wrap gap-2">
      {platforms.map((platform) => {
        const iconClass = platformToIcon[platform.toLowerCase()]
        if (!iconClass) return null
        return <span key={platform} className={`${iconClass} inline-block`} title={platform} />
      })}
    </div>
  )
}