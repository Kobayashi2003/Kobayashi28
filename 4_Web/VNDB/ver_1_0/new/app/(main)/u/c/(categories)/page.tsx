"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { motion, AnimatePresence } from "motion/react"

import { cn } from "@/lib/utils"
import { CategoryTypeSelecter } from "@/components/user/CategoryTypeSelecter"
import { CategorySelecter } from "@/components/user/CategorySelecter"
import { DelectModeButton } from "@/components/user/DelectModeButton"
import { CategoryCreator } from "@/components/user/CategoryCreator"
import { ImageCard } from "@/components/common/ImageCard"
import { TextCard } from "@/components/common/TextCard"
import { PaginationButtons } from "@/components/common/PaginationButtons"
import { Loading } from "@/components/common/Loading"
import { Error } from "@/components/common/Error"
import { NotFound } from "@/components/common/NotFound"

import {
  Category, Mark, VN_Small, Character_Small, Producer_Small, Staff_Small
} from "@/lib/types"
import { api } from "@/lib/api"


function GenVNCard(vn: VN_Small, sexualLevel: "safe" | "suggestive" | "explicit", violenceLevel: "tame" | "violent" | "brutal", cardType: "image" | "text") {
  if (cardType === "text") {
    return <TextCard title={vn.title} />
  }
  const sexual = vn.image?.sexual || 0
  const violence = vn.image?.violence || 0
  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      const yellow = sexual > 1 && violence > 1 ? `text-yellow-800` : `text-yellow-400`
      return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={yellow} />
    }
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={vn.title} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  return <ImageCard imageTitle={vn.title} imageUrl={vn.image?.thumbnail || vn.image?.url} imageDims={vn.image?.thumbnail_dims || vn.image?.dims} />
}

