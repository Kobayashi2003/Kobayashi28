"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { cn } from "@/lib/utils"

// import { SortSelector } from "@/components/category/SortSelector"

import { CategoryControlPanel } from "@/components/category/CategoryControlPanel"
import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"

import { TogglePanelButton } from "@/components/button/TogglePanelButton"
import { DeleteButton } from "@/components/button/DeleteButton"
import { DeleteModeButton } from "@/components/button/DeleteModeButton"
import { ReloadButton } from "@/components/button/ReloadButton"
import { PaginationButtons } from "@/components/button/PaginationButtons"
import { Settings2Button } from "@/components/button/Settings2Button"
import { CardTypeSwitch } from "@/components/selector/CardTypeSwtich"
import { OrderSwitch } from "@/components/selector/OrderSwitch"
import { SexualLevelSelector } from "@/components/selector/SexualLevelSelector"
import { ViolenceLevelSelector } from "@/components/selector/ViolenceLevelSelector"
import { SortByDialog } from "@/components/dialog/SortByDialog"
import { VNsCardsGrid, CharactersCardsGrid, ProducersCardsGrid, StaffCardsGrid } from "@/components/card/CardsGrid"

import {
  Category, VN_Small, Character_Small, Producer_Small, Staff_Small
} from "@/lib/types"
import { api } from "@/lib/api"


