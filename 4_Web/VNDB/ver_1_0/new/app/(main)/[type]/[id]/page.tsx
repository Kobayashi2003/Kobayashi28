"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"


import { cn } from "@/lib/utils"
import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"

import { VNDetailsPanel } from "@/components/panel/VNDetailsPanel"
import { ReleaseDetailsPanel } from "@/components/panel/ReleaseDetailsPanel"
import { CharacterDetailsPanel } from "@/components/panel/CharacterDetailsPanel"
import { ProducerDetailsPanel } from "@/components/panel/ProducerDetailsPanel"
import { StaffDetailsPanel } from "@/components/panel/StaffDetailsPanel"
import { TagDetailsPanel } from "@/components/panel/TagDetailsPanel"
import { TraitDetailsPanel } from "@/components/panel/TraitDetailsPanel"

import type {
  VN, Release, Character, Producer, Staff, Tag, Trait
} from "@/lib/types"
import { api } from "@/lib/api"

export default function ItemPage() {

  const params = useParams()
  const type = params.type as "v" | "r" | "c" | "p" | "s" | "g" | "i"
  const id = parseInt(params.id as string)

  const [resourceState, setResourceState] = useState({
    state: null as "loading" | "error" | "notFound" | null,
    message: null as string | null
  })

  const [resourceData, setResourceData] = useState({
    vn: null as VN | null,
    release: null as Release | null,
    character: null as Character | null,
    producer: null as Producer | null,
    staff: null as Staff | null,
    tag: null as Tag | null,
    trait: null as Trait | null
  })

  const [abortController, setAbortController] = useState<AbortController | null>(null)

  const fetchItem = async () => {
    try {
      abortController?.abort()
      const newController = new AbortController()
      setAbortController(newController)

      const requestFunction = {
        v: api.by_id.vn,
        r: api.by_id.release,
        c: api.by_id.character,
        p: api.by_id.producer,
        s: api.by_id.staff,
        g: api.by_id.tag,
        i: api.by_id.trait
      }

      const requestResource = {
        v: "vn",
        r: "release",
        c: "character",
        p: "producer",
        s: "staff",
        g: "tag",
        i: "trait"
      }

      setResourceData({
        vn: null,
        release: null,
        character: null,
        producer: null,
        staff: null,
        tag: null,
        trait: null
      })
      setResourceState({
        state: "loading",
        message: null
      })

      const data = await requestFunction[type as keyof typeof requestFunction](id, newController.signal)
      if (!data) {
        setResourceState({
          state: "notFound",
          message: null
        })
        return
      }
      setResourceData({
        ...resourceData,
        [requestResource[type as keyof typeof requestResource]]: data
      })
      setResourceState({
        state: null,
        message: null
      })
    } catch (error) {
      setResourceState({
        state: "error",
        message: error as string
      })
    }
  }

  useEffect(() => {
    fetchItem()
    return () => {
      abortController?.abort()
    }
  }, [])

  return (
    <main className="container mx-auto min-h-screen flex flex-col p-4 pb-8">
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
          {/* Loading */}
          {resourceState.state === "loading" && <Loading message="Loading..." />}
          {/* Error */}
          {resourceState.state === "error" && <Error message={`Error: ${resourceState.message}`} />}
          {/* Not Found */}
          {resourceState.state === "notFound" && <NotFound message="No items found" />}
        </motion.div>
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
          {type === "v" && resourceData.vn && <VNDetailsPanel vn={resourceData.vn} />}
          {type === "r" && resourceData.release && <ReleaseDetailsPanel release={resourceData.release} />}
          {type === "c" && resourceData.character && <CharacterDetailsPanel character={resourceData.character} />}
          {type === "p" && resourceData.producer && <ProducerDetailsPanel producer={resourceData.producer} />}
          {type === "s" && resourceData.staff && <StaffDetailsPanel staff={resourceData.staff} />}
          {type === "g" && resourceData.tag && <TagDetailsPanel tag={resourceData.tag} />}
          {type === "i" && resourceData.trait && <TraitDetailsPanel trait={resourceData.trait} />}
        </motion.div>
      </AnimatePresence>
    </main>
  )
}