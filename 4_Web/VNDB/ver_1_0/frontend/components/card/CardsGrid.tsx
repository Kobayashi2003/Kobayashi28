import { motion } from "motion/react"
import { cn } from "@/lib/utils"
import { ImageCard } from "./ImageCard"
import { ImageCard2 } from "./ImageCard2"
import { TextCard } from "./TextCard"

import { ENUMS } from "@/lib/enums"

import {
  VN_Small, Release_Small, Character_Small, Producer_Small, Staff_Small, Tag_Small, Trait_Small
} from "@/lib/types"

type ImageProps = {
  url: string
  dims: [number, number]
  thumbnail?: string
  thumbnail_dims?: [number, number]
  sexual: number
  violence: number
}

type GridItem = {
  id: string
  title: string
  msgs: string[]
  image?: ImageProps
  link: string
}

interface BaseCardsGridProps {
  items: GridItem[]
  cardType?: "image" | "text"
  layout?: "single" | "grid"
  sexualLevel?: "safe" | "suggestive" | "explicit"
  violenceLevel?: "tame" | "violent" | "brutal"
}

interface GenImageCardProps {
  image?: ImageProps
  title: string
  msgs: string[]
  link?: string
  sexualLevel?: "safe" | "suggestive" | "explicit"
  violenceLevel?: "tame" | "violent" | "brutal"
  layout?: "single" | "grid"
  className?: string
}

interface GenTextCardProps {
  title: string
  msgs: string[]
  link?: string
  layout?: "single" | "grid"
  className?: string
}

interface VNsCardsGridProps {
  vns: VN_Small[]
  cardType?: "image" | "text"
  layout?: "single" | "grid"
  sexualLevel?: "safe" | "suggestive" | "explicit"
  violenceLevel?: "tame" | "violent" | "brutal"
}

interface CharacterCardsGridProps {
  characters: Character_Small[]
  cardType?: "image" | "text"
  layout?: "single" | "grid"
  sexualLevel?: "safe" | "suggestive" | "explicit"
  violenceLevel?: "tame" | "violent" | "brutal"
}

interface ReleaseCardsGridProps {
  releases: Release_Small[]
  layout?: "single" | "grid"
}

interface ProducerCardsGridProps {
  producers: Producer_Small[]
  layout?: "single" | "grid"
}

interface StaffCardsGridProps {
  staff: Staff_Small[]
  layout?: "single" | "grid"
}

interface TagCardsGridProps {
  tags: Tag_Small[]
  layout?: "single" | "grid"
}

interface TraitCardsGridProps {
  traits: Trait_Small[]
  layout?: "single" | "grid"
}

export function GenImageCard({ image, title, msgs, link, sexualLevel = "safe", violenceLevel = "tame", layout = "grid", className }: GenImageCardProps) {

  const sexual = image?.sexual || 0
  const violence = image?.violence || 0

  const alwaysShowImage = true
  const alwaysAllowClick = true
  const blurEffect = "blur-lg"
  const blurHoverEffect = "hover:blur-xs"

  const mildYellowFilter = sexual > 1 && violence > 1 ?
    `${blurEffect} ${blurHoverEffect} bg-yellow-800/30 hover:bg-yellow-800/50` :
    `${blurEffect} ${blurHoverEffect} bg-yellow-400/30 hover:bg-yellow-400/50`
  const moderateYellowFilter = sexual > 1 && violence > 1 ?
    `${blurEffect} ${blurHoverEffect} bg-yellow-800/30 hover:bg-yellow-800/50` :
    `${blurEffect} ${blurHoverEffect} bg-yellow-400/30 hover:bg-yellow-400/50`
  const moderateRedFilter = sexual > 1 && violence > 1 ?
    `${blurEffect} ${blurHoverEffect} bg-red-800/30 hover:bg-red-800/50` :
    `${blurEffect} ${blurHoverEffect} bg-red-400/30 hover:bg-red-400/50`
  const severeRedFilter = sexual > 1 && violence > 1 ?
    `${blurEffect} ${blurHoverEffect} bg-red-800/30 hover:bg-red-800/50` :
    `${blurEffect} ${blurHoverEffect} bg-red-400/30 hover:bg-red-400/50`

  const clickable = alwaysAllowClick ? "cursor-pointer" : "cursor-not-allowed pointer-events-none"

  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      const warningFilter = sexual > 1 && violence > 1 ? mildYellowFilter : moderateYellowFilter
      return layout === "grid" ? (
        <ImageCard
          url={alwaysShowImage ? image?.thumbnail || image?.url || "" : ""}
          title={title} msgs={msgs}
          link={alwaysAllowClick ? link : undefined}
          className={cn(className, clickable, warningFilter, "transition-all duration-300 ease-in-out")}
        />
      ) : (
        <ImageCard2
          url={alwaysShowImage ? image?.thumbnail || image?.url || "" : ""}
          title={title} msgs={msgs}
          link={alwaysAllowClick ? link : undefined}
          className={cn(className, clickable, warningFilter, "transition-all duration-300 ease-in-out")}
        />
      )
    }
    const cautionFilter = sexual > 1 && violence > 1 ? moderateRedFilter : severeRedFilter
    return layout === "grid" ? (
      <ImageCard
        url={alwaysShowImage ? image?.thumbnail || image?.url || "" : ""}
        title={title} msgs={msgs}
        link={alwaysAllowClick ? link : undefined}
        className={cn(className, clickable, cautionFilter, "transition-all duration-300 ease-in-out")}
      />
    ) : (
      <ImageCard2
        url={alwaysShowImage ? image?.thumbnail || image?.url || "" : ""}
        title={title} msgs={msgs}
        link={alwaysAllowClick ? link : undefined}
        className={cn(className, clickable, cautionFilter, "transition-all duration-300 ease-in-out")}
      />
    )
  }
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    const cautionFilter = sexual > 1 && violence > 1 ? moderateRedFilter : severeRedFilter
    return layout === "grid" ? (
      <ImageCard
        url={alwaysShowImage ? image?.thumbnail || image?.url || "" : ""}
        title={title} msgs={msgs}
        link={alwaysAllowClick ? link : undefined}
        className={cn(className, clickable, cautionFilter, "transition-all duration-300 ease-in-out")}
      />
    ) : (
      <ImageCard2
        url={alwaysShowImage ? image?.thumbnail || image?.url || "" : ""}
        title={title} msgs={msgs}
        link={alwaysAllowClick ? link : undefined}
        className={cn(className, clickable, cautionFilter, "transition-all duration-300 ease-in-out")}
      />
    )
  }
  return layout === "grid" ? (
    <ImageCard
      url={image?.thumbnail || image?.url || ""}
      title={title} msgs={msgs}
      link={link}
      className={cn(className)}
    />
  ) : (
    <ImageCard2
      url={image?.thumbnail || image?.url || ""}
      title={title} msgs={msgs}
      link={link}
      className={cn(className)}
    />
  )
}

