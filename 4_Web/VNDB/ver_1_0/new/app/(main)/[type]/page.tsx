"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useParams } from "next/navigation"
import { useUrlParams } from "@/hooks/useUrlParams"
import { motion, AnimatePresence } from "motion/react"

import { cn } from "@/lib/utils"
import { SexualLevelSelector } from "@/components/selector/SexualLevelSelector"
import { ViolenceLevelSelector } from "@/components/selector/ViolenceLevelSelector"
import { CardTypeSwitch } from "@/components/selector/CardTypeSwtich"
import { GridLayoutSwitch } from "@/components/selector/GridLayoutSwitch"
import { PaginationButtons } from "@/components/button/PaginationButtons"

import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"

import {
  VNsCardsGrid, ReleasesCardsGrid, CharactersCardsGrid,
  ProducersCardsGrid, StaffCardsGrid, TagsCardsGrid, TraitsCardsGrid
}
  from "@/components/card/CardsGrid"

import type {
  VN_Small, Character_Small, Producer_Small, Staff_Small,
  Tag_Small, Trait_Small, Release_Small, VNDBQueryParams
} from "@/lib/types"
import { api } from "@/lib/api"

export default function SearchResults() {
  const params = useParams()
  const searchParams = useSearchParams()
  const { updateKey } = useUrlParams()

  const type = params.type as "c" | "v" | "p" | "s" | "g" | "i" | "r"

  const itemsPerPage = 24
  const currentPage = parseInt(searchParams.get("page") || "1")

  const [resourceState, setResourceState] = useState({
    state: null as "loading" | "error" | "notFound" | null,
    message: null as string | null
  })

  const [resourceData, setResourceData] = useState({
    vns: [] as VN_Small[],
    characters: [] as Character_Small[],
    producers: [] as Producer_Small[],
    staff: [] as Staff_Small[],
    tags: [] as Tag_Small[],
    traits: [] as Trait_Small[],
    releases: [] as Release_Small[]
  })

  const [totalPages, setTotalPages] = useState(0)

  const [cardType, setCardType] = useState<"image" | "text">("image")
  const [layout, setLayout] = useState<"single" | "grid">("grid")
  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const [abortController, setAbortController] = useState<AbortController | null>(null)

  const clearItems = () => {
    setResourceData({
      vns: [],
      releases: [],
      characters: [],
      producers: [],
      staff: [],
      tags: [],
      traits: []
    })
  }

  const fetchItems = async () => {
    try {
      abortController?.abort()
      const newController = new AbortController()
      setAbortController(newController)

      const requestFunction = {
        v: api.small.vn,
        r: api.small.release,
        c: api.small.character,
        p: api.small.producer,
        s: api.small.staff,
        g: api.small.tag,
        i: api.small.trait
      }

      const requestResource = {
        v: "vns",
        r: "releases",
        c: "characters",
        p: "producers",
        s: "staff",
        g: "tags",
        i: "traits"
      }

      setResourceState({
        state: "loading",
        message: null
      })

      const params: VNDBQueryParams = { page: currentPage, limit: itemsPerPage }
      for (const [key, value] of searchParams.entries()) {
        params[key as keyof VNDBQueryParams] = value as string
      }

      const response = await requestFunction[type as keyof typeof requestFunction](params, newController.signal)
      setResourceData({
        ...resourceData,
        [requestResource[type as keyof typeof requestResource]]: response.results
      })
      setTotalPages(Math.ceil(response.count / itemsPerPage))
      if (response.results.length === 0) {
        setResourceState({
          state: "notFound",
          message: null
        })
      } else {
        setResourceState({
          state: null,
          message: null
        })
      }
    } catch (error) {
      setResourceState({
        state: "error",
        message: error as string
      })
    }
  }

  const handlePageChange = (page: number) => {
    updateKey("page", page.toString())
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

  return (
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">
      {/* Selectors for VNs and Characters */}
      {(type === "v" || type === "c") && (
        <div className={cn(
          "flex mb-4",
          "flex-col items-center gap-2",
          "sm:flex-row sm:justify-between sm:gap-4"
        )}>
          <div className="w-full sm:flex-1 flex sm:justify-start gap-2">
            {/* Card Type Selector */}
            <CardTypeSwitch
              cardType={cardType}
              setCardType={setCardType}
            />
            {/* Grid Layout Switch */}
            <GridLayoutSwitch
              layout={layout}
              setLayout={setLayout}
            />
          </div>
          <div className="w-full sm:flex-1 flex sm:justify-end gap-2">
            {/* Sexual Level Selector */}
            <SexualLevelSelector
              sexualLevel={sexualLevel}
              setSexualLevel={(value: string) => setSexualLevel(value as "safe" | "suggestive" | "explicit")}
              className="w-full sm:w-auto"
            />
            {/* Divider */}
            <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block" />
            {/* Violence Level Selector */}
            <ViolenceLevelSelector
              violenceLevel={violenceLevel}
              setViolenceLevel={(value: string) => setViolenceLevel(value as "tame" | "violent" | "brutal")}
              className="w-full sm:w-auto"
            />
          </div>
        </div>
      )}
      {(type === "r" || type === "p" || type === "s" || type === "g" || type === "i") && (
        <GridLayoutSwitch
          layout={layout}
          setLayout={setLayout}
          className="mb-4"
        />
      )}
      <AnimatePresence mode="wait">
        {/* Status */}
        <motion.div
          key="status"
          initial={{ filter: "blur(20px)", opacity: 0 }}
          animate={{ filter: "blur(0px)", opacity: 1 }}
          exit={{ filter: "blur(20px)", opacity: 0 }}
          transition={{ duration: 0.4, ease: "easeInOut" }}
          className={cn(
            "flex-grow flex justify-center items-center",
            resourceState.state === null && "hidden"
          )}
        >
          {resourceState.state === "loading" && <Loading message="Loading..." />}
          {resourceState.state === "error" && <Error message={`Error: ${resourceState.message}`} />}
          {resourceState.state === "notFound" && <NotFound message="No items found" />}
        </motion.div>
        
        {/* Cards */}
        <motion.div
          key="content"
          initial={{ filter: "blur(20px)", opacity: 0 }}
          animate={{ filter: "blur(0px)", opacity: 1 }}
          exit={{ filter: "blur(20px)", opacity: 0 }}
          transition={{ duration: 0.4, ease: "easeInOut" }}
          className={cn(
            "w-full",
            resourceState.state !== null && "hidden"
          )}
        >
          {type === "v" && (
            <VNsCardsGrid vns={resourceData.vns} layout={layout} cardType={cardType} sexualLevel={sexualLevel} violenceLevel={violenceLevel} />
          )}
          {type === "c" && (
            <CharactersCardsGrid characters={resourceData.characters} layout={layout} cardType={cardType} sexualLevel={sexualLevel} violenceLevel={violenceLevel} />
          )}
          {type === "r" && (
            <ReleasesCardsGrid releases={resourceData.releases} layout={layout} />
          )}
          {type === "p" && (
            <ProducersCardsGrid producers={resourceData.producers} layout={layout} />
          )}
          {type === "s" && (
            <StaffCardsGrid staff={resourceData.staff} layout={layout} />
          )}
          {type === "g" && (
            <TagsCardsGrid tags={resourceData.tags} layout={layout} />
          )}
          {type === "i" && (
            <TraitsCardsGrid traits={resourceData.traits} layout={layout} />
          )}
        </motion.div>
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