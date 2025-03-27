"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { cn } from "@/lib/utils"

import { CategoryTypeSelecter } from "@/components/category/CategoryTypeSelecter"
import { CategorySelecter } from "@/components/category/CategorySelecter"
import { SortSelector } from "@/components/category/SortSelector"
import { CategoryCreator } from "@/components/category/CategoryCreator"
import { CategorySearcher } from "@/components/category/CategorySearcher"

import { Loading } from "@/components/status/Loading"
import { Error } from "@/components/status/Error"
import { NotFound } from "@/components/status/NotFound"

import { TogglePanelButton } from "@/components/button/TogglePanelButton"
import { DeleteButton } from "@/components/button/DeleteButton"
import { DeleteModeButton } from "@/components/button/DeleteModeButton"
import { ReloadButton } from "@/components/button/ReloadButton"
import { CardTypeButton } from "@/components/button/CardTypeButton"
import { PaginationButtons } from "@/components/button/PaginationButtons"

import { SexualLevelSelector } from "@/components/selector/SexualLevelSelector"
import { ViolenceLevelSelector } from "@/components/selector/ViolenceLevelSelector"

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
  const [mounted, setMounted] = useState(false)
  const [open, setOpen] = useState(true)

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

  const [queryTemp, setQueryTemp] = useState<string>("")
  const [newCategoryName, setNewCategoryName] = useState<string>("")
  const [deleteCategoryMode, setDeleteCategoryMode] = useState<boolean>(false)
  const [toDeleteCategoryId, setToDeleteCategoryId] = useState<number | undefined>(undefined)
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

  const setQuery = (value: string) => {
    updateSearchParams("q", value)
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


  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    const queryTempTrim = queryTemp.trim()
    if (!queryTempTrim) {
      removeKeyFromSearchParams("q")
    } else {
      updateMultipleSearchParams({ q: queryTempTrim, page: "1" })
    }
  }

  const handleCreateCategory = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    if (!selectedType || !newCategoryName) return
    try {
      setLoadingCategories(true)
      setErrorCategories("")
      await api.category.create(selectedType, newCategoryName)
      setNewCategoryName("")
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setErrorCategories(error as string)
    } finally {
      setLoadingCategories(false)
    }
  }

  const handleDeleteCategory = async () => {
    if (!selectedType || !toDeleteCategoryId) return
    try {
      setLoadingCategories(true)
      setErrorCategories("")
      await api.category.delete(selectedType, toDeleteCategoryId)
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
    setMounted(true)
  }, [])

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
      <AnimatePresence mode="wait">
        {/* Category Pannel */}
        {open && (
          <>
            {/* Category Pannel */}
            <motion.div
              key="open"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.1 }}
              className={cn(
                "w-full md:fixed md:top-[10%] md:w-100 lg:w-120 xl:w-140 flex-col gap-2 transition-all duration-300",
                !mounted && "opacity-0"
              )}>
              <div className="flex-1 flex flex-row gap-2 justify-between items-center">
                <CategoryTypeSelecter
                  typeOptions={[
                    { key: "v", value: "v", label: "𝓥" },
                    { key: "c", value: "c", label: "𝓒" },
                    { key: "p", value: "p", label: "𝓟" },
                    { key: "s", value: "s", label: "𝓢" },
                  ]}
                  selectedValue={selectedType}
                  onChange={(value) => setSelectedType(value)}
                  size="icon"
                />
                <div className="flex flex-row gap-2 justify-center items-center">
                  <DeleteModeButton
                    deleteMode={deleteCategoryMode}
                    setDeleteMode={setDeleteCategoryMode}
                  />
                  <TogglePanelButton
                    open={open}
                    setOpen={setOpen}
                    direction="left"
                  />
                </div>
              </div>
              {errorCategories && (
                <div className="flex-1 flex flex-row gap-2 justify-center items-center">
                  {/* <p className="text-red-500/50">{errorCategories}</p> */}
                </div>
              )}
              <div className="flex-1 flex flex-col gap-2 justify-between items-center">
                <CategorySelecter
                  loading={loadingCategories}
                  categoryOptions={categories.map(category => ({
                    key: `category-${category.id}`,
                    value: category.id,
                    label: category.category_name,
                  }))}
                  selectedValue={selectedCategoryId}
                  deleteMode={deleteCategoryMode}
                  setToDeleteId={setToDeleteCategoryId}
                  handleDeleteCategory={handleDeleteCategory}
                  onChange={(value) => setSelectedCategoryId(value)}
                  className="w-full"
                />
                <CategoryCreator
                  loading={loadingCategories}
                  newCategoryName={newCategoryName}
                  setNewCategoryName={setNewCategoryName}
                  handleCreateCategory={handleCreateCategory}
                  className="w-full"
                />
                <CategorySearcher
                  loading={loadingCategories}
                  isSearching={isSearching}
                  query={queryTemp}
                  setQuery={setQueryTemp}
                  handleSearch={handleSearch}
                  className={cn(
                    "w-full",
                    !selectedCategoryId && "opacity-0"
                  )}
                />
              </div>
            </motion.div>
            {/* Placeholder */}
            <motion.div
              key="placeholder"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.1 }}
              className="hidden h-full md:block md:w-100 lg:w-120 xl:w-140"
            />
          </>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className={cn(
        "flex-1 p-4 flex flex-col gap-2 transition-all duration-300 justify-between items-center",
        !mounted && "opacity-0"
      )}>
        {selectedCategoryId && (selectedType === "v" || selectedType === "c") && (
          <div className="w-full flex flex-row gap-2 justify-between items-center">
            <div className="flex flex-wrap justify-start gap-2">
              {/* Show Panel Button */}
              {!open && (
                <TogglePanelButton
                  open={open}
                  setOpen={setOpen}
                  direction="left"
                />
              )}
              {/* Sort Selecter Button */}
              <SortSelector
                type={selectedType}
                sortBy={sortBy}
                sortOrder={sortOrder}
                setSortBy={setSortBy}
                setSortOrder={setSortOrder}
              />
              {/* Card Type Button */}
              <CardTypeButton
                cardType={cardType}
                setCardType={(value) => setCardType(value as "image" | "text")}
              />
              {/* Delete Mode Button */}
              <DeleteModeButton
                deleteMode={deleteMarkMode}
                setDeleteMode={setDeleteMarkMode}
              />
              {/* Reload Button */}
              <ReloadButton
                handleReload={() => { fetchResources() }}
              />
            </div>
            <div className="flex flex-wrap justify-end gap-2">
              <SexualLevelSelector
                sexualLevel={sexualLevel}
                setSexualLevel={(value) => setSexualLevel(value as "safe" | "suggestive" | "explicit")}
              />
              {/* Divider */}
              <div className="w-px bg-gray-300 dark:bg-gray-700 hidden sm:block" />
              <ViolenceLevelSelector
                violenceLevel={violenceLevel}
                setViolenceLevel={(value) => setViolenceLevel(value as "tame" | "violent" | "brutal")}
              />
            </div>
          </div>
        )}
        {selectedCategoryId && (selectedType === "s" || selectedType === "p") && (
          <div className="w-full flex flex-row gap-2 justify-start items-center">
            {/* Show Panel Button */}
            {!open && (
              <TogglePanelButton
                open={open}
                setOpen={setOpen}
                direction="left"
              />
            )}
            {/* Sort Selecter Button */}
            <SortSelector
              type={selectedType}
              sortBy={sortBy}
              sortOrder={sortOrder}
              setSortBy={setSortBy}
              setSortOrder={setSortOrder}
            />
            {/* Delete Mode Button */}
            <DeleteModeButton
              deleteMode={deleteMarkMode}
              setDeleteMode={setDeleteMarkMode}
            />
            {/* Reload Button */}
            <ReloadButton
              handleReload={() => { fetchResources() }}
            />
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