function GenCharacterCard(character: Character_Small, sexualLevel: "safe" | "suggestive" | "explicit", violenceLevel: "tame" | "violent" | "brutal", cardType: "image" | "text") {
  if (cardType === "text") {
    return <TextCard title={character.name} />
  }
  const sexual = character.image?.sexual || 0
  const violence = character.image?.violence || 0
  if (sexualLevel === "safe" && sexual > 0.5 || violenceLevel === "tame" && violence > 0.5) {
    if (sexual <= 1 && violence <= 1) {
      const yellow = sexual > 1 && violence > 1 ? `text-yellow-800` : `text-yellow-400`
      return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor={yellow} />
    }
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  if (sexualLevel === "suggestive" && sexual > 1 || violenceLevel === "violent" && violence > 1) {
    const red = sexual > 1 && violence > 1 ? `text-red-800` : `text-red-400`
    return <ImageCard imageTitle={character.name} imageUrl={""} imageDims={[0, 0]} textColor={red} />
  }
  return <ImageCard imageTitle={character.name} imageUrl={character.image?.url} imageDims={character.image?.dims} />
}

function GenProducerCard(producer: Producer_Small) {
  return <TextCard title={producer.name} />
}

function GenStaffCard(staff: Staff_Small) {
  return <TextCard title={staff.name} />
}

export default function UserCategoriesPage() {

  const itemsPerPage = 24

  const [mounted, setMounted] = useState(false)

  const [loadingCategories, setLoadingCategories] = useState(false)
  const [errorCategories, setErrorCategories] = useState<string>("")
  const [loadingMarks, setLoadingMarks] = useState(false)
  const [errorMarks, setErrorMarks] = useState<string>("")
  const [loadingVNs, setLoadingVNs] = useState(false)
  const [errorVNs, setErrorVNs] = useState<string>("")
  const [loadingCharacters, setLoadingCharacters] = useState(false)
  const [errorCharacters, setErrorCharacters] = useState<string>("")
  const [loadingProducers, setLoadingProducers] = useState(false)
  const [errorProducers, setErrorProducers] = useState<string>("")
  const [loadingStaffs, setLoadingStaffs] = useState(false)
  const [errorStaffs, setErrorStaffs] = useState<string>("")

  const [categories, setCategories] = useState<Category[]>([])
  const [marks, setMarks] = useState<Mark[]>([])
  const [vns, setVNs] = useState<VN_Small[]>([])
  const [characters, setCharacters] = useState<Character_Small[]>([])
  const [producers, setProducers] = useState<Producer_Small[]>([])
  const [staff, setStaffs] = useState<Staff_Small[]>([])

  const [selectedType, setSelectedType] = useState<string | undefined>(undefined)
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | undefined>(undefined)

  const [name, setName] = useState<string>("")
  const [deleteMode, setDeleteMode] = useState<boolean>(false)
  const [toDeleteId, setToDeleteId] = useState<number | undefined>(undefined)

  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const [cardType, setCardType] = useState<"image" | "text">("image")
  const [sexualLevel, setSexualLevel] = useState<"safe" | "suggestive" | "explicit">("safe")
  const [violenceLevel, setViolenceLevel] = useState<"tame" | "violent" | "brutal">("tame")

  const fetchCategories = async () => {
    if (!selectedType) return
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

  const fetchMarks = async () => {
    if (!selectedType || !selectedCategoryId) return
    try {
      setLoadingMarks(true)
      const response = await api.category.getMarks(selectedType, selectedCategoryId)
      setMarks(response.results)
    } catch (error) {
      setErrorMarks(error as string)
    } finally {
      setLoadingMarks(false)
    }
  }

  const fetchVNs = async () => {
    setVNs([])
    if (selectedType !== "v" || marks.length === 0) return
    try {
      setLoadingVNs(true)
      const response = await api.small.vn({
        id: marks.map(mark => mark.id).join(","),
        sort: "id",
        page: currentPage,
        limit: itemsPerPage,
      })
      setVNs(response.results)
      setTotalPages(Math.ceil(response.count / itemsPerPage) || 1)
    } catch (error) {
      setErrorVNs(error as string)
    } finally {
      setLoadingVNs(false)
    }
  }

  const fetchCharacters = async () => {
    setCharacters([])
    if (selectedType !== "c" || marks.length === 0) return
    try {
      setLoadingCharacters(true)
      const response = await api.small.character({
        id: marks.map(mark => mark.id).join(","),
        page: currentPage,
        limit: itemsPerPage,
      })
      setCharacters(response.results)
    } catch (error) {
      setErrorCharacters(error as string)
    } finally {
      setLoadingCharacters(false)
    }
  }

  const fetchProducers = async () => {
    setProducers([])
    if (selectedType !== "p" || marks.length === 0) return
    try {
      setLoadingProducers(true)
      const response = await api.small.producer({
        id: marks.map(mark => mark.id).join(","),
        page: currentPage,
        limit: itemsPerPage,
      })
      setProducers(response.results)
    } catch (error) {
      setErrorProducers(error as string)
    } finally {
      setLoadingProducers(false)
    }
  }

  const fetchStaffs = async () => {
    setStaffs([])
    if (selectedType !== "s" || marks.length === 0) return
    try {
      setLoadingStaffs(true)
      const response = await api.small.staff({
        id: marks.map(mark => mark.id).join(","),
        page: currentPage,
        limit: itemsPerPage,
      })
      setStaffs(response.results)
    } catch (error) {
      setErrorStaffs(error as string)
    } finally {
      setLoadingStaffs(false)
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
      if (!selectedType || !toDeleteId) return
      setLoadingCategories(true)
      await api.category.delete(selectedType, toDeleteId)
      setSelectedCategoryId(undefined)
      fetchCategories()
    } catch (error) {
      setErrorCategories(error as string)
    } finally {
      setLoadingCategories(false)
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
      setErrorMarks("")
    }, 5000)
    return () => clearTimeout(timeout)
  }, [errorMarks])

  useEffect(() => {
    setSelectedCategoryId(undefined)
    fetchCategories()
  }, [selectedType])

  useEffect(() => {
    fetchMarks()
  }, [selectedType, selectedCategoryId])

  useEffect(() => {
    if (!selectedType) return
    switch (selectedType) {
      case "v":
        fetchVNs()
        break
      case "c":
        fetchCharacters()
        break
      case "p":
        fetchProducers()
        break
      case "s":
        fetchStaffs()
        break
    }
  }, [currentPage, selectedType, selectedCategoryId])


  console.log({ loadingCategories, loadingMarks, loadingVNs, loadingCharacters, loadingProducers, loadingStaffs })
  
  return (
    <div className="w-full min-h-screen flex flex-col md:flex-row">
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
          />
          <DelectModeButton
            deleteMode={deleteMode}
            setDeleteMode={setDeleteMode}
          />
        </div>
        {errorCategories && (
          <div className="flex-1 flex flex-row gap-2 justify-center items-center">
            <p className="text-red-500/50">{errorCategories}</p>
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
            deleteMode={deleteMode}
            setToDeleteId={setToDeleteId}
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
      <div className="hidden h-full md:block md:w-100 lg:w-120 xl:w-140"></div>

      <div className={cn(
        "flex-1 container mx-auto md:mt-4 md:ml-4 flex flex-col gap-2 transition-all duration-300 justify-between items-center",
        !mounted && "opacity-0"
      )}>




        {/* TODO */}
        <AnimatePresence mode="wait">
          {selectedType === "v" && loadingVNs ||
           selectedType === "c" && loadingCharacters ||
           selectedType === "p" && loadingProducers ||
           selectedType === "s" && loadingStaffs && (
            <motion.div
              key="loading"
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="flex-grow flex justify-center items-center">
              <Loading message="Loading..." />
            </motion.div>
          )}

          {selectedType === "v" && errorVNs ||
           selectedType === "c" && errorCharacters ||
           selectedType === "p" && errorProducers ||
           selectedType === "s" && errorStaffs && (
            <motion.div
              key="error"
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="flex-grow flex justify-center items-center">
              <Error message="Error: {error}" />
            </motion.div>
          )}

          {selectedType === "v" && !loadingVNs && !errorVNs && vns.length === 0 ||
           selectedType === "c" && !loadingCharacters && !errorCharacters && characters.length === 0 ||
           selectedType === "p" && !loadingProducers && !errorProducers && producers.length === 0 ||
           selectedType === "s" && !loadingStaffs && !errorStaffs && staff.length === 0 && (
            <motion.div
              key="notfound"
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="flex-grow flex justify-center items-center">
              <NotFound message="No results found" />
            </motion.div>
          )}

          {selectedType === "v" && vns.length > 0 && (
            <motion.div
              key={`vns-${currentPage}-${cardType}`}
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className={cardType === "image" ?
                "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4" :
                "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4"
              }
            >
              {vns.map((vn) => (
                <Link key={`card-${vn.id}`} href={`/v/${vn.id.slice(1)}`}>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3, delay: 0.1 }}
                  >
                    {GenVNCard(vn, sexualLevel, violenceLevel, cardType)}
                  </motion.div>
                </Link>
              ))}
            </motion.div>
          )}
          {selectedType === "c" && characters.length > 0 && (
            <motion.div
              key={`characters-${currentPage}-${cardType}`}
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className={cardType === "image" ?
                `grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4` :
                `grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4`
              }>
              {characters.map((character) => (
                <Link key={`card-${character.id}`} href={`/c/${character.id.slice(1, -1)}`}>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3, delay: 0.1 }}
                  >
                    {GenCharacterCard(character, sexualLevel, violenceLevel, cardType)}
                  </motion.div>
                </Link>
              ))}
            </motion.div>
          )}
          {selectedType === "p" && producers.length > 0 && (
            <motion.div
              key={`producers-${currentPage}-${cardType}`}
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className={cardType === "image" ?
                `grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4` :
                `grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4`
              }>
              {producers.map((producer) => (
                <Link key={`card-${producer.id}`} href={`/p/${producer.id.slice(1, -1)}`}>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3, delay: 0.1 }}
                  >
                    {GenProducerCard(producer)}
                  </motion.div>
                </Link>
              ))}
            </motion.div>
          )}
          {selectedType === "s" && staff.length > 0 && (
            <motion.div
              key={`staff-${currentPage}-${cardType}`}
              initial={{ filter: "blur(20px)", opacity: 0 }}
              animate={{ filter: "blur(0px)", opacity: 1 }}
              exit={{ filter: "blur(20px)", opacity: 0 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className={cardType === "image" ?
                `grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4` :
                `grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4`
              }>
              {staff.map((staff) => (
                <Link key={`card-${staff.id}`} href={`/s/${staff.id.slice(1, -1)}`}>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3, delay: 0.1 }}
                  >
                    {GenStaffCard(staff)}
                  </motion.div>
                </Link>
              ))}
            </motion.div>
          )}
        </AnimatePresence>




        <PaginationButtons
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
        />
      </div>
    </div>
  )
}