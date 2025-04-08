"use client"

import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { useUrlParams } from "@/hooks/useUrlParams"
import { useOnVisible } from "@/hooks/useOnVisible"
import { motion, AnimatePresence } from "motion/react"

import { cn } from "@/lib/utils"

import { CategoryControlPanel } from "@/components/category/CategoryControlPanel"
import { TogglePanelButton } from "@/components/button/TogglePanelButton"
import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"

import { DeleteButton } from "@/components/button/DeleteButton"
import { DeleteModeButton } from "@/components/button/DeleteModeButton"
import { ReloadButton } from "@/components/button/ReloadButton"
import { PaginationButtons } from "@/components/button/PaginationButtons"
import { Settings2Button } from "@/components/button/Settings2Button"
import { CardTypeSwitch } from "@/components/selector/CardTypeSwtich"
import { GridLayoutSwitch } from "@/components/selector/GridLayoutSwitch"
import { OrderSwitch } from "@/components/selector/OrderSwitch"
import { SexualLevelSelector } from "@/components/selector/SexualLevelSelector"
import { ViolenceLevelSelector } from "@/components/selector/ViolenceLevelSelector"
import { SortByDialog } from "@/components/dialog/SortByDialog"
import { VNsCardsGrid, CharactersCardsGrid, ProducersCardsGrid, StaffCardsGrid, TagsCardsGrid, ReleasesCardsGrid, TraitsCardsGrid } from "@/components/card/CardsGrid"

import {
  VN_Small, Character_Small, Producer_Small, Staff_Small,
  Tag_Small, Trait_Small, Release_Small, Category
} from "@/lib/types"
import { api } from "@/lib/api"


