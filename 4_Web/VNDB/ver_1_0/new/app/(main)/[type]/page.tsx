"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useRouter, useParams } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { SexualLevelSelector } from "@/components/selector/SexualLevelSelector"
import { ViolenceLevelSelector } from "@/components/selector/ViolenceLevelSelector"
import { CardTypeSwitch } from "@/components/selector/CardTypeSwtich"
import { PaginationButtons } from "@/components/button/PaginationButtons"

import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"

import { 
  VNsCardsGrid, ReleasesCardsGrid, CharactersCardsGrid, 
  ProducersCardsGrid, StaffCardsGrid, TagsCardsGrid, TraitsCardsGrid } 
from "@/components/card/CardsGrid"

import type { 
  VN_Small, Character_Small, Producer_Small, Staff_Small, 
  Tag_Small, Trait_Small, Release_Small, VNDBQueryParams 
} from "@/lib/types"
import { api } from "@/lib/api"

export default function SearchResults() {
  const router = useRouter()
  const params = useParams()
  const searchParams = useSearchParams()

  const type = params.type as "c" | "v" | "p" | "s" | "g" | "i" | "r"

  const itemsPerPage = 24
  const currentPage = parseInt(searchParams.get("page") || "1")

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [totalPages, setTotalPages] = useState(0)

  const [vns, setVNs] = useState<VN_Small[]>([])
  const [characters, setCharacters] = useState<Character_Small[]>([])
  const [producers, setProducers] = useState<Producer_Small[]>([])
  const [staff, setStaff] = useState<Staff_Small[]>([])
  const [tags, setTags] = useState<Tag_Small[]>([])
  const [traits, setTraits] = useState<Trait_Small[]>([])
  const [releases, setReleases] = useState<Release_Small[]>([])

  // CardType, SexualLevel, ViolenceLevel just works in VNs and Characters Pages
  const [cardType, setCardType] = useState<"image" | "text">("image")
  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const [abortController, setAbortController] = useState<AbortController | null>(null)


  const removeKeyFromSearchParams = (key: string) => {
    const params = new URLSearchParams(searchParams)
    params.delete(key)
    router.push(`/${type}?${params.toString()}`)
  }

  const removeMultipleKeysFromSearchParams = (keys: string[]) => {
    const params = new URLSearchParams(searchParams)
    keys.forEach(key => params.delete(key))
    router.push(`/${type}?${params.toString()}`)
  }

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/${type}?${params.toString()}`)
  }

  const updateMultipleSearchParams = (params: Record<string, string>) => {
    const newParams = new URLSearchParams(searchParams)
    Object.entries(params).forEach(([key, value]) => {
      newParams.set(key, value)
    })
    router.push(`/${type}?${newParams.toString()}`)
  }

  const clearItems = () => {
    setVNs([])
    setReleases([])
    setCharacters([])
    setProducers([])
    setStaff([])
    setTags([])
    setTraits([])
  }

  const fetchItems = async () => {
    try {
      abortController?.abort()
      const newController = new AbortController()
      setAbortController(newController)

      setLoading(true)
      setError(null)
      setNotFound(false)

      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as string] = value as string
      }

      switch (type) {
        case "v":
          const vnsResponse = await api.small.vn(params, newController.signal)
          if (vnsResponse.results.length === 0) {
            setNotFound(true)
          }
          setVNs(vnsResponse.results)
          setTotalPages(Math.ceil(vnsResponse.count / itemsPerPage))
          break;
        case "r":
          const releasesResponse = await api.small.release(params, newController.signal)
          if (releasesResponse.results.length === 0) {
            setNotFound(true)
          }
          setReleases(releasesResponse.results)
          setTotalPages(Math.ceil(releasesResponse.count / itemsPerPage))
          break;
        case "c":
          const charactersResponse = await api.small.character(params, newController.signal)
          if (charactersResponse.results.length === 0) {
            setNotFound(true)
          }
          setCharacters(charactersResponse.results)
          setTotalPages(Math.ceil(charactersResponse.count / itemsPerPage))
          break;
        case "p":
          const producersResponse = await api.small.producer(params, newController.signal)
          if (producersResponse.results.length === 0) {
            setNotFound(true)
          }
          setProducers(producersResponse.results)
          setTotalPages(Math.ceil(producersResponse.count / itemsPerPage))
          break;
        case "s":
          const staffResponse = await api.small.staff(params, newController.signal)
          if (staffResponse.results.length === 0) {
            setNotFound(true)
          }
          setStaff(staffResponse.results)
          setTotalPages(Math.ceil(staffResponse.count / itemsPerPage))
          break;
        case "g":
          const tagsResponse = await api.small.tag(params, newController.signal)
          if (tagsResponse.results.length === 0) {
            setNotFound(true)
          }
          setTags(tagsResponse.results)
          setTotalPages(Math.ceil(tagsResponse.count / itemsPerPage))
          break;
        case "i":
          const traitsResponse = await api.small.trait(params, newController.signal)
          if (traitsResponse.results.length === 0) {
            setNotFound(true)
          }
          setTraits(traitsResponse.results)
          setTotalPages(Math.ceil(traitsResponse.count / itemsPerPage))
          break;
      }
    } catch (error) {
      setError(error as string)
    } finally {
      setLoading(false)
    }
  }
  
  const handlePageChange = (page: number) => {
    updateSearchParams("page", page.toString())
  }

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" })
    clearItems()
    fetchItems()
  }, [currentPage, searchParams, type])

  useEffect(() => {
    return () => {
      abortController?.abort()
    }
  }, [abortController])

  const fadeInAnimation = {
    initial: { filter: "blur(20px)", opacity: 0 },
    animate: { filter: "blur(0px)", opacity: 1 },
    exit: { filter: "blur(20px)", opacity: 0 },
    transition: { duration: 0.4, ease: "easeInOut" }
  }
  const statusStyle = "flex-grow flex justify-center items-center"

  return (
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">
      {/* Selectors for VNs and Characters */}
      {(type === "v" || type === "c") && (
        <div className="flex flex-wrap overflow-x-auto items-center justify-between mb-4">
          {/* Card Type Selector */}
          <CardTypeSwitch
            cardType={cardType}
            setCardType={setCardType}
          />
          <div className="flex flex-wrap justify-end gap-2">
            {/* Sexual Level Selector */}
            <SexualLevelSelector
              sexualLevel={sexualLevel}
              setSexualLevel={(value: string) => setSexualLevel(value as "safe" | "suggestive" | "explicit")}
            />
            {/* Divider */}
            <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block" />
            {/* Violence Level Selector */}
            <ViolenceLevelSelector
              violenceLevel={violenceLevel}
              setViolenceLevel={(value: string) => setViolenceLevel(value as "tame" | "violent" | "brutal")}
            />
          </div>
        </div>
      )}
      <AnimatePresence mode="wait">
        {/* Loading */}
        {loading && (
          <motion.div
            key="loading"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <Loading message="Loading..." />
          </motion.div>
        )}
        {/* Error */}
        {error && (
          <motion.div
            key="error"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <Error message={`Error: ${error}`} />
          </motion.div>
        )}
        {/* Not Found */}
        {notFound && (
          <motion.div
            key="notfound"
            {...fadeInAnimation}
            className={statusStyle}
          >
            <NotFound message="No items found" />
          </motion.div>
        )}
        {/* Cards */}
        {!loading && !error && !notFound && (
          <motion.div>
            {type === "v" && (
              <VNsCardsGrid vns={vns} cardType={cardType} sexualLevel={sexualLevel} violenceLevel={violenceLevel} />
            )}
            {type === "c" && (
              <CharactersCardsGrid characters={characters} cardType={cardType} sexualLevel={sexualLevel} violenceLevel={violenceLevel} />
            )}
            {type === "r" && (
              <ReleasesCardsGrid releases={releases} />
            )}
            {type === "p" && (
              <ProducersCardsGrid producers={producers} />
            )}
            {type === "s" && (
              <StaffCardsGrid staff={staff} />
            )}
            {type === "g" && (
              <TagsCardsGrid tags={tags} />
            )}
            {type === "i" && (
              <TraitsCardsGrid traits={traits} />
            )}
          </motion.div>
        )}
      </AnimatePresence>
      {/* Keep the footer at the bottom of the page */}
      <div className="flex-grow" />
      {/* Pagination Buttons */}
      {totalPages > 0 && (
        <div className="flex justify-center items-center mt-4">
          <PaginationButtons
            totalPages={totalPages}
            currentPage={currentPage}
            onPageChange={handlePageChange}
          />
        </div>
      )}
    </main>
  )
}