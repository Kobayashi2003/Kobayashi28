"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { motion, AnimatePresence } from "motion/react"

import { cn } from "@/lib/utils"
import { CategoryTypeSelecter } from "@/components/user/CategoryTypeSelecter"
import { CategorySelecter } from "@/components/user/CategorySelecter"
import { DeleteButton } from "@/components/common/DeleteButton"
import { DeleteModeButton } from "@/components/common/DeleteModeButton"
import { ReloadButton } from "@/components/common/ReloadButton"
import { CategoryCreator } from "@/components/user/CategoryCreator"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"
import { LevelSelecter } from "@/components/common/LevelSelecter"
import { CardTypeSelecter } from "@/components/common/CardTypeSelecter"
import { GenVNCard, GenCharacterCard, GenProducerCard, GenStaffCard } from "@/utils/genCard"

import {
  Category, Mark, VN_Small, Character_Small, Producer_Small, Staff_Small
} from "@/lib/types"
import { api } from "@/lib/api"


export default function UserCategoriesPage() {
  const itemsPerPage = 24

  const [mounted, setMounted] = useState(false)

  const [loadingCategories, setLoadingCategories] = useState(false)
  const [errorCategories, setErrorCategories] = useState<string>("")
  const [loadingResources, setLoadingResources] = useState(false)
  const [errorResources, setErrorResources] = useState<string>("")

  const [categories, setCategories] = useState<Category[]>([])
  const [vns, setVNs] = useState<VN_Small[]>([])
  const [characters, setCharacters] = useState<Character_Small[]>([])
  const [producers, setProducers] = useState<Producer_Small[]>([])
  const [staff, setStaffs] = useState<Staff_Small[]>([])

  const [selectedType, setSelectedType] = useState<string>("v")
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | undefined>(undefined)

  const [name, setName] = useState<string>("")
  const [deleteCategoryMode, setDeleteCategoryMode] = useState<boolean>(false)
  const [toDeleteCategoryId, setToDeleteCategoryId] = useState<number | undefined>(undefined)
  const [deleteMarkMode, setDeleteMarkMode] = useState<boolean>(false)

  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const [cardType, setCardType] = useState<"image" | "text">("image")
  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const fetchCategories = async () => {
    try {
      setLoadingCategories(true)
      const response = await api.category.get(selectedType)
      const sortedCategories = response.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      setCategories(sortedCategories)
    } catch (error) {
      setErrorCategories(error as string)
    } finally {
      setLoadingCategories(false)
    }
  }

  const fetchResources = async () => {
    if (!selectedCategoryId) return
    try {
      setLoadingResources(true)
      const marksResponse = await api.category.getMarks(selectedType, selectedCategoryId)
      const markIds = marksResponse.results.map(mark => mark.id).join(",")

      setTotalPages(Math.ceil(marksResponse.results.length / itemsPerPage))

      switch (selectedType) {
        case "v":
          const vnsResponse = await api.small.vn({
            id: markIds,
            sort: "released",
            reverse: true,
            page: currentPage,
            limit: itemsPerPage,
          })
          setVNs(vnsResponse.results)
          break
        case "c":
          const charactersResponse = await api.small.character({
            id: markIds,
            sort: "name",
            page: currentPage,
            limit: itemsPerPage,
          })
          setCharacters(charactersResponse.results)
          break
        case "p":
          const producersResponse = await api.small.producer({
            id: markIds,
            sort: "name",
            page: currentPage,
            limit: itemsPerPage,
          })
          setProducers(producersResponse.results)
          break
        case "s":
          const staffsResponse = await api.small.staff({
            id: markIds,
            sort: "name",
            page: currentPage,
            limit: itemsPerPage,
          })
          setStaffs(staffsResponse.results)
          break
      }
    } catch (error) {
      setErrorResources(error as string)
    } finally {
      setLoadingResources(false)
    }
  }

  const handleCreateCategory = async () => {
    try {
      if (!selectedType || !name) return
      setLoadingCategories(true)
      await api.category.create(selectedType, name)
      setName("")
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setErrorCategories(error as string)
    } finally {
      setLoadingCategories(false)
    }
  }

  const handleDeleteCategory = async () => {
    try {
      if (!selectedType || !toDeleteCategoryId) return
      setLoadingCategories(true)
      await api.category.delete(selectedType, toDeleteCategoryId)
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setErrorCategories(error as string)
    } finally {
      setLoadingCategories(false)
    }
  }

  const handleDeleteMark = async (markId: number) => {
    try {
      if (!selectedType || !selectedCategoryId) return
      setLoadingResources(true)
      await api.category.removeMark(selectedType, selectedCategoryId, markId)
      fetchResources()
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
    setSelectedCategoryId(undefined)
    fetchCategories()
  }, [selectedType])

  useEffect(() => {
    setCurrentPage(1)
    setTotalPages(0)
    setVNs([])
    setCharacters([])
    setProducers([])
    setStaffs([])
    fetchResources()
  }, [selectedCategoryId])

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" })
    setVNs([])
    setCharacters([])
    setProducers([])
    setStaffs([])
    fetchResources()
  }, [currentPage])

  return (
    <div className="w-full min-h-screen flex flex-col md:flex-row gap-1">
      {/* Category Pannel */}
      <div className={cn(
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
          <DeleteModeButton
            deleteMode={deleteCategoryMode}
            setDeleteMode={setDeleteCategoryMode}
          />
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
            name={name}
            setName={setName}
            handleCreateCategory={handleCreateCategory}
            className="w-full"
          />
        </div>
      </div>
      {/* Placeholder */}
      <div className="hidden h-full md:block md:w-100 lg:w-120 xl:w-140"></div>
      {/* Main Content */}
      <div className={cn(
        "flex-1 container mx-auto md:mt-4 md:ml-4 flex flex-col gap-2 transition-all duration-300 justify-between items-center",
        !mounted && "opacity-0"
      )}>
        {selectedCategoryId && (selectedType === "v" || selectedType === "c") && (
          <div className="w-full flex flex-row gap-2 justify-between items-center">
            {/* Card Type Selector */}
            <div className="flex flex-wrap justify-start gap-2">
              <CardTypeSelecter
                selected={cardType}
                onSelect={(value) => setCardType(value)}
              />
              <DeleteModeButton
                deleteMode={deleteMarkMode}
                setDeleteMode={setDeleteMarkMode}
              />
              <ReloadButton
                onClick={() => { fetchResources() }}
              />
            </div>
            <div className="flex flex-wrap justify-end gap-2">
              {/* Sexual Level Selector */}
              <LevelSelecter
                levelOptions={[
                  {
                    key: "sexual-level-safe", label: "Safe", labelSmall: "🟢SA", value: "safe",
                    activeColor: "text-[#88ccff]", defaultClassName: "hover:text-[#88ccff]/70"
                  },
                  {
                    key: "sexual-level-suggestive", label: "Suggestive", labelSmall: "🟡SU", value: "suggestive",
                    activeColor: "text-[#ffcc66]", defaultClassName: "hover:text-[#ffcc66]/70"
                  },
                  {
                    key: "sexual-level-explicit", label: "Explicit", labelSmall: "🔴EX", value: "explicit",
                    activeColor: "text-[#ff6666]", defaultClassName: "hover:text-[#ff6666]/70"
                  },
                ]}
                selectedValue={sexualLevel}
                onChange={(value) => setSexualLevel(value as "safe" | "suggestive" | "explicit")}
                className="font-serif italic border-r pr-2"
              />
              {/* Violence Level Selector */}
              <LevelSelecter
                levelOptions={[
                  {
                    key: "violence-level-tame", label: "Tame", labelSmall: "🟢TA", value: "tame",
                    activeColor: "text-[#88ccff]", defaultClassName: "hover:text-[#88ccff]/70"
                  },
                  {
                    key: "violence-level-violent", label: "Violent", labelSmall: "🟡VI", value: "violent",
                    activeColor: "text-[#ffcc66]", defaultClassName: "hover:text-[#ffcc66]/70"
                  },
                  {
                    key: "violence-level-brutal", label: "Brutal", labelSmall: "🔴BR", value: "brutal",
                    activeColor: "text-[#ff6666]", defaultClassName: "hover:text-[#ff6666]/70"
                  },
                ]}
                selectedValue={violenceLevel}
                onChange={(value) => setViolenceLevel(value as "tame" | "violent" | "brutal")}
                className="font-serif italic border-r pr-2"
              />
            </div>
          </div>
        )}
        {selectedCategoryId && (selectedType === "s" || selectedType === "p") && (
          <div className="w-full flex flex-row gap-2 justify-start items-center">
            <DeleteModeButton
              deleteMode={deleteMarkMode}
              setDeleteMode={setDeleteMarkMode}
            />
            <ReloadButton
              onClick={() => { fetchResources() }}
            />
          </div>
        )}
        <AnimatePresence mode="wait">
          {!selectedCategoryId ? (
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
          ) : loadingResources ? (
            <motion.div
              key="loading"
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="flex-grow flex justify-center items-center"
            >
              <Loading message="Loading..." />
            </motion.div>
          ) : errorResources ? (
            <motion.div
              key="error"
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="flex-grow flex justify-center items-center"
            >
              <Error message={`Error: ${errorResources}`} />
            </motion.div>
          ) : totalPages === 0 ? (
            <motion.div
              key="notfound"
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="flex-grow flex justify-center items-center"
            >
              <NotFound message="No resources found" />
            </motion.div>
          ) : (
            <motion.div
              key={`${selectedType}-${currentPage}-${cardType}`}
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className={cn(
                "w-full",
                (selectedType === "v" || selectedType === "c") && cardType === "image" ?
                  "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4" :
                  "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
              )}
            >
              {selectedType === "v" && vns.map((vn) => (
                <div key={`card-${vn.id}`} className="relative">
                  <Link href={`/v/${vn.id.slice(1)}`}>
                    {GenVNCard(vn, sexualLevel, violenceLevel, cardType)}
                  </Link>
                  {deleteMarkMode && (
                    <div className="absolute top-0 right-0">
                      <DeleteButton
                        loading={loadingResources}
                        onClick={() => { handleDeleteMark(parseInt(vn.id.slice(1))) }}
                      />
                    </div>
                  )}
                </div>
              ))}
              {selectedType === "c" && characters.map((character) => (
                <div key={`card-${character.id}`} className="relative">
                  <Link href={`/c/${character.id.slice(1)}`}>
                    {GenCharacterCard(character, sexualLevel, violenceLevel, cardType)}
                  </Link>
                  {deleteMarkMode && (
                    <div className="absolute top-0 right-0">
                      <DeleteButton
                        loading={loadingResources}
                        onClick={() => { handleDeleteMark(parseInt(character.id.slice(1))) }}
                      />
                    </div>
                  )}
                </div>
              ))}
              {selectedType === "p" && producers.map((producer) => (
                <div key={`card-${producer.id}`} className="relative">
                  <Link href={`/p/${producer.id.slice(1)}`}>
                    {GenProducerCard(producer)}
                  </Link>
                  {deleteMarkMode && (
                    <div className="absolute top-0 right-0">
                      <DeleteButton
                        loading={loadingResources}
                        onClick={() => { handleDeleteMark(parseInt(producer.id.slice(1))) }}
                      />
                    </div>
                  )}
                </div>
              ))}
              {selectedType === "s" && staff.map((staff) => (
                <div key={`card-${staff.id}`} className="relative">
                  <Link href={`/s/${staff.id.slice(1)}`}>
                    {GenStaffCard(staff)}
                  </Link>
                  {deleteMarkMode && (
                    <div className="absolute top-0 right-0">
                      <DeleteButton
                        loading={loadingResources}
                        onClick={() => { handleDeleteMark(parseInt(staff.id.slice(1))) }}
                      />
                    </div>
                  )}
                </div>
              ))}
            </motion.div>
          )}
        </ AnimatePresence>
        {/* Keep the footer at the bottom of the page */}
        <div className="flex-grow"></div>
        <PaginationButtons
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
        />
      </div>
    </div>
  )
}