import { motion } from "motion/react"
import { cn } from "@/lib/utils"
import { ImageCard } from "./ImageCard"
import { TextCard } from "./TextCard"

import { FULL_FORM } from "@/lib/fullForm"

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
  className?: string
}

interface GenTextCardProps {
  title: string
  msgs: string[]
  link?: string
  className?: string
}

interface VNsCardsGridProps {
  vns: VN_Small[]
  cardType?: "image" | "text"
  sexualLevel?: "safe" | "suggestive" | "explicit"
  violenceLevel?: "tame" | "violent" | "brutal"
}

interface CharacterCardsGridProps {
  characters: Character_Small[]
  cardType?: "image" | "text"
  sexualLevel?: "safe" | "suggestive" | "explicit"
  violenceLevel?: "tame" | "violent" | "brutal"
}

interface ReleaseCardsGridProps {
  releases: Release_Small[]
}

interface ProducerCardsGridProps {
  producers: Producer_Small[]
}

interface StaffCardsGridProps {
  staff: Staff_Small[]
}

interface TagCardsGridProps {
  tags: Tag_Small[]
}

interface TraitCardsGridProps {
  traits: Trait_Small[]
}

export function GenImageCard({image, title, msgs, link, sexualLevel = "safe", violenceLevel = "tame", className}: GenImageCardProps) {

  const sexual = image?.sexual || 0
  const violence = image?.violence || 0

  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      const yellow = sexual > 1 && violence > 1 ? `text-yellow-800` : `text-yellow-400`
      return <ImageCard url={""} title={title} msgs={msgs} link={link} className={cn(className, yellow)} />
    }
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard url={""} title={title} msgs={msgs} link={link} className={cn(className, red)} />
  }
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard url={""} title={title} msgs={msgs} link={link} className={cn(className, red)} />
  }
  return <ImageCard url={image?.thumbnail || image?.url || ""} title={title} msgs={msgs} link={link} className={cn(className)} />
}

export function GenTextCard({title, msgs, link, className}: GenTextCardProps) {
  return <TextCard title={title} msgs={msgs} link={link} className={cn(className)} />
}

const gridClassName = (cardType: "image" | "text") => {
  return cardType === "image" ?
    "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4" :
    "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
}

const fadeInAnimation = {
  initial: { filter: "blur(20px)", opacity: 0, scale: 0.95 },
  animate: { filter: "blur(0px)", opacity: 1, scale: 1 },
  exit: { filter: "blur(20px)", opacity: 0, scale: 0.95 },
  transition: { duration: 0.5, ease: "easeInOut" }
}

const cardAnimation = {
  initial: { opacity: 0, y: 20, scale: 0.98 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: -20, scale: 0.98 },
  transition: { duration: 0.3, delay: 0.1, ease: "easeInOut" }
}

function BaseCardsGrid({ items, cardType = "text", sexualLevel = "safe", violenceLevel = "tame" }: BaseCardsGridProps) {
  return (
    <motion.div 
      key={`grid-${cardType}`} 
      {...fadeInAnimation} 
      className={gridClassName(cardType)}
    >
      {items.map((item, index) => (
        <motion.div 
          key={`card-${index}`} 
          {...cardAnimation}
        >
          {cardType === "image" && item.image ? (
            <GenImageCard 
              image={item.image}
              title={item.title}
              msgs={item.msgs}
              link={item.link}
              sexualLevel={sexualLevel}
              violenceLevel={violenceLevel}
            />
          ) : (
            <GenTextCard 
              title={item.title}
              msgs={item.msgs}
              link={item.link}
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
      `Released: ${vn.released}`
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

export function ReleasesCardsGrid({ releases }: ReleaseCardsGridProps) {
  const items: GridItem[] = releases.map(release => ({
    id: release.id,
    title: release.title,
    msgs: [`Released: ${release.released}`],
    link: `/r/${release.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} />
}

export function ProducersCardsGrid({ producers }: ProducerCardsGridProps) {
  const items: GridItem[] = producers.map(producer => ({
    id: producer.id,
    title: producer.name,
    msgs: [producer.original ?? producer.name],
    link: `/p/${producer.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} />
}

export function StaffCardsGrid({ staff }: StaffCardsGridProps) {
  const items: GridItem[] = staff.map(s => ({
    id: s.id,
    title: s.name,
    msgs: [s.original ?? s.name],
    link: `/s/${s.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} />
}

export function TagsCardsGrid({ tags }: TagCardsGridProps) {
  const items: GridItem[] = tags.map(tag => ({
    id: tag.id,
    title: tag.name,
    msgs: [FULL_FORM.TAG_CATEGORY[tag.category as keyof typeof FULL_FORM.TAG_CATEGORY]],
    link: `/t/${tag.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} />
}

export function TraitsCardsGrid({ traits }: TraitCardsGridProps) {
  const items: GridItem[] = traits.map(trait => ({
    id: trait.id,
    title: trait.name,
    msgs: [trait.group_name ?? ""],
    link: `/t/${trait.id.slice(1)}`
  }))
  return <BaseCardsGrid items={items} />
}