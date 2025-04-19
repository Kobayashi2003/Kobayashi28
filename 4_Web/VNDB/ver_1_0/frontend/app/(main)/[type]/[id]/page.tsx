"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"
import { useUserContext } from "@/context/UserContext"

import { cn } from "@/lib/utils"
import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"
import { MarkButton } from "@/components/button/MarkButton"
import { MarkDialog } from "@/components/dialog/MarkDialog"

import VNPage from "./VNPage"
import CharacterPage from "./CharacterPage"
import StaffPage from "./StaffPage"
import TraitPage from "./TraitPage"
import TagPage from "./TagPage"
import ProducerPage from "./ProducerPage"
import ReleasePage from "./ReleasePage"

import type {
  VN, Release, Character, Producer, Staff, Tag, Trait, Category
} from "@/lib/types"
import { api } from "@/lib/api"

export default function ItemPage() {
  const { user } = useUserContext()
  const params = useParams()
  const type = params.type as "v" | "r" | "c" | "p" | "s" | "g" | "i"
  const id = parseInt(params.id as string)

  const [resourceState, setResourceState] = useState({
    state: null as "loading" | "error" | "notFound" | null,
    message: null as string | null
  })

  const [categoryState, setCategoryState] = useState({
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

  const [openMarkDialog, setOpenMarkDialog] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [toggledCategoryIds, setToggledCategoryIds] = useState<number[]>([])

  const [resourceAbortController, setResourceAbortController] = useState<AbortController | null>(null)
  const [categoryAbortController, setCategoryAbortController] = useState<AbortController | null>(null)

  const fetchItem = async () => {
    try {
      resourceAbortController?.abort()
      const newController = new AbortController()
      setResourceAbortController(newController)

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

  const fetchCategories = async () => {
    if (!user) return
    try {
      categoryAbortController?.abort()
      const newController = new AbortController()
      setCategoryAbortController(newController)
      setCategoryState({
        state: "loading",
        message: null
      })
      const fetchedCategories = await api.category.get(type, newController.signal)
      if (fetchedCategories.length === 0) {
        setCategoryState({
          state: "notFound",
          message: null
        })
        return
      }
      const fetchedToggledCategoryIds = await api.mark.getCategoriesByMark(type, id)
      const sortedCategories = fetchedCategories.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      const toggledCategories = sortedCategories.filter((category) => fetchedToggledCategoryIds.categoryIds.includes(category.id))
      const otherCategories = sortedCategories.filter((category) => !fetchedToggledCategoryIds.categoryIds.includes(category.id))
      setCategories([...toggledCategories, ...otherCategories])
      setToggledCategoryIds(fetchedToggledCategoryIds.categoryIds)
      setCategoryState({
        state: null,
        message: null
      })
    } catch (error) {
      setCategoryState({
        state: "error",
        message: error as string
      })
    }
  }

  const handleRefreshCategories = async () => {
    fetchCategories()
  }

  const handleToggleCategory = async (categoryId: number) => {
    if (!user) return
    try {
      setCategoryState({
        state: "loading",
        message: null
      })
      if (toggledCategoryIds.includes(categoryId)) {
        await api.category.removeMark(type, categoryId, id)
      } else {
        await api.category.addMark(type, categoryId, id)
      }
      handleRefreshCategories()
    } catch (error) {
      setCategoryState({
        state: "error",
        message: error as string
      })
    }
  }

  const handleCreateCategory = async (newCategoryName: string) => {
    if (!user) return
    try {
      setCategoryState({
        state: "loading",
        message: null
      })
      await api.category.create(type, newCategoryName)
      handleRefreshCategories()
    } catch (error) {
      setCategoryState({
        state: "error",
        message: error as string
      })
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    if (!user) return
    try {
      setCategoryState({
        state: "loading",
        message: null
      })
      await api.category.delete(type, categoryId)
      handleRefreshCategories()
    } catch (error) {
      setCategoryState({
        state: "error",
        message: error as string
      })
    }
  }

  useEffect(() => {
    fetchItem()
    return () => {
      resourceAbortController?.abort()
    }
  }, [])

  useEffect(() => {
    if (!user) return
    fetchCategories()
    return () => {
      categoryAbortController?.abort()
    }
  }, [user])

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
          {type === "v" && resourceData.vn && <VNPage vn={resourceData.vn} />}
          {type === "r" && resourceData.release && <ReleasePage release={resourceData.release} />}
          {type === "c" && resourceData.character && <CharacterPage character={resourceData.character} />}
          {type === "p" && resourceData.producer && <ProducerPage producer={resourceData.producer} />}
          {type === "s" && resourceData.staff && <StaffPage staff={resourceData.staff} />}
          {type === "g" && resourceData.tag && <TagPage tag={resourceData.tag} />}
          {type === "i" && resourceData.trait && <TraitPage trait={resourceData.trait} />}
        </motion.div>
      </AnimatePresence>
      <MarkButton 
        isMarked={toggledCategoryIds.length > 0}
        onClick={() => setOpenMarkDialog(true)}
        disabled={false}
        className={cn(
          "fixed bottom-6 right-6 z-1",
          !user && "hidden"
        )}
      />
      <MarkDialog
        open={openMarkDialog}
        setOpen={setOpenMarkDialog}
        state={categoryState.state}
        categories={categories}
        toggledCategoryIds={toggledCategoryIds}
        handleRefreshCategories={handleRefreshCategories}
        handleCreateCategory={handleCreateCategory}
        handleDeleteCategory={handleDeleteCategory}
        handleToggleCategory={handleToggleCategory}
      />
    </main>
  )
}