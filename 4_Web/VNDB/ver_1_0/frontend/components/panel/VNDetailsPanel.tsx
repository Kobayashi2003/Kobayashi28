import { cn } from "@/lib/utils"
import { Image } from "@/components/image/Image"
import { Row } from "@/components/row/Row"
import { TitlesRow } from "@/components/row/TitlesRow"
import { PlatformsRow } from "@/components/row/PlatformsRow"
import { DevelopersRow } from "@/components/row/DevelopersRow"
import { PublishersRow } from "@/components/row/PublishersRow"
import { RelationsRow } from "@/components/row/RelationsRow"
import { ExtlinksRow } from "@/components/row/ExtlinksRow"
import { VN } from "@/lib/types"
import { ENUMS } from "@/lib/enums"
export function VNDetailsPanel({ vn }: { vn: VN }) {

  const mainTitle = vn.title
  const subTitle = vn.titles.find((t) => t.official && t.main)?.title || ""
  const image_url = vn.image?.url
  const image_dims = vn.image?.dims
  const image_thumbnail = vn.image?.thumbnail
  const image_thumbnail_dims = vn.image?.thumbnail_dims
  const image_sexual = vn.image?.sexual
  const image_violence = vn.image?.violence

  const titles = vn.titles
  const aliases = vn.aliases
  const released = vn.released
  const platforms = vn.platforms
  const developers = vn.developers
  const publishers = vn.publishers
  const length = vn.length
  const lengthHours = vn.length_minutes && Math.floor(vn.length_minutes / 60)
  const lengthMinutes = vn.length_minutes && vn.length_minutes % 60
  const lengthVotes = vn.length_votes
  const relations = vn.relations
  const extlinks = vn.extlinks

  return (
    <div className="flex flex-col gap-4 bg-[#0F2942]/80 backdrop-blur-md rounded-lg shadow-lg border border-white/10 p-4 md:p-8">
      <div>
        {/* TITLE */}
        <h1 className="text-2xl font-bold">{mainTitle}</h1>
        <h2 className="text-sm text-gray-500">{subTitle}</h2>
      </div>
      <div className={cn(
        "grid",
        image_url && "md:grid-cols-[250px_1fr]"
      )}>
        {/* IMAGE */}
        {image_url && (
          <Image
            url={image_url}
            thumbnail={image_thumbnail}
            image_dims={image_dims}
            thumbnail_dims={image_thumbnail_dims}
          />
        )}
        {/* Details */}
        <div className="flex flex-col gap-2">
          <TitlesRow titles={titles} />
          <Row label="Aliases" value={aliases.join(", ")} />
          <Row label="Play Time" value={ENUMS.LENGTH[length as keyof typeof ENUMS.LENGTH]
            + ((lengthHours || lengthMinutes) && (
              ` (${lengthHours ? `${lengthHours}h` : ``}${lengthMinutes ? `${lengthMinutes}m` : ``} from ${lengthVotes} votes)`
            ))
          } />
          <Row label="Release Date" value={released} />
          <PlatformsRow platforms={platforms} />
          <DevelopersRow developers={developers} />
          <PublishersRow publishers={publishers} />
          <RelationsRow relations={relations} />
          <ExtlinksRow extlinks={extlinks} />
        </div>
      </div>
    </div>
  )
}