export default function CategoriesPage() {
  const searchParams = useSearchParams()
  const { removeKey, removeMultipleKeys, updateKey, updateMultipleKeys } = useUrlParams()

  const { isVisible } = useOnVisible("item-bar")

  const itemsPerPage = 24

  const selectedType = searchParams.get("type") || "v"
  const selectedCategoryId = searchParams.get("cid") ? parseInt(searchParams.get("cid") as string) : undefined
  const query = searchParams.get("q") || ""
  const currentPage = searchParams.get("page") ? parseInt(searchParams.get("page") as string) : 1
  const sortBy = searchParams.get("sort") || "id"
  const sortOrder = searchParams.get("order") || "asc"

  const isSearching = query !== ""
  const [openControlPanel, setOpenControlPanel] = useState(true)
  const [sortByDialogOpen, setSortByDialogOpen] = useState(false)

  const [categoryState, setCategoryState] = useState({
    state: null as "loading" | "error" | "notFound" | null,
    message: null as string | null
  })
  const [resourceState, setResourceState] = useState({
    state: null as "loading" | "error" | "notFound" | null,
    message: null as string | null
  })

  const [resourceData, setResourceData] = useState({
    vns: [] as VN_Small[],
    releases: [] as Release_Small[],
    characters: [] as Character_Small[],
    producers: [] as Producer_Small[],
    staff: [] as Staff_Small[],
    tags: [] as Tag_Small[],
    traits: [] as Trait_Small[]
  })

  const [currentPageItemsCount, setCurrentPageItemsCount] = useState(0)
  const [totalItemsCount, setTotalItemsCount] = useState(0)
  const [categories, setCategories] = useState<Category[]>([])

  const [deleteCategoryMode, setDeleteCategoryMode] = useState<boolean>(false)
  const [deleteMarkMode, setDeleteMarkMode] = useState<boolean>(false)

  const [totalPages, setTotalPages] = useState(0)
  const [layout, setLayout] = useState<"grid" | "single">("grid")
  const [cardType, setCardType] = useState<"image" | "text">("image")
  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const [categoriesAbortController, setCategoriesAbortController] = useState<AbortController>()
  const [resourcesAbortController, setResourcesAbortController] = useState<AbortController>()

  const setSelectedType = (value: string) => {
    updateKey("type", value)
  }

  const setSelectedCategoryId = (value: number | undefined) => {
    if (value === undefined) {
      removeKey("cid")
    } else {
      updateKey("cid", value.toString())
    }
  }

  const setCurrentPage = (value: number) => {
    updateKey("page", value.toString())
  }

  const setSortBy = (value: string) => {
    if (value === "marked_at" && query.trim() !== "") {
      setResourceState({
        state: "error",
        message: "marked_at is not supported for search"
      })
      return
    }
    updateKey("sort", value)
  }

  const setSortOrder = (value: string) => {
    updateKey("order", value)
  }


  const fetchCategories = async () => {
    if (!selectedType) return
    try {
      categoriesAbortController?.abort()
      const newAbortController = new AbortController()
      setCategoriesAbortController(newAbortController)

      setCategoryState({
        state: "loading",
        message: null
      })
      const response = await api.category.get(selectedType, newAbortController.signal)
      const sortedCategories = response.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      setCategories(sortedCategories)
      if (sortedCategories.length === 0) {
        setCategoryState({
          state: "notFound",
          message: null
        })
      } else {
        setCategoryState({
          state: null,
          message: null
        })
      }
    } catch (error) {
      setCategoryState({
        state: "error",
        message: error as string
      })
    }
  }

  const fetchResources = async () => {
    if (!selectedType || !selectedCategoryId) {
      setResourceState({
        state: null,
        message: null
      })
      return
    }
    
    try {
      resourcesAbortController?.abort()
      const newAbortController = new AbortController()
      setResourcesAbortController(newAbortController)

      setResourceState({
        state: "loading",
        message: null
      })

      const marksResponse = await api.category.getMarks(selectedType, selectedCategoryId, newAbortController.signal)
      setTotalItemsCount(marksResponse.results.length)
      setTotalPages(Math.ceil(marksResponse.results.length / itemsPerPage))

      if (marksResponse.results.length === 0) {
        setResourceState({
          state: "notFound",
          message: null
        })
        return
      }

      if (sortBy === "marked_at") {
        marksResponse.results.sort((a, b) => new Date(b.marked_at).getTime() - new Date(a.marked_at).getTime())
        marksResponse.results = marksResponse.results.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
      }

      const markIds = marksResponse.results.map(mark => mark.id).join(",")
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

      const response = await requestFunction[selectedType as keyof typeof requestFunction]({
        id: markIds,
        sort: sortBy === "marked_at" ? "id" : sortBy,
        reverse: sortOrder === "desc",
        page: sortBy === "marked_at" ? 1 : currentPage,
        limit: itemsPerPage,
        search: query,
      }, newAbortController.signal)

      if (sortBy === "marked_at") {
        response.results.sort((a, b) => {
          const aId = a.id.slice(1)
          const bId = b.id.slice(1)
          return markIds.indexOf(aId) - markIds.indexOf(bId)
        })
      }

      setResourceData({
        ...resourceData,
        [requestResource[selectedType as keyof typeof requestResource]]: response.results
      })
      setCurrentPageItemsCount(response.results.length)

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


  const handleSearch = async (query: string) => {
    if (!query) {
      removeKey("q")
    } else {
      if (sortBy === "marked_at") {
        setResourceState({
          state: "error",
          message: "marked_at is not supported for search"
        })
        return
      }
      updateMultipleKeys({ q: query, page: "1" })
    }
  }

  const handleCreateCategory = async (newCategoryName: string) => {
    if (!selectedType || !newCategoryName) return
    try {
      setCategoryState({
        state: "loading",
        message: null
      })
      await api.category.create(selectedType, newCategoryName)
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setCategoryState({
        state: "error",
        message: error as string
      })
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    if (!selectedType || !categoryId) return
    try {
      setCategoryState({
        state: "loading",
        message: null
      })
      await api.category.delete(selectedType, categoryId)
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setCategoryState({
        state: "error",
        message: error as string
      })
    }
  }

  const handleDeleteMark = async (markId?: number) => {
    if (!selectedType || !selectedCategoryId || !markId) return
    try {
      if (confirm(`Are you sure you want to delete ${markId}?`)) {
        setResourceState({
          state: "loading",
          message: null
        })
        await api.category.removeMark(selectedType, selectedCategoryId, markId)
        fetchResources()
      }
    } catch (error) {
      setResourceState({
        state: "error",
        message: error as string
      })
    }
  }

  useEffect(() => {
    return () => {
      categoriesAbortController?.abort()
      resourcesAbortController?.abort()
    }
  }, [categoriesAbortController, resourcesAbortController])


  useEffect(() => {
    if (categoryState.state !== "error") return
    
    const timeout = setTimeout(() => {
      setCategoryState({
        state: null,
        message: null
      })
    }, 5000)
    return () => clearTimeout(timeout)
  }, [categoryState.state])

  useEffect(() => {
    if (resourceState.state !== "error") return
    
    const timeout = setTimeout(() => {
      setResourceState({
        state: null,
        message: null
      })
    }, 5000)
    return () => clearTimeout(timeout)
  }, [resourceState.state])


  useEffect(() => {
    removeMultipleKeys(["cid", "q", "page", "sort", "order"])
    setTotalPages(0)
    setResourceData({
      vns: [],
      releases: [],
      characters: [],
      producers: [],
      staff: [],
      tags: [],
      traits: []
    })
    fetchCategories()
  }, [selectedType])

  useEffect(() => {
    removeMultipleKeys(["q", "page", "sort", "order"])
    setTotalPages(0)
    setResourceData({
      vns: [],
      releases: [],
      characters: [],
      producers: [],
      staff: [],
      tags: [],
      traits: []
    })
    fetchResources()
  }, [selectedCategoryId])

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" })
    setTotalPages(0)
    setResourceData({
      vns: [],
      releases: [],
      characters: [],
      producers: [],
      staff: [],
      tags: [],
      traits: []
    })
    fetchResources()
  }, [currentPage, query, sortBy, sortOrder])


  const getItemId = (index: number) => {
    if (selectedType === "v" && resourceData.vns[index]) {
      return resourceData.vns[index].id;
    } else if (selectedType === "r" && resourceData.releases[index]) {
      return resourceData.releases[index].id;
    } else if (selectedType === "c" && resourceData.characters[index]) {
      return resourceData.characters[index].id;
    } else if (selectedType === "p" && resourceData.producers[index]) {
      return resourceData.producers[index].id;
    } else if (selectedType === "s" && resourceData.staff[index]) {
      return resourceData.staff[index].id;
    } else if (selectedType === "g" && resourceData.tags[index]) {
      return resourceData.tags[index].id;
    } else if (selectedType === "i" && resourceData.traits[index]) {
      return resourceData.traits[index].id;
    }
    return undefined;
  }

  const gridClassName = (layout: "grid" | "single", cardType: "image" | "text") => {
    if (layout === "single") {
      return cardType === "image" ?
        "grid grid-cols-1 gap-4" :
        "grid grid-cols-1 gap-4"
    }
    return cardType === "image" ?
      "grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4" :
      "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
  }

  return (
    <div className="w-full min-h-screen flex flex-col md:flex-row gap-1">
      {/* Control Panel */}
      <CategoryControlPanel
        open={openControlPanel}
        type={selectedType}
        categoryOptions={categories.map(category => ({
          value: category.id,
          label: category.category_name,
        }))}
        selectedCategoryId={selectedCategoryId}
        deleteMode={deleteCategoryMode}
        isSearching={isSearching}
        setOpen={setOpenControlPanel}
        setType={setSelectedType}
        setSelectedCategoryId={setSelectedCategoryId}
        setDeleteMode={setDeleteCategoryMode}
        handleDeleteCategory={handleDeleteCategory}
        handleCreateCategory={handleCreateCategory}
        handleSearch={handleSearch}
        disabled={categoryState.state === "loading" || resourceState.state === "loading"}
        className={"md:pl-4 z-10 fixed top-[18%]"}
      />
      <TogglePanelButton
        open={openControlPanel}
        setOpen={setOpenControlPanel}
        direction="left"
        disabled={resourceState.state === "loading"}
        className={cn(
          "z-10 fixed top-[18%] left-0",
          "opacity-60 hover:opacity-100",
          "translate-x-[-50%] hover:translate-x-0",
          isVisible && "hidden",
          openControlPanel && "hidden"
        )}
      />
      {/* Placeholder for Control Panel */}
      <div className={cn("max-md:hidden h-full md:w-100 lg:w-120 xl:w-140", !openControlPanel && "hidden")} />

      {/* Main Content */}
      <div className="overflow-hidden flex-1 p-4 flex flex-col gap-2 transition-all duration-300 justify-between items-center">
        {selectedCategoryId && (
          <div id="item-bar" className="w-full flex max-md:flex-col justify-between gap-2">
            <div className="flex flex-wrap justify-start gap-2">
              {/* Toggle Control Panel Button */}
              <TogglePanelButton
                open={openControlPanel}
                setOpen={setOpenControlPanel}
                direction="left"
                disabled={resourceState.state === "loading"}
                className={cn(openControlPanel && "hidden")}
              />
              {/* Sort By Dialog Button */}
              <Settings2Button
                onClick={() => setSortByDialogOpen(true)}
                disabled={resourceState.state === "loading"}
              />
              {/* Sort By Dialog */}
              <SortByDialog
                open={sortByDialogOpen}
                setOpen={setSortByDialogOpen}
                type={selectedType}
                from={"local"}
                sortBy={sortBy}
                setSortBy={setSortBy}
                additionalOptions={[{ value: "marked_at", label: "Marked At" }]}
              />
              {/* Order Switch Button */}
              <OrderSwitch
                order={sortOrder}
                setOrder={setSortOrder}
                disabled={resourceState.state === "loading"}
              />
              {/* Card Type Button */}
              <CardTypeSwitch
                cardType={cardType}
                setCardType={(value) => setCardType(value as "image" | "text")}
                disabled={resourceState.state === "loading"}
              />
              {/* Layout Switch Button */}
              <GridLayoutSwitch
                layout={layout}
                setLayout={(value) => setLayout(value as "grid" | "single")}
                disabled={resourceState.state === "loading"}
              />
              {/* Delete Mode Button */}
              <DeleteModeButton
                deleteMode={deleteMarkMode}
                setDeleteMode={setDeleteMarkMode}
                disabled={resourceState.state === "loading"}
              />
              {/* Reload Button */}
              <ReloadButton
                handleReload={() => { fetchResources() }}
                disabled={resourceState.state === "loading"}
              />
              {/* Total Items Count */}
              <p className="text-gray-500 self-center select-none">Total: {totalItemsCount}</p>
            </div>
            {(selectedType === "v" || selectedType === "c") ? (
              <div className="w-full md:flex-1 flex justify-end gap-2">
                <SexualLevelSelector
                  sexualLevel={sexualLevel}
                  setSexualLevel={(value) => setSexualLevel(value as "safe" | "suggestive" | "explicit")}
                  disabled={resourceState.state === "loading"}
                  className="w-full md:w-auto"
                />
                {/* Divider */}
                <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block" />
                <ViolenceLevelSelector
                  violenceLevel={violenceLevel}
                  setViolenceLevel={(value) => setViolenceLevel(value as "tame" | "violent" | "brutal")}
                  disabled={resourceState.state === "loading"}
                  className="w-full md:w-auto"
                />
              </div>
            ) : (
              <div className="" />
            )}
          </div>
        )}
        {JSON.stringify(resourceState)}
        <AnimatePresence mode="wait">
          {!selectedCategoryId && (
            <motion.div
              key="notselected"
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="flex-grow flex justify-center items-center"
            >
              <p className="text-gray-500">Select a category to view resources</p>
            </motion.div>
          )}
          {resourceState.state !== null && (
            <motion.div
              key={`status-${resourceState.state}-${resourceState.message}`}
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
              className="flex-grow flex justify-center items-center"
            >
              {resourceState.state === "loading" && (
                <Loading message="Loading..." />
              )}
              {resourceState.state === "error" && (
                <Error message={`Error: ${resourceState.message}`} />
              )}
              {resourceState.state === "notFound" && (
                <NotFound message="No resources found" />
              )}
            </motion.div>
          )}
          {resourceState.state === null && (
            <div className="relative w-full">
              {selectedType === "v" && (
                <VNsCardsGrid vns={resourceData.vns} layout={layout} cardType={cardType} sexualLevel={sexualLevel} violenceLevel={violenceLevel} />
              )}
              {selectedType === "c" && (
                <CharactersCardsGrid characters={resourceData.characters} layout={layout} cardType={cardType} sexualLevel={sexualLevel} violenceLevel={violenceLevel} />
              )}
              {selectedType === "r" && (
                <ReleasesCardsGrid releases={resourceData.releases} layout={layout} />
              )}
              {selectedType === "p" && (
                <ProducersCardsGrid producers={resourceData.producers} layout={layout} />
              )}
              {selectedType === "s" && (
                <StaffCardsGrid staff={resourceData.staff} layout={layout} />
              )}
              {selectedType === "g" && (
                <TagsCardsGrid tags={resourceData.tags} layout={layout} />
              )}
              {selectedType === "i" && (
                <TraitsCardsGrid traits={resourceData.traits} layout={layout} />
              )}
              {deleteMarkMode && (
                <motion.div
                  key={`delete-layer-${deleteMarkMode}-${currentPageItemsCount}`}
                  initial={{ filter: "blur(20px)", opacity: 0, scale: 0.95 }}
                  animate={{ filter: "blur(0px)", opacity: 1, scale: 1 }}
                  exit={{ filter: "blur(20px)", opacity: 0, scale: 0.95 }}
                  transition={{ duration: 0.5, ease: "easeInOut" }}
                  className={cn(
                    "absolute inset-0 pointer-events-auto z-10",
                    (selectedType === "v" || selectedType === "c") && gridClassName(layout, cardType),
                    (selectedType === "p" || selectedType === "s" || selectedType === "g" || selectedType === "i") && gridClassName(layout, "text")
                  )}
                >
                  {Array.from({ length: currentPageItemsCount }).map((_, index) => (
                    <div key={`delete-container-${index}`} className="relative w-full">
                      <motion.div
                        key={`delete-ghost-card-${index}`}
                        initial={{ opacity: 0, y: 20, scale: 0.98 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -20, scale: 0.98 }}
                        transition={{ duration: 0.3, delay: 0.1, ease: "easeInOut" }}
                        className="bg-black/20 w-full h-full rounded-lg"
                      >
                      </motion.div>
                      <DeleteButton
                        handleDelete={() => {
                          const itemId = getItemId(index)
                          if (itemId) {
                            handleDeleteMark(parseInt(itemId.slice(1)))
                          }
                        }}
                        className="absolute top-2 right-2"
                      />
                    </div>
                  ))}
                </motion.div>
              )}
            </div>
          )}
        </ AnimatePresence>
        {/* Keep the footer at the bottom of the page */}
        <div className="flex-grow"></div>
        {totalPages > 1 && (
          <PaginationButtons
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        )}
      </div>
    </div>
  )
}