export default function CategoriesPage() {
  const searchParams = useSearchParams()
  const router = useRouter()

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

  const [loadingCategories, setLoadingCategories] = useState(false)
  const [errorCategories, setErrorCategories] = useState<string>("")
  const [loadingResources, setLoadingResources] = useState(false)
  const [errorResources, setErrorResources] = useState<string>("")
  const [notfoundResources, setNotfoundResources] = useState<boolean>(false)

  const [currentPageItemsCount, setCurrentPageItemsCount] = useState(0)
  const [categories, setCategories] = useState<Category[]>([])
  const [vns, setVNs] = useState<VN_Small[]>([])
  const [characters, setCharacters] = useState<Character_Small[]>([])
  const [producers, setProducers] = useState<Producer_Small[]>([])
  const [staff, setStaffs] = useState<Staff_Small[]>([])

  const [deleteCategoryMode, setDeleteCategoryMode] = useState<boolean>(false)
  const [deleteMarkMode, setDeleteMarkMode] = useState<boolean>(false)

  const [totalPages, setTotalPages] = useState(0)
  const [cardType, setCardType] = useState<"image" | "text">("image")
  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const [categoriesAbortController, setCategoriesAbortController] = useState<AbortController>()
  const [resourcesAbortController, setResourcesAbortController] = useState<AbortController>()


  const removeKeyFromSearchParams = (key: string) => {
    const params = new URLSearchParams(searchParams)
    params.delete(key)
    router.push(`/u/c?${params.toString()}`)
  }

  const removeMultipleKeysFromSearchParams = (keys: string[]) => {
    const params = new URLSearchParams(searchParams)
    keys.forEach(key => params.delete(key))
    router.push(`/u/c?${params.toString()}`)
  }

  const updateSearchParams = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    params.set(key, value)
    router.push(`/u/c?${params.toString()}`)
  }

  const updateMultipleSearchParams = (params: Record<string, string>) => {
    const newParams = new URLSearchParams(searchParams)
    Object.entries(params).forEach(([key, value]) => {
      newParams.set(key, value)
    })
    router.push(`/u/c?${newParams.toString()}`)
  }


  const setSelectedType = (value: string) => {
    updateSearchParams("type", value)
  }

  const setSelectedCategoryId = (value: number | undefined) => {
    if (value === undefined) {
      removeKeyFromSearchParams("cid")
    } else {
      updateSearchParams("cid", value.toString())
    }
  }

  const setCurrentPage = (value: number) => {
    updateSearchParams("page", value.toString())
  }

  const setSortBy = (value: string) => {
    updateSearchParams("sort", value)
  }

  const setSortOrder = (value: string) => {
    updateSearchParams("order", value)
  }


  const fetchCategories = async () => {
    if (!selectedType) return
    try {
      categoriesAbortController?.abort()
      const newAbortController = new AbortController()
      setCategoriesAbortController(newAbortController)

      setLoadingCategories(true)
      setErrorCategories("")
      const response = await api.category.get(selectedType, newAbortController.signal)
      const sortedCategories = response.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      setCategories(sortedCategories)
    } catch (error) {
      setErrorCategories(error as string)
    } finally {
      setLoadingCategories(false)
    }
  }

  const fetchResources = async () => {
    if (!selectedType || !selectedCategoryId) return
    try {
      resourcesAbortController?.abort()
      const newAbortController = new AbortController()
      setResourcesAbortController(newAbortController)

      setLoadingResources(true)
      setErrorResources("")
      setNotfoundResources(false)
      const marksResponse = await api.category.getMarks(selectedType, selectedCategoryId, newAbortController.signal)
      if (marksResponse.results.length === 0) {
        setLoadingResources(false)
        setNotfoundResources(true)
        return
      }
      const markIds = marksResponse.results.map(mark => mark.id).join(",")
      switch (selectedType) {
        case "v":
          const vnsResponse = await api.small.vn({
            from: "local",
            id: markIds,
            sort: sortBy,
            reverse: sortOrder === "desc",
            page: currentPage,
            limit: itemsPerPage,
            search: query,
          }, newAbortController.signal)
          setVNs(vnsResponse.results)
          setTotalPages(Math.ceil(vnsResponse.count / itemsPerPage))
          setCurrentPageItemsCount(vnsResponse.results.length)
          break
        case "c":
          const charactersResponse = await api.small.character({
            id: markIds,
            sort: sortBy,
            reverse: sortOrder === "desc",
            page: currentPage,
            limit: itemsPerPage,
            search: query,
          }, newAbortController.signal)
          setCharacters(charactersResponse.results)
          setTotalPages(Math.ceil(charactersResponse.count / itemsPerPage))
          setCurrentPageItemsCount(charactersResponse.results.length)
          break
        case "p":
          const producersResponse = await api.small.producer({
            id: markIds,
            sort: sortBy,
            reverse: sortOrder === "desc",
            page: currentPage,
            limit: itemsPerPage,
            search: query,
          }, newAbortController.signal)
          setProducers(producersResponse.results)
          setTotalPages(Math.ceil(producersResponse.count / itemsPerPage))
          setCurrentPageItemsCount(producersResponse.results.length)
          break
        case "s":
          const staffsResponse = await api.small.staff({
            id: markIds,
            sort: sortBy,
            reverse: sortOrder === "desc",
            page: currentPage,
            limit: itemsPerPage,
            search: query,
          }, newAbortController.signal)
          setStaffs(staffsResponse.results)
          setTotalPages(Math.ceil(staffsResponse.count / itemsPerPage))
          setCurrentPageItemsCount(staffsResponse.results.length)
          break
      }
    }
    catch (error) {
      setErrorResources(error as string)
    } finally {
      setLoadingResources(false)
    }
  }


  const handleSearch = async (query: string) => {
    if (!query) {
      removeKeyFromSearchParams("q")
    } else {
      updateMultipleSearchParams({ q: query, page: "1" })
    }
  }

  const handleCreateCategory = async (newCategoryName: string) => {
    if (!selectedType || !newCategoryName) return
    try {
      setLoadingCategories(true)
      setErrorCategories("")
      await api.category.create(selectedType, newCategoryName)
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setErrorCategories(error as string)
    } finally {
      setLoadingCategories(false)
    }
  }

  const handleDeleteCategory = async (categoryId: number) => {
    if (!selectedType || !categoryId) return
    try {
      setLoadingCategories(true)
      setErrorCategories("")
      await api.category.delete(selectedType, categoryId)
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setErrorCategories(error as string)
    } finally {
      setLoadingCategories(false)
    }
  }

  const handleDeleteMark = async (markId?: number) => {
    if (!selectedType || !selectedCategoryId || !markId) return
    try {
      if (confirm(`Are you sure you want to delete ${markId}?`)) {
        setLoadingResources(true)
        setErrorResources("")
        await api.category.removeMark(selectedType, selectedCategoryId, markId)
        fetchResources()
      }
    } catch (error) {
      setErrorResources(error as string)
    } finally {
      setLoadingResources(false)
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
      setErrorCategories("")
    }, 5000)
    return () => clearTimeout(timeout)
  }, [errorCategories])

  useEffect(() => {
    const timeout = setTimeout(() => {
      setErrorResources("")
    }, 5000)
    return () => clearTimeout(timeout)
  }, [errorResources])


  useEffect(() => {
    removeMultipleKeysFromSearchParams(["cid", "q", "page", "sort", "order"])
    setTotalPages(0)
    setVNs([])
    setCharacters([])
    setProducers([])
    setStaffs([])
    fetchCategories()
  }, [selectedType])

  useEffect(() => {
    removeMultipleKeysFromSearchParams(["q", "page", "sort", "order"])
    setTotalPages(0)
    setVNs([])
    setCharacters([])
    setProducers([])
    setStaffs([])
    fetchResources()
  }, [selectedCategoryId])

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" })
    setTotalPages(0)
    setVNs([])
    setCharacters([])
    setProducers([])
    setStaffs([])
    fetchResources()
  }, [currentPage, query, sortBy, sortOrder])


  const getItemId = (index: number) => {
    if (selectedType === "v" && vns[index]) {
      return vns[index].id;
    } else if (selectedType === "c" && characters[index]) {
      return characters[index].id;
    } else if (selectedType === "p" && producers[index]) {
      return producers[index].id;
    } else if (selectedType === "s" && staff[index]) {
      return staff[index].id;
    }
    return undefined;
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

  const statusStyle = "flex-grow flex justify-center items-center"

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
        disabled={loadingCategories || loadingResources}
        className={"z-10 md:fixed md:top-[10%]"}
      />
      {/* Placeholder for Control Panel */}
      <div className={cn("max-md:hidden h-full md:w-100 lg:w-120 xl:w-140", !open && "hidden")} />

      {/* Main Content */}
      <div className="flex-1 p-4 flex flex-col gap-2 transition-all duration-300 justify-between items-center">
        {selectedCategoryId && (
          <div className={cn(
            "w-full flex flex-row gap-2",
            selectedType === "v" && "justify-between",
            selectedType === "c" && "justify-between",
            selectedType === "p" && "justify-start",
            selectedType === "s" && "justify-start",
          )}>
            <div className="flex flex-wrap justify-start gap-2">
              {/* Sort By Dialog Button */}
              <Settings2Button
                onClick={() => setSortByDialogOpen(true)}
                disabled={loadingResources}
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
                disabled={loadingResources}
              />
              {/* Card Type Button */}
              <CardTypeSwitch
                cardType={cardType}
                setCardType={(value) => setCardType(value as "image" | "text")}
                disabled={loadingResources}
              />
              {/* Delete Mode Button */}
              <DeleteModeButton
                deleteMode={deleteMarkMode}
                setDeleteMode={setDeleteMarkMode}
                disabled={loadingResources}
              />
              {/* Reload Button */}
              <ReloadButton
                handleReload={() => { fetchResources() }}
                disabled={loadingResources}
              />
            </div>
            {selectedType === "v" || selectedType === "c" && (
              <div className="flex flex-wrap justify-end gap-2">
                <SexualLevelSelector
                  sexualLevel={sexualLevel}
                  setSexualLevel={(value) => setSexualLevel(value as "safe" | "suggestive" | "explicit")}
                  disabled={loadingResources}
                />
                {/* Divider */}
                <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block" />
                <ViolenceLevelSelector
                  violenceLevel={violenceLevel}
                  setViolenceLevel={(value) => setViolenceLevel(value as "tame" | "violent" | "brutal")}
                  disabled={loadingResources}
                />
              </div>
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
          {loadingResources && (
            <motion.div
              key="loading"
              {...fadeInAnimation}
              className={statusStyle}
            >
              <Loading message="Loading..." />
            </motion.div>
          )}
          {errorResources && (
            <motion.div
              key="error"
              {...fadeInAnimation}
              className={statusStyle}
            >
              <Error message={`Error: ${errorResources}`} />
            </motion.div>
          )}
          {notfoundResources && (
            <motion.div
              key="notfound"
              {...fadeInAnimation}
              className={statusStyle}
            >
              <NotFound message="No resources found" />
            </motion.div>
          )}
          {(!loadingResources && !errorResources && !notfoundResources) && (
            <div className="relative w-full">
              {selectedType === "v" ? (
                <VNsCardsGrid
                  vns={vns}
                  cardType={cardType}
                  sexualLevel={sexualLevel}
                  violenceLevel={violenceLevel}
                />
              ) : selectedType === "c" ? (
                <CharactersCardsGrid
                  characters={characters}
                  cardType={cardType}
                  sexualLevel={sexualLevel}
                  violenceLevel={violenceLevel}
                />
              ) : selectedType === "p" ? (
                <ProducersCardsGrid
                  producers={producers}
                />
              ) : selectedType === "s" ? (
                <StaffCardsGrid
                  staff={staff}
                />
              ) : <></>}
              {deleteMarkMode && (
                <motion.div
                  key={`delete-layer-${deleteMarkMode}-${currentPageItemsCount}`}
                  {...fadeInAnimation}
                  className={cn(
                    "absolute inset-0 pointer-events-auto z-10",
                    (selectedType === "v" || selectedType === "c") && gridClassName(cardType),
                    (selectedType === "p" || selectedType === "s") && gridClassName("text")
                  )}
                >
                  {Array.from({ length: currentPageItemsCount }).map((_, index) => (
                    <div key={`delete-container-${index}`} className="relative w-full">
                      <motion.div
                        key={`delete-ghost-card-${index}`}
                        {...cardAnimation}
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