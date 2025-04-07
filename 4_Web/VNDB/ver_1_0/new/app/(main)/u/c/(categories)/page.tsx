"use client"

import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { useUrlParams } from "@/hooks/useUrlParams"
import { motion, AnimatePresence } from "motion/react"

import { cn } from "@/lib/utils"

import { CategoryControlPanel } from "@/components/category/CategoryControlPanel"
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

  const itemsPerPage = 24

  const selectedType = searchParams.get("type") || "v"
  const selectedCategoryId = searchParams.get("cid") ? parseInt(searchParams.get("cid") as string) : undefined
  const query = searchParams.get("q") || ""
  const currentPage = searchParams.get("page") ? parseInt(searchParams.get("page") as string) : 1
  const sortBy = searchParams.get("sort") || "id"
  const sortOrder = searchParams.get("order") || "asc"

  const isSearching = query !== ""
  const [open, setOpen] = useState(true)
  const [sortByDialogOpen, setSortByDialogOpen] = useState(false)

  const [categoryState, setCategoryState] = useState({
    loading: false,
    error: null as string | null,
    notFound: false
  })
  const [resourceState, setResourceState] = useState({
    loading: false,
    error: null as string | null,
    notFound: false
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
        loading: true,
        error: null,
        notFound: false
      })
      const response = await api.category.get(selectedType, newAbortController.signal)
      const sortedCategories = response.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      setCategories(sortedCategories)
      if (sortedCategories.length === 0) {
        setCategoryState({
          loading: false,
          error: null,
          notFound: true
        })
      } else {
        setCategoryState({
          loading: false,
          error: null,
          notFound: false
        })
      }
    } catch (error) {
      setCategoryState({
        loading: false,
        error: error as string,
        notFound: false
      })
    }
  }

  const fetchResources = async () => {
    if (!selectedType || !selectedCategoryId) return
    try {
      resourcesAbortController?.abort()
      const newAbortController = new AbortController()
      setResourcesAbortController(newAbortController)

      setResourceState({
        loading: true,
        error: null,
        notFound: false
      })

      const marksResponse = await api.category.getMarks(selectedType, selectedCategoryId, newAbortController.signal)
      setTotalItemsCount(marksResponse.results.length)
      if (marksResponse.results.length === 0) {
        setResourceState({
          loading: false,
          error: null,
          notFound: true
        })
        return
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
        sort: sortBy,
        reverse: sortOrder === "desc",
        page: currentPage,
        limit: itemsPerPage,
        search: query,
      }, newAbortController.signal)

      setResourceData({
        ...resourceData,
        [requestResource[selectedType as keyof typeof requestResource]]: response.results
      })
      setTotalPages(Math.ceil(response.count / itemsPerPage))
      setCurrentPageItemsCount(response.results.length)

      setResourceState({
        loading: false,
        error: null,
        notFound: false
      })
    } catch (error) {
      setResourceState({
        loading: false,
        error: error as string,
        notFound: false
      })
    }
  }


  const handleSearch = async (query: string) => {
    if (!query) {
      removeKey("q")
    } else {
      updateMultipleKeys({ q: query, page: "1" })
    }
  }

  const handleCreateCategory = async (newCategoryName: string) => {
    if (!selectedType || !newCategoryName) return
    try {
      setCategoryState({
        loading: true,
        error: null,
        notFound: false
      })
      await api.category.create(selectedType, newCategoryName)
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setCategoryState({
        loading: false,
        error: error as string,
        notFound: false
      })
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    if (!selectedType || !categoryId) return
    try {
      setCategoryState({
        loading: true,
        error: null,
        notFound: false
      })
      await api.category.delete(selectedType, categoryId)
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setCategoryState({
        loading: false,
        error: error as string,
        notFound: false
      })
    }
  }

  const handleDeleteMark = async (markId?: number) => {
    if (!selectedType || !selectedCategoryId || !markId) return
    try {
      if (confirm(`Are you sure you want to delete ${markId}?`)) {
        setResourceState({
          loading: true,
          error: null,
          notFound: false
        })
        await api.category.removeMark(selectedType, selectedCategoryId, markId)
        fetchResources()
      }
    } catch (error) {
      setResourceState({
        loading: false,
        error: error as string,
        notFound: false
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
    const timeout = setTimeout(() => {
      setCategoryState({
        loading: false,
        error: null,
        notFound: false
      })
    }, 5000)
    return () => clearTimeout(timeout)
  }, [categoryState.error])

  useEffect(() => {
    const timeout = setTimeout(() => {
      setResourceState({
        loading: false,
        error: null,
        notFound: false
      })
    }, 5000)
    return () => clearTimeout(timeout)
  }, [resourceState.error])


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
      "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4" :
      "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
  }

  return (
    <div className="w-full min-h-screen flex flex-col md:flex-row gap-1">
      {/* Control Panel */}
      <CategoryControlPanel
        open={open}
        type={selectedType}
        categoryOptions={categories.map(category => ({
          value: category.id,
          label: category.category_name,
        }))}
        selectedCategoryId={selectedCategoryId}
        deleteMode={deleteCategoryMode}
        isSearching={isSearching}
        setOpen={setOpen}
        setType={setSelectedType}
        setSelectedCategoryId={setSelectedCategoryId}
        setDeleteMode={setDeleteCategoryMode}
        handleDeleteCategory={handleDeleteCategory}
        handleCreateCategory={handleCreateCategory}
        handleSearch={handleSearch}
        disabled={categoryState.loading || resourceState.loading}
        className={"z-10 md:fixed md:top-[10%]"}
      />
      {/* Placeholder for Control Panel */}
      <div className={cn("max-md:hidden h-full md:w-100 lg:w-120 xl:w-140", !open && "hidden")} />

      {/* Main Content */}
      <div className="overflow-hidden flex-1 p-4 flex flex-col gap-2 transition-all duration-300 justify-between items-center">
        {selectedCategoryId && (
          <div className="w-full flex justify-between gap-2">
            <div className="flex flex-wrap justify-start gap-2">
              {/* Sort By Dialog Button */}
              <Settings2Button
                onClick={() => setSortByDialogOpen(true)}
                disabled={resourceState.loading}
              />
              {/* Sort By Dialog */}
              <SortByDialog
                open={sortByDialogOpen}
                setOpen={setSortByDialogOpen}
                type={selectedType}
                from={"local"}
                sortBy={sortBy}
                setSortBy={setSortBy}
              />
              {/* Order Switch Button */}
              <OrderSwitch
                order={sortOrder}
                setOrder={setSortOrder}
                disabled={resourceState.loading}
              />
              {/* Card Type Button */}
              <CardTypeSwitch
                cardType={cardType}
                setCardType={(value) => setCardType(value as "image" | "text")}
                disabled={resourceState.loading}
              />
              {/* Layout Switch Button */}
              <GridLayoutSwitch
                layout={layout}
                setLayout={(value) => setLayout(value as "grid" | "single")}
                disabled={resourceState.loading}
              />
              {/* Delete Mode Button */}
              <DeleteModeButton
                deleteMode={deleteMarkMode}
                setDeleteMode={setDeleteMarkMode}
                disabled={resourceState.loading}
              />
              {/* Reload Button */}
              <ReloadButton
                handleReload={() => { fetchResources() }}
                disabled={resourceState.loading}
              />
              {/* Total Items Count */}
              <p className="text-gray-500 self-center select-none">Total: {totalItemsCount}</p>
            </div>
            {(selectedType === "v" || selectedType === "c") ? (
              <div className="flex flex-wrap justify-end gap-2">
                <SexualLevelSelector
                  sexualLevel={sexualLevel}
                  setSexualLevel={(value) => setSexualLevel(value as "safe" | "suggestive" | "explicit")}
                  disabled={resourceState.loading}
                />
                {/* Divider */}
                <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block" />
                <ViolenceLevelSelector
                  violenceLevel={violenceLevel}
                  setViolenceLevel={(value) => setViolenceLevel(value as "tame" | "violent" | "brutal")}
                  disabled={resourceState.loading}
                />
              </div>
            ) : (
              <div className="" />
            )}
          </div>
        )}
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
          {(resourceState.loading || resourceState.error || resourceState.notFound) && (
            <motion.div
              key="status"
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
              className="flex-grow flex justify-center items-center"
            >
              {resourceState.loading && (
                <Loading message="Loading..." />
              )}
              {resourceState.error && (
                <Error message={`Error: ${resourceState.error}`} />
              )}
              {resourceState.notFound && (
                <NotFound message="No resources found" />
              )}
            </motion.div>
          )}
          {(!resourceState.loading && !resourceState.error && !resourceState.notFound) && (
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