export function GenTextCard({ title, msgs, link, layout = "grid", className }: GenTextCardProps) {
  return <TextCard title={title} msgs={msgs} link={link} className={cn(className)} />
}

const gridClassName = (layout: "single" | "grid", cardType: "image" | "text") => {
  if (layout === "single") {
    return cardType === "image" ?
      "grid grid-cols-1 gap-4":
      "grid grid-cols-1 gap-4"
  }

  return cardType === "image" ?
    "grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4" :
    "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
}

function BaseCardsGrid({ items, cardType = "text", layout = "grid", sexualLevel = "safe", violenceLevel = "tame" }: BaseCardsGridProps) {
  return (
    <motion.div
      key={`grid-${layout}-${cardType}-${items.map(item => item.id).join("-")}`}
      initial={{ filter: "blur(20px)", opacity: 0, scale: 0.95 }}
      animate={{ filter: "blur(0px)", opacity: 1, scale: 1 }}
      exit={{ filter: "blur(20px)", opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.5, ease: "easeInOut" }}
      className={gridClassName(layout, cardType)}
    >
      {items.map((item, index) => (
        <motion.div
          key={`card-${index}`}
          initial={{ opacity: 0, y: 20, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.98 }}
          transition={{ duration: 0.3, delay: 0.1, ease: "easeInOut" }}
        >
          {cardType === "image" ? (
            <GenImageCard
              image={item.image}
              title={item.title}
              msgs={item.msgs}
              link={item.link}
              sexualLevel={sexualLevel}
              violenceLevel={violenceLevel}
              layout={layout}
            />
          ) : (
            <GenTextCard
              title={item.title}
              msgs={item.msgs}
              link={item.link}
              layout={layout}
            />
          )}
        </motion.div>
      ))}
    </motion.div>
  )
}

export function VNsCardsGrid({ vns, ...props }: VNsCardsGridProps) {
  const items: GridItem[] = vns.map(vn => ({
    id: vn.id,
    title: vn.title,
    msgs: [
      vn.titles.find(title => title.main && title.official)?.title || vn.title,
      `Released: ${vn.released}`,
      vn.developers.length > 0 ? `Developers: ${vn.developers.map(dev => dev.original || dev.name).join(" & ")}` : ""
    ],
    image: vn.image,
    link: `/v/${vn.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} {...props} />
}

export function CharactersCardsGrid({ characters, ...props }: CharacterCardsGridProps) {
  const items: GridItem[] = characters.map(char => ({
    id: char.id,
    title: char.name,
    msgs: [char.original ?? char.name],
    image: char.image,
    link: `/c/${char.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} {...props} />
}

export function ReleasesCardsGrid({ releases, ...props }: ReleaseCardsGridProps) {
  const items: GridItem[] = releases.map(release => ({
    id: release.id,
    title: release.title,
    msgs: [`Released: ${release.released}`],
    link: `/r/${release.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} {...props} />
}

export function ProducersCardsGrid({ producers, ...props }: ProducerCardsGridProps) {
  const items: GridItem[] = producers.map(producer => ({
    id: producer.id,
    title: producer.name,
    msgs: [producer.original ?? producer.name],
    link: `/p/${producer.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} {...props} />
}

export function StaffCardsGrid({ staff, ...props }: StaffCardsGridProps) {
  const items: GridItem[] = staff.map(s => ({
    id: s.id,
    title: s.name,
    msgs: [s.original ?? s.name],
    link: `/s/${s.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} {...props} />
}

export function TagsCardsGrid({ tags, ...props }: TagCardsGridProps) {
  const items: GridItem[] = tags.map(tag => ({
    id: tag.id,
    title: tag.name,
    msgs: [ENUMS.CATEGORY[tag.category as keyof typeof ENUMS.CATEGORY]],
    link: `/t/${tag.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} {...props} />
}

export function TraitsCardsGrid({ traits, ...props }: TraitCardsGridProps) {
  const items: GridItem[] = traits.map(trait => ({
    id: trait.id,
    title: trait.name,
    msgs: [trait.group_name ?? ""],
    link: `/t/${trait.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} {...props} />
}